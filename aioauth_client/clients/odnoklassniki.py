"""The OdnoklassnikiClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class OdnoklassnikiClient(OAuth2Client):
    """Support ok.ru.

    * Dashboard: http://ok.ru/dk?st.cmd=appsInfoMyDevList
    * Docs: https://apiok.ru/wiki/display/api/Authorization+OAuth+2.0
    * API reference: https://apiok.ru/wiki/pages/viewpage.action?pageId=49381398
    """

    authorize_url = "https://connect.ok.ru/oauth/authorize"
    access_token_url = "https://api.odnoklassniki.ru/oauth/token.do"
    user_info_url = (
        "https://api.ok.ru/api/users/getCurrentUser?"
        "fields=uid,first_name,last_name,gender,city,"
        "country,pic128max"
    )
    name = "odnoklassniki"
    base_url = "https://api.ok.ru"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Set default scope."""
        super().__init__(*args, **kwargs)
        self.params.setdefault("scope", "offline")

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        resp = data.get("response", [{}])[0]
        yield "id", resp.get("uid")
        yield "first_name", resp.get("first_name")
        yield "last_name", resp.get("last_name")
        location = resp.get("location", {})
        yield "city", location.get("city")
        yield "country", location.get("country")
        yield "picture", resp.get("pic128max")
