from aws_cdk import Stage, Stack, Tags, Environment
from constructs import Construct

from application.backend import LambdaFunc
from application.database import Database


class SimpleWebSite(Stage):
    def __init__(self, scope: Construct, id_: str, env: Environment, tags: dict, **kwargs) -> None:
        super().__init__(scope, id_, **kwargs)

        app_infra = Stack(self, "AppInfra", env=env)
        for k, v in tags.items():
            Tags.of(app_infra).add(k, v)

        dynamodb = Database(
            app_infra,
            "DynamoDB"
        )

        LambdaFunc(
            app_infra,
            "LambdaFunc",
            table_arn=dynamodb.db.table_arn
        )


