"""OAuth 2.0 client."""

import logging
from collections.abc import Awaitable
from typing import Any
from urllib.parse import urlencode

import httpx

from aioauth_client.base import Client
from aioauth_client.types import THeaders, TParams, TRes


class OAuth2Client(Client):
    """Implement OAuth2."""

    name = "oauth2"
    shared_key = "code"

    def __init__(  # noqa: PLR0913
        self,
        client_id: str,
        client_secret: str,
        base_url: str | None = None,
        authorize_url: str | None = None,
        access_token: str | None = None,
        access_token_url: str | None = None,
        access_token_key: str | None = None,
        transport: httpx.AsyncClient | None = None,
        logger: logging.Logger | None = None,
        **params: Any,
    ) -> None:
        """Initialize the client."""
        super().__init__(
            base_url, authorize_url, access_token_key, access_token_url, transport, logger
        )

        self.access_token = access_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.params = params

    def get_authorize_url(self, **params: Any) -> str:
        """Return formatted authorize URL."""
        params = dict(self.params, **params)
        params.update({"client_id": self.client_id, "response_type": "code"})
        return f"{self.authorize_url}?{urlencode(params)}"

    def request(
        self,
        method: str,
        url: str,
        params: TParams | None = None,
        headers: THeaders | None = None,
        access_token: str | None = None,
        **options: Any,
    ) -> Awaitable[TRes]:
        """Request OAuth2 resource."""
        url = self.urljoin(url)
        if headers:
            headers = dict(headers)
        else:
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            }
        access_token = access_token or self.access_token
        if access_token:
            headers.setdefault("Authorization", "Bearer %s" % access_token)

        return self._request(method, url, headers=headers, params=params, **options)

    async def get_access_token(
        self,
        code: str,
        redirect_uri: str | None = None,
        headers: dict[str, str] | None = None,
        **payload: Any,
    ) -> tuple[str, Any]:
        """Get an access_token from OAuth provider.

        :returns: (access_token, provider_data)
        """
        # Possibility to provide REQUEST DATA to the method
        payload.setdefault("grant_type", "authorization_code")
        payload.update(
            {"client_id": self.client_id, "client_secret": self.client_secret},
        )

        if code and not isinstance(code, str) and self.shared_key in code:
            code = code[self.shared_key]
        payload["refresh_token" if payload["grant_type"] == "refresh_token" else "code"] = code

        redirect_uri = redirect_uri or self.params.get("redirect_uri")
        if redirect_uri:
            payload["redirect_uri"] = redirect_uri

        data = await self.request(
            "POST", self.access_token_url, raise_for_status=True, data=payload, headers=headers
        )

        if not isinstance(data, dict):
            return "", data

        token = ""
        if "access_token" in data:
            assert isinstance(data["access_token"], str)
            token = data["access_token"]
            self.access_token = token

        else:
            self.logger.warning(
                "Error when getting the access token.\nData returned by OAuth server: %r",
                data,
            )

        return token, data
