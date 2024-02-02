"""A script that gets executed as a Google Cloud Function every minute on the minute,
as scheduled by Google Cloud Scheduler."""

import os

import pandas as pd
import requests

BEARER = os.environ["AWAIR_BEARER"]
DEVICE_ID = os.environ["AWAIR_DEVICE_ID"]
PM_HI_EVENT_NAME = os.environ["IFTTT_AWAIR_PM_HI_EVENT"]
PM_LOW_EVENT_NAME = os.environ["IFTTT_AWAIR_PM_LOW_EVENT"]
WEBHOOKS_KEY = os.environ["IFTTT_WEBHOOKS_KEY"]


def query_endpoint() -> pd.Series:
    return pd.DataFrame(
        requests.get(
            "https://developer-apis.awair.is/v1/users/self/devices/awair-element/"
            f"{DEVICE_ID}/air-data/latest",
            headers={"Authorization": f"Bearer {BEARER}"},
        ).json()["data"][0]["indices"]
    ).set_index("comp")["value"]


def check_pm(data: pd.Series) -> bool:
    if data.pm25 > 0:
        return True
    return False


def send_webhook(high: bool = True) -> requests.Request:
    if high:
        event_name = PM_HI_EVENT_NAME
    else:
        event_name = PM_LOW_EVENT_NAME
    return requests.post(
        f"http://maker.ifttt.com/trigger/{event_name}/with/key/{WEBHOOKS_KEY}"
    )


def execute_smart_home():
    send_webhook(high=check_pm(query_endpoint()))
