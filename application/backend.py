from aws_cdk import (
    CfnOutput, Aws,
    aws_lambda as lambda_,
    aws_iam as iam,
)
from constructs import Construct


class LambdaFunc(Construct):

    def __init__(self, scope: Construct, id_: str, table_arn: str) -> None:
        super().__init__(scope, id_)

        # Lambda function
        func = lambda_.Function(
            self,
            "SimpleLambdaWeb",
            function_name="simple-lambda-web",
            handler="lambda_handler.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('lambdas/python'),
            layers=[
                lambda_.LayerVersion.from_layer_version_arn(
                    self,
                    "LambdaPowertools",
                    layer_version_arn=f"arn:aws:lambda:{Aws.REGION}:017000801446:layer:AWSLambdaPowertoolsPythonV2:20"
                )
            ],
            environment={
                "LAMBDA_FUNCTION_URL": "YOUR_LAMBDA_URL"
            }
        )

        func.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:Get*",
                    "dynamodb:Put*",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                ],
                resources=[table_arn]
            )
        )

        func_url = lambda_.FunctionUrl(
            self,
            "SimpleLambdaWebURL",
            function=func,
            auth_type=lambda_.FunctionUrlAuthType.AWS_IAM
        )

        CfnOutput(
            self,
            "LambdaFunctionURL",
            value=func_url.url
        )

