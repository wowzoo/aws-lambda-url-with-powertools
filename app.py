#!/usr/bin/env python3
import os
import aws_cdk as cdk

from deployment import SimpleWebSite

app = cdk.App()

SimpleWebSite(
    app,
    "SimpleWebSite",
    env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]),
    tags={"Owner": "simple-website"}
)


app.synth()

