import sys

import requests

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

data = requests.get("https://www.adidas.com.ar/api/products/IB3593/availability", headers=headers).json()
if not data["availability_status"] == "IN_STOCK":
    print("no hay stock")
    sys.exit(1)

available = [a["size"] for a in data["variation_list"] if a["availability"]]
msg = "Hay stock de camisetas ⭐⭐⭐ del campeón del Mundo. "
msg += f"Talles {', '.join(i for i in available[:-1])} y {available[-1]}." if len(available) > 1 else f"Talle {available[0]} únicamente."

if sys.argv[1] == "--tweet":
    try:
        import tweepy
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "tweepy"])
        import tweepy
    import os

    consumer_key = os.environ["TW_CONSUMER_KEY"]
    consumer_secret = os.environ["TW_CONSUMER_SECRET"]
    access_token = os.environ["TW_ACCESS_TOKEN"]
    access_token_secret = os.environ["TW_ACCESS_TOKEN_SECRET"]

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    response = client.create_tweet(text=msg)
    print(f"https://twitter.com/user/status/{response.data['id']}")
