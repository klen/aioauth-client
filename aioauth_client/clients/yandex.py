"""The YandexClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class YandexClient(OAuth2Client):
    """Support Yandex.

    * Dashboard: https://oauth.yandex.com/client/my
    * Docs: http://api.yandex.com/oauth/doc/dg/reference/obtain-access-token.xml
    """

    access_token_url = "https://oauth.yandex.com/token"
    access_token_key = "oauth_token"
    authorize_url = "https://oauth.yandex.com/authorize"
    base_url = "https://login.yandex.ru/info"
    name = "yandex"
    user_info_url = "https://login.yandex.ru/info"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        assert isinstance(data, dict)
        yield "id", data.get("id")
        yield "username", data.get("login")
        yield "email", data.get("default_email")
        yield "first_name", data.get("first_name")
        yield "last_name", data.get("last_name")
        yield (
            "picture",
            "https://avatars.yandex.net/get-yapic/%s/islands-200"
            % data.get(
                "default_avatar_id",
                0,
            ),
        )
