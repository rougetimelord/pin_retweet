__version__ = "0.0.1"
from typing import Dict
import requests, json
from . import AuthHandler


class ClientException(Exception):
    """Client failure"""


class Client:
    """Basic client that only supports pinning and retweeting"""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        user_key: str | None = None,
        user_secret: str | None = None,
        callback: str | None = None,
    ) -> None:
        self.auth = AuthHandler(
            consumer_key, consumer_secret, user_key, user_secret, callback
        )
        self.headers = {}
        self.headers["User-Agent"] = f"Requests/{requests.__version__}"
        self.host = "https://twitter.com/i/api"
        self.session = requests.Session()

    def request(
        self, method: str, endpoint: str, id: str | None = None
    ) -> Dict[str, str]:
        url = f"{self.host}/1.1/{endpoint}.json"
        auth = self.auth.apply_auth()
        params = {}
        if not id == None:
            params["id"] = id
        try:
            resp = self.session.request(
                method, url, params=params, headers=self.headers, auth=auth
            )
        except Exception as e:
            raise ClientException(f"Failed request with: {e}")
        if not 200 <= resp.status_code < 300:
            raise ClientException(f"Failed with HTTP code: {resp.status_code}")
        self.session.close()
        return json.loads(resp.text)

    def pin_tweet(self, id: str) -> Dict[str, str]:
        return self.request("POST", "account/pin_tweet", id=id)

    def retweet(self, id: str) -> Dict[str, str]:
        return self.request("POST", f"statuses/retweet/{id}")

    def retweet_then_pin(self, id: str) -> None:
        data = self.retweet(id)
        self.pin_tweet(data["id_str"])
