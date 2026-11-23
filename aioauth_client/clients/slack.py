"""The SlackClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.base import OAuthError
from aioauth_client.oauth2 import OAuth2Client


class SlackClient(OAuth2Client):
    """Support Slack.

    * Dashboard: https://api.slack.com/apps
    * Docs: https://api.slack.com/docs/oauth
    """

    access_token_url = "https://slack.com/api/oauth.v2.access"
    authorize_url = "https://slack.com/oauth/v2/authorize"
    user_info_url = "https://slack.com/api/users.profile.get"
    base_url = "https://slack.com/api"
    name = "slack"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Convert Slack Response data to UserInfo."""
        assert isinstance(data, dict)
        if not data.get("ok", True):
            raise OAuthError(f"Slack user_info failed: {data.get('error')}")
        user = data.get("profile") or {}
        yield "username", user.get("display_name") or user.get("real_name_normalized")
        yield "picture", user.get("image_72")
        yield "first_name", user.get("first_name")
        yield "last_name", user.get("last_name")
        yield "email", user.get("email")
