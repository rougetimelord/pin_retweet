__version__ = "0.0.1"
from typing import Dict
import requests, json
from .AuthHandler import AuthHandler


class ClientException(Exception):
    """Client failure"""


class Client:
    """Basic client that only supports pinning and retweeting"""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str | None = None,
        access_token_secret: str | None = None,
        callback: str | None = None,
    ) -> None:
        self.auth: AuthHandler = AuthHandler(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret,
            callback,
        )
        self.headers = {}
        self.headers["User-Agent"] = f"Requests/{requests.__version__}"
        self.session = requests.Session()

    def request(
        self, method: str, endpoint: str, id_str: str | None = None
    ) -> Dict[str, str]:
        url = f"https://api.twitter.com/1.1/{endpoint}.json"
        auth = self.auth.apply_auth()
        params = {}
        if not id_str == None:
            params["id"] = id_str
        try:
            resp = self.session.request(
                method,
                url,
                params=params,
                data=params,
                json=params,
                headers=self.headers,
                auth=auth,
            )
        except Exception as e:
            raise ClientException(f"Failed request with: {e}")

        data = json.loads(resp.text)
        if not 200 <= resp.status_code < 300:
            err = data["errors"]
            raise ClientException(
                f"Failed hitting {endpoint} with HTTP code: {resp.status_code} {err}"
            )

        self.session.close()
        return data

    def pin_tweet(self, id_str: str) -> Dict[str, str | int | Dict]:
        return self.request("POST", "account/pin_tweet", id_str=id_str)

    def retweet(self, id_str: str) -> Dict[str, str | int | Dict]:
        return self.request("POST", f"statuses/retweet/{id_str}")

    def unretweet(
        self,
        id_str: str,
    ) -> Dict[str, str | int | Dict]:
        return self.request("POST", f"statuses/unretweet/{id_str}")

    def retweet_then_pin(self, id_str: str) -> None:
        data = self.retweet(id_str)
        try:
            self.pin_tweet(data["id_str"])
        except Exception as e:
            self.unretweet(id_str)
            raise e
