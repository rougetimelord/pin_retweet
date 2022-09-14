__version__ = "0.0.1"
from requests_oauthlib import OAuth1, OAuth1Session


class AuthException(Exception):
    """Auth failure"""


class AuthHandler:
    """Basic auth handler"""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str | None,
        access_token_secret: str | None,
        callback: str | None,
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        if access_token == None or access_token_secret == None:
            raise AuthException("Provide a user token")
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.callback = callback
        self.username = None
        self.request_token = {}
        self.oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            callback_uri=self.callback,
        )

    def apply_auth(self):
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            decoding=None,
        )
