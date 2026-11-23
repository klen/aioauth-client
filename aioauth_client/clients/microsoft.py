"""The MicrosoftClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class MicrosoftClient(OAuth2Client):
    """Support Microsoft.

    * Dashboard: https://portal.azure.com/
    * Docs: https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-app-types
    """

    access_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    authorize_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    base_url = "https://graph.microsoft.com/v1.0"
    name = "microsoft"
    user_info_url = "https://graph.microsoft.com/v1.0/me"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse user data."""
        assert isinstance(data, dict)
        yield "id", data.get("id")
        yield "username", data.get("displayName")
        yield "first_name", data.get("givenName")
        yield "last_name", data.get("surname")
        yield "email", data.get("userPrincipalName")
