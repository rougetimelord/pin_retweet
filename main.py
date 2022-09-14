import limited_twit, json


def main():
    with open("key.json", "r") as f:
        keys = json.load(f)
    client = limited_twit.Client(
        keys["consumer_key"],
        keys["consumer_secret"],
        keys["access_token"],
        keys["access_token_secret"],
    )
    id_str = input("Tweet link: ").split("/")[-1].split("?")[0]
    try:
        resp = client.retweet_then_pin(id_str)
    except limited_twit.ClientException as e:
        print(e)


if __name__ == "__main__":
    main()
