"""The Bitbucket2Client provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class Bitbucket2Client(OAuth2Client):
    """Support Bitbucket API 2.0.

    * Dashboard: https://bitbucket.org/account/user/peterhudec/api
    * Docs:https://confluence.atlassian.com/display/BITBUCKET/OAuth+on+Bitbucket+Cloud
    * API refer: https://confluence.atlassian.com/display/BITBUCKET/Using+the+Bitbucket+REST+APIs
    """

    access_token_url = "https://bitbucket.org/site/oauth2/access_token"
    authorize_url = "https://bitbucket.org/site/oauth2/authorize"
    base_url = "https://api.bitbucket.org/2.0/"
    name = "bitbucket"
    user_info_url = "https://api.bitbucket.org/2.0/user"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        assert isinstance(data, dict)
        yield "id", data.get("uuid")
        yield "username", data.get("username")
        yield "last_name", data.get("display_name")
        links = data.get("links", {})
        assert isinstance(links, dict)
        avatar = links.get("avatar", {})
        assert isinstance(avatar, dict)
        yield "picture", avatar.get("href")
        link = links.get("html", {})
        assert isinstance(link, dict)
        yield "link", link.get("href")
