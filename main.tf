provider "aws" {
    profile = "default"
    region  = "eu-north-1"
}

resource "aws_s3_bucket" "osrs_lambda_bucket" {
    bucket = "osrs-lambda-bucket"
}

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
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject",
                        "s3:ListBucket",
                    ],
                    Effect    = "Allow",
                    Resource  = [
                        aws_s3_bucket.osrs_lambda_bucket.arn
                    ]
                }
            ],
        }
    )
}

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

resource "aws_iam_role_policy_attachment" "osrs_lambda_s3_access" {
    role       = aws_iam_role.osrs_lambda_role.name
    policy_arn = aws_iam_policy.osrs_lambda_policy.arn
}

data "archive_file" "lambda_zip" {
    type        = "zip"
    source_dir  = "src"
    output_path = "lambda_function.zip"
}

resource "aws_lambda_layer_version" "osrs_layer" {
    layer_name           = "osrs"
    filename             = "osrs.zip"
    compatible_runtimes  = [
        "python3.10",
    ]
}

resource "aws_lambda_function" "osrs_lambda" {
    filename         = "osrs.zip"
    function_name    = "osrs_lambda"
    role             = aws_iam_role.osrs_lambda_role.arn
    handler          = "lambda_function.lambda_handler"
    runtime          = "python3.10"
    timeout          = 35
    layers = [aws_lambda_layer_version.osrs_layer.arn]

}

resource "aws_lambda_permission" "allow_eventbridge" {
    statement_id  = "AllowExecutionFromEventBridge"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.osrs_lambda.function_name
    principal     = "events.amazonaws.com"
    source_arn    = aws_lambda_function.osrs_lambda.arn
}
