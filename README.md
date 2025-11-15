# Fetch Hiscores from Old School Runescape

Easily fetch your OSRS user hiscores with the following:

```python
from runescape.api.osrs.hiscores import Hiscores

user = Hiscores("Zehahandsome")
print(user.character)
```

## Discord Webhook

This repo also provides a Discord webhook that uses AWS Cloud in the
background to log and report progress to a desired Discord channel. This will
continuously provide progress every 7 days to your Discord channel:

<p align="center">
<img src="osrs_discord_webhook_example.png" alt="Discord webhook example" width="400"/>
</p>

To setup Discord webhook, you will have to first install:

1. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

> **__NOTE__:** Remember to configure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY either as
environment variables or within the AWS CLI configuration.

When AWS CLI and Terraform is installed, create a `setup.tfvars` file in the `terraform/` folder. The content
of the `.tfvars` file should look something similar to:

```yaml
osrs_usernames = ["osrs_user1", "osrs_user2"]  # List of the OSRS users to track progress
osrs_remote_folder = "hiscores"  # Prefix for S3 object keys that will hold level information of OSRS users from `osrs_usernames`
discord_webhook_url = "https://discordapp.com/api/webhooks/123456789/blabla-f456ds-this-is-a-fake-url"  # Discord webhook URL
```

> **__NOTE__:** To get the Discord Webhook URL look in `Discord > Server Settings > APPS > Integrations > Webhooks`

From the repository root, run:

```bash
task infra:apply
```

To destroy all the created resources again, run:

```bash
task infra:destroy
```

## Development

### Install UV

Run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Taskfile

Run this command:

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/task/task/setup.deb.sh' | sudo -E bash
```

Then you can install Task with:

```bash
apt install task
```

### Testing

To run tests in this repository, follow these steps:

1. Make sure you have the necessary environment variables set up. These variables are required for the tests to run successfully.

    ```yaml
    DISCORD_WEBHOOK=...
    AWS_ACCESS_KEY_ID=...
    AWS_SECRET_ACCESS_KEY=...
    DISCORD_BOT_TOKEN=...
    ```

2. Run the test command in your terminal or command prompt:

   ```bash
   task test:unit
   ```

   This run all the unit tests in the `tests` directory. To run all tests including the AWS tests, do

   ```bash
   task test:aws
   ```

   This requires all the environment variables to be set from step 1.

3. Check the test results in the terminal or command prompt. Any failures or errors will be displayed, allowing you to identify and fix any issues.

Note: If you encounter any issues related to environment variables, make sure they are correctly set up and accessible to the test environment.
