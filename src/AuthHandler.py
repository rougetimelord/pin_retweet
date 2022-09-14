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
        user_key: str | None,
        user_secret: str | None,
        callback: str | None,
    ) -> None:
        self.con_key = consumer_key
        self.con_secret = consumer_secret
        if user_key == None or user_secret == None:
            raise AuthException("Provide a user token")
        self.user_key = user_key
        self.user_secret = user_secret
        self.callback = callback
        self.oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            callback_uri=self.callback,
        )

    def apply_auth(self) -> OAuth1:
        return OAuth1(
            self.con_key,
            client_secret=self.con_secret,
            resource_owner_key=self.user_key,
            resource_owner_secret=self.user_secret,
            decoding=None,
        )
