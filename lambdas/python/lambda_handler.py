import boto3
import os

from http import HTTPStatus
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver, Response, content_types
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Users")

tracer = Tracer()
logger = Logger()
app = LambdaFunctionUrlResolver()

URL = os.environ["LAMBDA_FUNCTION_URL"]


@app.get("/")
@tracer.capture_method
def index():
    with open("index.html", "r") as f:
        html_text = f.read()
        html_text = html_text.replace("YOUR_LAMBDA_URL", URL)

    return Response(
        status_code=HTTPStatus.OK.value,  # 200
        content_type=content_types.TEXT_HTML,
        body=html_text,
    )


@app.get("/sample")
@tracer.capture_method
def get_data():
    kwargs = {
        "ConsistentRead": True,
    }
    response: dict = table.scan(**kwargs)
    logger.info(response)
    body: dict = response["Items"]

    return body


@app.post("/sample")
@tracer.capture_method
def post_data():
    data: dict = app.current_event.json_body

    logger.info(data)

    new_item = {
        "name": data["name"],
        "location": data["location"]
    }

    table.put_item(
        Item=new_item
    )
    body = {"msg": "Data Inserted"}

    return body


@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL, log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
