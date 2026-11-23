"""The MTSClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class MTSClient(OAuth2Client):
    """Support MTS.

    * Docs: https://developers.mts.ru/mts-id/documentation/tehnicheskoe-opisanie-integratsii
    """

    name = "mts"
    base_url = "https://login.mts.ru/amserver/oauth2"
    authorize_url = f"{base_url}/authorize"
    access_token_url = f"{base_url}/access_token"
    user_info_url = f"{base_url}/userinfo"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        assert isinstance(data, dict)
        yield "phone", data.get("phone")
        yield "country", data.get("country")
        yield "first_name", data.get("first_name")
        yield "last_name", data.get("given_name")
        yield "gender", data.get("gender")
        yield "birthday", data.get("birthday")
