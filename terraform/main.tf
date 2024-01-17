module "discord_hook" {
    source = "./discord_webhook"
    osrs_usernames = var.osrs_usernames
    osrs_remote_folder = var.osrs_remote_folder
    discord_webhook_url = var.discord_webhook_url
}
