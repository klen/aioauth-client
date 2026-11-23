"""The TrelloClient provider client."""

from aioauth_client.oauth1 import OAuth1Client


class TrelloClient(OAuth1Client):
    """Support Trello.

    * Dashboard: https://trello.com/app-key
    * Docs: https://developer.atlassian.com/cloud/trello/
    """

    access_token_url = "https://trello.com/1/OAuthGetAccessToken"
    authorize_url = "https://trello.com/1/authorize"
    base_url = "https://api.trello.com/1/"
    name = "trello"
    request_token_url = "https://trello.com/1/OAuthGetRequestToken"
    user_info_url = "https://api.trello.com/1/members/me/"

    escape = True
