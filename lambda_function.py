from src.webhooks.discord import main, USERNAMES, BUCKET_NAME, REMOTE_FOLDER


def lambda_handler(event, context):
    main(USERNAMES, BUCKET_NAME, REMOTE_FOLDER)
    return {
        "statusCode": 200,
        "body": "Successfully sent webhook to Discord.",
    }
