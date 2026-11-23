"""Base classes: errors, user model, registry and the abstract client."""

import logging
from collections.abc import Awaitable, Iterator
from typing import Any, ClassVar, cast
from urllib.parse import parse_qsl, urljoin

import httpx

from aioauth_client.types import THeaders, TParams, TRes


class OAuthError(RuntimeError):
    """AIOAuth Exceptions Class."""


class User:
    """Store user's information."""

    __slots__ = (
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "picture",
        "link",
        "locale",
        "city",
        "country",
        "gender",
        "discriminator",
        "phone",
        "birthday",
    )

    id: int | str | None
    email: str | None
    first_name: str | None
    last_name: str | None
    username: str | None
    picture: str | None
    link: str | None
    locale: str | None
    city: str | int | None
    country: str | int | None
    gender: str | None
    discriminator: str | int | None
    phone: str | None
    birthday: str | None

    def __init__(self, **info: Any) -> None:
        """Initialize self data."""
        for attr in self.__slots__:
            setattr(self, attr, info.get(attr))


class ClientRegistry(type):
    """Meta class to register OAUTH clients."""

    clients: ClassVar[dict[str, type["Client"]]] = {}

    def __new__(
        cls, name: str, bases: tuple[type, ...], params: dict[str, Any]
    ) -> "ClientRegistry":
        """Save created client in self registry."""
        kls = cast("type[Client]", super().__new__(cls, name, bases, params))
        if params.get("name"):
            cls.clients[kls.name] = kls
        return kls


class Client(object, metaclass=ClientRegistry):
    """Base abstract OAuth Client class.

    A client holds one user's tokens: create one per user/request instead of
    sharing an instance between concurrent logins.
    """

    name: str = ""
    base_url: str = ""
    user_info_url: str = ""
    access_token_key: str = "access_token"
    shared_key: str = "oauth_verifier"
    access_token_url: str = ""
    authorize_url: str = ""

    def __init__(  # noqa: PLR0913
        self,
        base_url: str | None = None,
        authorize_url: str | None = None,
        access_token_key: str | None = None,
        access_token_url: str | None = None,
        transport: httpx.AsyncClient | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize the client."""
        self.base_url = base_url or self.base_url
        self.authorize_url = authorize_url or self.authorize_url
        self.access_token_key = access_token_key or self.access_token_key
        self.access_token_url = access_token_url or self.access_token_url
        self.logger = logger or logging.getLogger("OAuth: %s" % self.name)
        self.transport = transport

    def urljoin(self, url: str) -> str:
        """Build provider's url. Join with base_url part if needed."""
        if self.base_url and not url.startswith(("http://", "https://")):
            return urljoin(f"{self.base_url}/", url)
        return url

    def __str__(self) -> str:
        """String representation."""
        return f"{self.name.title()} {self.base_url}"

    def __repr__(self) -> str:
        """String representation."""
        return f"<{self}>"

    async def _request(
        self, method: str, url: str, *, raise_for_status: bool = False, **options: Any
    ) -> TRes:
        """Make a request through HTTPX."""
        client = self.transport or httpx.AsyncClient()
        try:
            self.logger.debug("Request %s: %s", method, url)
            response = await client.request(method, url, **options)
            if raise_for_status and response.status_code >= 300:
                raise OAuthError(str(response))

            if "json" in response.headers.get("content-type", ""):
                return response.json()

            return dict(parse_qsl(response.text)) or response.text
        finally:
            if self.transport is None:
                await client.aclose()

    def request(
        self,
        method: str,
        url: str,
        params: TParams | None = None,
        headers: THeaders | None = None,
        **options: Any,
    ) -> Awaitable[TRes]:
        """Make a request to provider."""
        raise NotImplementedError("Shouldnt be called.")

    async def user_info(self, **options: Any) -> tuple[User, TRes]:
        """Load user information from provider."""
        if not self.user_info_url:
            raise NotImplementedError("The provider doesnt support user_info method.")

        data = await self.request("GET", self.user_info_url, raise_for_status=True, **options)
        if not isinstance(data, dict):
            raise OAuthError(f"Invalid user info response: {data!r}")
        user = User(**dict(self.user_parse(data)))
        return user, data

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:  # noqa: ARG004
        """Parse user's information from given provider data."""
        yield "id", None

    def get_authorize_url(self, **_: Any) -> str:
        """Get an authorization URL."""
        return self.authorize_url

    async def get_access_token(self, *args: Any, **kwargs: Any) -> tuple[str, Any]:
        """Abstract base method."""
        raise NotImplementedError
