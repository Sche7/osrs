terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.32.0"
        }
        archive = {
            source  = "hashicorp/archive"
            version = "~> 2.4.1"
        }
    }
}

provider "aws" {
    profile = "default"
    region  = "eu-north-1"
}

# Create a S3 bucket for the lambda function
resource "aws_s3_bucket" "osrs_lambda_bucket" {
    bucket = "osrs-lambda-bucket"
    force_destroy = true
}

# Create a policy for the lambda function
resource "aws_iam_policy" "osrs_lambda_policy" {
    name        = "osrs_lambda_policy"
    description = "Policy for osrs lambda"
    policy      = jsonencode(
        {
            Version   = "2012-10-17",
            Statement = [
                {
                    Sid       = "AllowLambdaAccessToS3",
                    Action    = [
                        "s3:*",
                    ],
                    Effect    = "Allow",
                    Resource  = [
                        "${aws_s3_bucket.osrs_lambda_bucket.arn}",
                        "${aws_s3_bucket.osrs_lambda_bucket.arn}/*"
                    ]
                },
                {
                    Sid       = "AllowLambdaAccessToCloudWatch",
                    Action    = [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    Effect    = "Allow",
                    Resource  = [
                        "arn:aws:logs:*:*:*"
                    ]
                },
                {
                    Sid       = "AllowLambdaAccessToEventBridge",
                    Action    = [
                        "events:PutEvents"
                    ],
                    Effect    = "Allow",
                    Resource  = [
                        "arn:aws:events:*:*:*"
                    ]
                }
            ],
        }
    )
}

# Create a role for the lambda function
resource "aws_iam_role" "osrs_lambda_role" {
    name               = "osrs_lambda_role"
    assume_role_policy = jsonencode(
        {
            Version   = "2012-10-17",
            Statement = [
                {
                    Action    = "sts:AssumeRole",
                    Principal = {
                        Service = "lambda.amazonaws.com"
                    },
                    Effect    = "Allow",
                    Sid       = "AllowLambdaServiceToPerformActions"
                }
            ]
        }
    )
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "osrs_lambda_s3_access" {
    role       = aws_iam_role.osrs_lambda_role.name
    policy_arn = aws_iam_policy.osrs_lambda_policy.arn
}

# Create a lambda layer based on the osrs package
# that (for now) manually needs to be created with command:
# make zip-file
resource "aws_lambda_layer_version" "osrs_layer" {
    layer_name           = "osrs"
    filename             = "../osrs.zip"
    compatible_runtimes  = [
        "python3.10",
    ]
}

# Zip the lambda function
data "archive_file" "lambda_zip" {
    type        = "zip"
    source_file = "discord_webhook/lambda_function.py"
    output_path = "lambda_function.zip"
}

# Create the lambda function
resource "aws_lambda_function" "osrs_lambda" {
    filename         = "lambda_function.zip"
    function_name    = "osrs_lambda"
    role             = aws_iam_role.osrs_lambda_role.arn
    handler          = "lambda_function.lambda_handler"
    runtime          = "python3.10"
    timeout          = 35
    layers = [aws_lambda_layer_version.osrs_layer.arn]
    environment {
        variables = {
            BUCKET_NAME = aws_s3_bucket.osrs_lambda_bucket.bucket,
            USERNAMES = jsonencode(var.osrs_usernames),
            REMOTE_FOLDER = var.osrs_remote_folder,
            DISCORD_WEBHOOK = var.discord_webhook_url,
        }
    }
}

# Schedule event with EventBridge (CloudWatch)
# Create a rule that triggers every 7 days
resource "aws_cloudwatch_event_rule" "osrs_lambda_event" {
    name                = "osrs_lambda_event"
    description         = "Event for osrs lambda"
    schedule_expression = "cron(0 6 ? * * *)"
}

# Create a target lambda function for the rule
resource "aws_cloudwatch_event_target" "osrs_lambda_target" {
    rule      = aws_cloudwatch_event_rule.osrs_lambda_event.name
    target_id = "osrs_lambda_target"
    arn       = aws_lambda_function.osrs_lambda.arn
}

# Allow CloudWatch to invoke the lambda function
resource "aws_lambda_permission" "allow_cloudwatch" {
    statement_id  = "AllowExecutionFromCloudWatch"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.osrs_lambda.function_name
    principal     = "events.amazonaws.com"
    source_arn    = aws_cloudwatch_event_rule.osrs_lambda_event.arn
}

# Invoke the lambda function manually the first time
resource "aws_lambda_invocation" "example" {
  function_name = aws_lambda_function.osrs_lambda.function_name
    input       = jsonencode({})
}
