"""The DiscordClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class DiscordClient(OAuth2Client):
    """Support Discord API.

    * Dashboard: https://discordapp.com/developers/applications/me
    * Docs: https://discordapp.com/developers/docs/topics/oauth2
    * API refer: https://discordapp.com/developers/docs/reference
    """

    access_token_url = "https://discordapp.com/api/oauth2/token"
    authorize_url = "https://discordapp.com/api/oauth2/authorize"
    base_url = "https://discordapp.com/api/v6/"
    name = "discord"
    user_info_url = "https://discordapp.com/api/v6/users/@me"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        assert isinstance(data, dict)
        yield "id", data.get("id")
        yield "username", data.get("username")
        yield "discriminator", data.get("discriminator")
        yield (
            "picture",
            "https://cdn.discordapp.com/avatars/{}/{}.png".format(
                data.get("id"),
                data.get("avatar"),
            ),
        )
