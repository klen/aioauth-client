"""The StravaClient provider client."""

from aioauth_client.oauth2 import OAuth2Client


class StravaClient(OAuth2Client):
    """Support Strava."""

    access_token_url = "https://www.strava.com/oauth/token"
    authorize_url = "https://www.strava.com/oauth/authorize"
    base_url = "https://www.strava.com/api/v3/"
    name = "strava"
