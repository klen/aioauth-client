"""The AmazonClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class AmazonClient(OAuth2Client):
    """Support Amazon.

    * Dashboard: https://developer.amazon.com/lwa/sp/overview.html
    * Docs: https://developer.amazon.com/public/apis/engage/login-with-amazon/docs
    /conceptual_overview.html
    * API reference: https://developer.amazon.com/public/apis
    """

    access_token_url = "https://api.amazon.com/auth/o2/token"
    authorize_url = "https://www.amazon.com/ap/oa"
    base_url = "https://api.amazon.com/"
    name = "amazon"
    user_info_url = "https://api.amazon.com/user/profile"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        assert isinstance(data, dict)
        yield "id", data.get("user_id")
