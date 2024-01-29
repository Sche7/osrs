import os
import json

from runescape.webhooks.discord import main

USERNAMES = json.loads(os.environ["USERNAMES"])
BUCKET_NAME = os.environ["BUCKET_NAME"]
REMOTE_FOLDER = os.environ["REMOTE_FOLDER"]


def lambda_handler(event, context):
    main(USERNAMES, BUCKET_NAME, REMOTE_FOLDER)
    return {
        "statusCode": 200,
        "body": (
            "Successfully sent webhook to Discord. "
            f"Saved hiscores to {BUCKET_NAME}/{REMOTE_FOLDER}"
        ),
    }
