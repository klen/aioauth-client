"""Provider clients, one module each. Importing registers them all."""

from aioauth_client.clients.amazon import AmazonClient
from aioauth_client.clients.bitbucket import Bitbucket2Client
from aioauth_client.clients.discord import DiscordClient
from aioauth_client.clients.eventbrite import EventbriteClient
from aioauth_client.clients.facebook import FacebookClient
from aioauth_client.clients.flickr import Flickr
from aioauth_client.clients.foursquare import FoursquareClient
from aioauth_client.clients.github import GithubClient
from aioauth_client.clients.gitlab import GitlabClient
from aioauth_client.clients.google import GoogleClient
from aioauth_client.clients.instagram import InstagramClient
from aioauth_client.clients.lichess import LichessClient
from aioauth_client.clients.linkedin import LinkedinClient
from aioauth_client.clients.meetup import Meetup
from aioauth_client.clients.microsoft import MicrosoftClient
from aioauth_client.clients.mts import MTSClient
from aioauth_client.clients.odnoklassniki import OdnoklassnikiClient
from aioauth_client.clients.pinterest import PinterestClient
from aioauth_client.clients.plurk import Plurk
from aioauth_client.clients.slack import SlackClient
from aioauth_client.clients.strava import StravaClient
from aioauth_client.clients.todoist import TodoistClient
from aioauth_client.clients.trello import TrelloClient
from aioauth_client.clients.tumblr import TumblrClient
from aioauth_client.clients.twitter import TwitterClient
from aioauth_client.clients.vimeo import VimeoClient
from aioauth_client.clients.vk import VKClient
from aioauth_client.clients.yandex import YandexClient

__all__ = (
    "AmazonClient",
    "Bitbucket2Client",
    "DiscordClient",
    "EventbriteClient",
    "FacebookClient",
    "Flickr",
    "FoursquareClient",
    "GithubClient",
    "GitlabClient",
    "GoogleClient",
    "InstagramClient",
    "LichessClient",
    "LinkedinClient",
    "MTSClient",
    "Meetup",
    "MicrosoftClient",
    "OdnoklassnikiClient",
    "PinterestClient",
    "Plurk",
    "SlackClient",
    "StravaClient",
    "TodoistClient",
    "TrelloClient",
    "TumblrClient",
    "TwitterClient",
    "VKClient",
    "VimeoClient",
    "YandexClient",
)
