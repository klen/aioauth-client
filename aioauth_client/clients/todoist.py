"""The TodoistClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class TodoistClient(OAuth2Client):
    """Support Todoist.

    * Dashboard: https://app.todoist.com/app/settings/integrations/app-management
    * Docs: https://developer.todoist.com/api/v1/

    """

    authorize_url = "https://app.todoist.com/oauth/authorize"
    access_token_url = "https://api.todoist.com/oauth/access_token"
    user_info_url = "https://api.todoist.com/api/v1/user"
    base_url = "https://api.todoist.com/api/v1"
    name = "todoist"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse user data."""
        assert isinstance(data, dict)
        yield "id", data.get("id")
        yield "email", data.get("email")
        first_name, _, last_name = data.get("full_name", "").partition(" ")
        yield "first_name", first_name
        yield "last_name", last_name
        yield "picture", data.get("avatar_big")
        yield "locale", data.get("lang")
