"""The VKClient provider client."""

from collections.abc import Awaitable, Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client
from aioauth_client.types import TParams, TRes


class VKClient(OAuth2Client):
    """Support vk.com.

    * Dashboard: http://vk.com/editapp?id={consumer_key}
    * Docs: http://vk.com/developers.php?oid=-17680044&p=Authorizing_Sites
    * API reference: http://vk.com/developers.php?oid=-17680044&p=API_Method_Description
    """

    authorize_url = "https://api.vk.com/oauth/authorize"
    access_token_url = "https://api.vk.com/oauth/access_token"
    user_info_url = (
        "https://api.vk.com/method/getProfiles?"
        "fields=uid,first_name,last_name,nickname,sex,bdate,city,"
        "country,timezone,photo_big"
    )
    name = "vk"
    base_url = "https://api.vk.com"

    def __init__(self, version: str = "5.9.2", *args: Any, **kwargs: Any) -> None:
        """Set default scope."""
        super(VKClient, self).__init__(*args, **kwargs)
        self.user_info_url = "{0}&v={1}".format(self.user_info_url, version)
        self.params.setdefault("scope", "offline")

    def request(  # type: ignore[override]  # VK keeps access_token as the third argument
        self,
        method: str,
        url: str,
        access_token: str | None = None,
        params: TParams | None = None,
        **aio_kwargs: Any,
    ) -> Awaitable[TRes]:
        """VK supports access token only in query."""
        params = params or {}
        access_token = access_token or self.access_token
        if access_token:
            params.setdefault("access_token", access_token)

        return super(VKClient, self).request(
            method,
            url,
            access_token=access_token,
            params=params,
            **aio_kwargs,
        )

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        resp = data.get("response", [{}])[0]
        yield "id", resp.get("id")
        yield "first_name", resp.get("first_name")
        yield "last_name", resp.get("last_name")
        yield "username", resp.get("nickname")
        yield "city", resp.get("city")
        yield "country", resp.get("country")
        yield "picture", resp.get("photo_big")
