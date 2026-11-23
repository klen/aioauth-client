"""The TodoistClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.base import OAuthError, User
from aioauth_client.oauth2 import OAuth2Client
from aioauth_client.types import TParams, TRes


class TodoistClient(OAuth2Client):
    """Support Todoist.

    * Dashboard: https://developer.todoist.com/appconsole.html
    * Docs: https://developer.todoist.com/sync/v8/

    """

    authorize_url = "https://todoist.com/oauth/authorize"
    access_token_url = "https://todoist.com/oauth/access_token"
    user_info_url = "https://api.todoist.com/sync/v9/sync"
    base_url = "https://api.todoist.com/rest/v2"
    name = "todoist"

    async def user_info(
        self,
        access_token: str | None = None,
        params: TParams | None = None,
        **kwargs: Any,
    ) -> tuple[User, TRes]:
        """Load user data."""
        params = params or {
            "token": access_token or self.access_token,
            "sync_token": "*",
            "resource_types": '["user"]',
        }
        return await super(TodoistClient, self).user_info(params=params, **kwargs)

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse user data."""
        assert isinstance(data, dict)
        user = data.get("user")
        if not isinstance(user, dict):
            raise OAuthError(f"Invalid user info response: {data!r}")
        yield "id", user.get("id")
        yield "email", user.get("email")
        first_name, _, last_name = user.get("full_name", "").partition(" ")
        yield "first_name", first_name
        yield "last_name", last_name
        yield "picture", user.get("avatar_big")
        yield "locale", user.get("lang")
