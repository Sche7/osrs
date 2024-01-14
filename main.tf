provider "aws" {
    profile = "default"
    region  = "eu-north-1"
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
    source_code_hash = filebase64sha256("osrs.zip")
    runtime          = "python3.10"
    timeout          = 300
    layers = [aws_lambda_layer_version.osrs_layer.arn]

}

resource "aws_lambda_permission" "allow_eventbridge" {
    statement_id  = "AllowExecutionFromEventBridge"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.osrs_lambda.function_name
    principal     = "events.amazonaws.com"
    source_arn    = aws_lambda_function.osrs_lambda.arn
}

resource "aws_iam_role" "osrs_lambda_role" {
    name = "osrs_lambda_role"
    assume_role_policy = jsonencode(
        {
            Version = "2012-10-17",
            Statement = [
                {
                    Action = "sts:AssumeRole",
                    Principal = {
                        Service = "lambda.amazonaws.com"
                    },
                    Effect = "Allow",
                    Sid = ""
                }
            ]
        }
    )
}