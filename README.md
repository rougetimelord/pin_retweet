# pin_retweet
Tries to pin the status created by retweeting someone else's tweet

## limited_twit
Included in this package is an extremely limited Twitter API wrapper based on Tweepy. Unlike tweepy the Client handles intializing an auth in its own initialization.

Usage example:
```python
import limited_twit

client = limited_twit(
    "your consumer key",
    "your consumer secret",
    "your access token",
    "your access token secret"
)

client.retweet("12345678910")
client.unretweet("12345678910")
client.retweet_then_pin("12345678910")
```
