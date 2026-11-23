"""The GitlabClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class GitlabClient(OAuth2Client):
    """Support GitLab.

    * Dashboard: https://gitlab.com/-/profile/applications
    * Docs: https://docs.gitlab.com/ee/integration/oauth_provider.html
    """

    access_token_url = "https://gitlab.com/oauth/token"
    authorize_url = "https://gitlab.com/oauth/authorize"
    base_url = "https://gitlab.com/api/v4"
    name = "gitlab"
    user_info_url = "https://gitlab.com/api/v4/user"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        assert isinstance(data, dict)
        yield "id", data.get("id")
        yield "email", data.get("email")
        first_name, _, last_name = (data.get("name") or "").partition(" ")
        yield "first_name", first_name
        yield "last_name", last_name
        yield "username", data.get("username")
        yield "picture", data.get("avatar_url")
        yield "link", data.get("web_url")
        location = data.get("location", "")
        if location:
            split_location = location.split(",")
            yield "country", split_location[0].strip()
            if len(split_location) > 1:
                yield "city", split_location[1].strip()
