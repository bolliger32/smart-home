import os

import pandas as pd
import requests

BEARER = os.environ("AWAIR_BEARER")
DEVICE_ID = os.environ("AWAIR_DEVICE_ID")
EVENT_NAME = os.environ("IFTTT_AWAIR_PM_EVENT")
WEBHOOKS_KEY = os.environ("IFTTT_WEBHOOKS_KEY")


def query_endpoint():
    return pd.DataFrame(
        requests.get(
            "https://developer-apis.awair.is/v1/users/self/devices/awair-element/"
            f"{DEVICE_ID}/air-data/latest",
            headers={"Authorization": f"Bearer {BEARER}"},
        ).json()["data"][0]["indices"]
    ).set_index("comp")["value"]


def check_pm(data):
    if data.pm25 > 0:
        return True
    return False


def send_webhook():
    return requests.post(
        f"http://maker.ifttt.com/trigger/{EVENT_NAME}/json/with/key/{WEBHOOKS_KEY}",
        headers={"Content-Type": "application/json"},
    )


def main():
    data = query_endpoint()
    if check_pm(data):
        return send_webhook()
