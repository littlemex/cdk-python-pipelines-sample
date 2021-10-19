#!/usr/bin/env python3

from aws_cdk import core
from sample.pipeline_stack import PipelineStack

app = core.App()
PipelineStack(app, "PipelineStack")

app.synth()