"""OAuth 1.0a client and signature implementations."""

import base64
import hmac
import logging
import time
from collections.abc import Awaitable
from hashlib import sha1
from random import SystemRandom
from typing import Any, cast
from urllib.parse import quote, urlencode, urlsplit

import httpx

from aioauth_client.base import Client, OAuthError
from aioauth_client.types import THeaders, TParams, TRes

RANDOM = SystemRandom().random


class Signature:
    """Abstract base class for signature methods."""

    name: str = ""

    @staticmethod
    def _escape(s: str) -> str:
        """URL escape a string."""
        return quote(s, safe=b"~")

    def sign(
        self,
        consumer_secret: str,
        method: str,
        url: str,
        oauth_token_secret: str | None = None,
        **params: Any,
    ) -> str:
        """Abstract method."""
        raise NotImplementedError("Shouldnt be called.")


class HmacSha1Signature(Signature):
    """HMAC-SHA1 signature-method."""

    name = "HMAC-SHA1"

    def sign(
        self,
        consumer_secret: str,
        method: str,
        url: str,
        oauth_token_secret: str | None = None,
        *,
        escape: bool = False,
        **params,
    ) -> str:
        """Create a signature using HMAC-SHA1."""
        if escape:
            query = [(self._escape(k), self._escape(v)) for k, v in params.items()]
            query_string = "&".join(["%s=%s" % item for item in sorted(query)])

        else:
            query_string = urlencode(sorted(params.items()))

        signature = "&".join(map(self._escape, (method.upper(), url, query_string)))

        key = self._escape(consumer_secret) + "&"
        if oauth_token_secret:
            key += self._escape(oauth_token_secret)

        hashed = hmac.new(key.encode(), signature.encode(), sha1)
        return base64.b64encode(hashed.digest()).decode()


class OAuth1Client(Client):
    """Implement OAuth1."""

    name = "oauth1"
    access_token_key = "oauth_token"
    version = "1.0"
    escape = False
    request_token_url: str = ""

    def __init__(  # noqa: PLR0913
        self,
        consumer_key: str,
        consumer_secret: str,
        base_url: str | None = None,
        authorize_url: str | None = None,
        oauth_token: str | None = None,
        oauth_token_secret: str | None = None,
        request_token_url: str | None = None,
        access_token_url: str | None = None,
        access_token_key: str | None = None,
        transport: httpx.AsyncClient | None = None,
        logger: logging.Logger | None = None,
        signature: Signature | None = None,
        **params: Any,
    ) -> None:
        """Initialize the client."""
        super().__init__(
            base_url,
            authorize_url,
            access_token_key,
            access_token_url,
            transport,
            logger,
        )

        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.request_token_url = request_token_url or self.request_token_url
        self.params = params
        self.signature = signature or HmacSha1Signature()

    def get_authorize_url(self, request_token: str | None = None, **params: Any) -> str:
        """Return formatted authorization URL."""
        params.update({"oauth_token": request_token or self.oauth_token})
        params.update(self.params)
        return self.authorize_url + "?" + urlencode(params)

    def request(
        self,
        method: str,
        url: str,
        params: TParams | None = None,
        headers: THeaders | None = None,
        **options: Any,
    ) -> Awaitable[TRes]:
        """Make a request to provider."""
        oparams = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_nonce": sha1(str(RANDOM()).encode("ascii")).hexdigest(),  # noqa: S324
            "oauth_signature_method": self.signature.name,
            "oauth_timestamp": str(int(time.time())),
            "oauth_version": self.version,
            **(params or {}),
        }

        if self.oauth_token:
            oparams["oauth_token"] = self.oauth_token

        url = self.urljoin(url)

        if urlsplit(url).query:
            raise ValueError(
                'Request parameters should be in the "params" parameter, not inlined in the URL',
            )

        oparams["oauth_signature"] = self.signature.sign(
            self.consumer_secret,
            method,
            url,
            oauth_token_secret=self.oauth_token_secret,
            escape=self.escape,
            **oparams,
        )
        return self._request(method, url, params=oparams, headers=headers, **options)

    async def get_request_token(self, **params: Any) -> tuple[str, Any]:
        """Get a request_token and request_token_secret from OAuth1 provider."""
        params = dict(self.params, **params)
        data = await self.request(
            "GET", self.request_token_url, raise_for_status=True, params=params
        )
        if not isinstance(data, dict):
            return "", data

        self.oauth_token = cast(str, data.get("oauth_token") or "")
        self.oauth_token_secret = cast(str, data.get("oauth_token_secret"))
        return self.oauth_token, data

    async def get_access_token(
        self,
        oauth_verifier: str | dict[str, Any],
        request_token: str | None = None,
        headers: THeaders | None = None,
        **_: Any,
    ) -> tuple[str, dict[str, Any]]:
        """Get access_token from OAuth1 provider.

        :returns: (access_token, access_token_secret, provider_data)
        """
        # Possibility to provide REQUEST DATA to the method
        if not isinstance(oauth_verifier, str):
            oauth_verifier = str(oauth_verifier.get(self.shared_key, ""))

        if request_token and self.oauth_token != request_token:
            raise OAuthError(
                "Failed to obtain OAuth 1.0 access token. Request token is invalid",
            )

        data = await self.request(
            "POST",
            self.access_token_url,
            raise_for_status=True,
            headers=headers,
            params={"oauth_verifier": oauth_verifier, "oauth_token": request_token},
        )

        if not isinstance(data, dict):
            raise OAuthError(
                f"Failed to obtain OAuth 1.0 access token. Invalid data: {data}",
            )

        self.oauth_token = cast(str, data.get("oauth_token") or "")
        self.oauth_token_secret = cast(str, data.get("oauth_token_secret"))

        return self.oauth_token, data
