import os
import random
import sys

import requests
import tweepy

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}

data = requests.get(
    "https://www.adidas.com.ar/api/products/IB3593/availability", headers=headers
).json()
NO_STOCK_MESSAGES = [
    "Ya no quedan 😔. Pero te aviso en cuanto me entere.",
    "Se acabaron. Vuelan. Tss tss tss.",
    "Durmieron, pero tranqui que me ocupo.",
    "Fue bueno mientras duró. Pero seguimos siendo campeones del mundo.",
]


if data["availability_status"] == "IN_STOCK":
    available = [a["size"] for a in data["variation_list"] if a["availability"]]
    msg = "Hay stock de camisetas ⭐⭐⭐ del campeón del Mundo. "
    msg += (
        f"Talles {', '.join(i for i in available[:-1])} y {available[-1]}."
        if len(available) > 1
        else f"Talle {available[0]} únicamente."
    )
    msg += " https://www.adidas.com.ar/camiseta-titular-argentina-3-estrellas-2022/IB3593.html"
else:
    msg = random.choice(NO_STOCK_MESSAGES)

print(msg)


if len(sys.argv) > 1 and sys.argv[1] == "--tweet":
    consumer_key = os.environ["TW_CONSUMER_KEY"]
    consumer_secret = os.environ["TW_CONSUMER_SECRET"]
    access_token = os.environ["TW_ACCESS_TOKEN"]
    access_token_secret = os.environ["TW_ACCESS_TOKEN_SECRET"]

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    me = client.get_me()
    last_tweet = client.get_users_tweets(
        me.data.id, user_auth=True, max_results=5
    ).data[0]

    # only tweet one "no stock" message
    if str(last_tweet) not in NO_STOCK_MESSAGES:

        response = client.create_tweet(
            text=msg
        )
        print(f"https://twitter.com/user/status/{response.data['id']}")
