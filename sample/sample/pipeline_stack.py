from aws_cdk import (
    core,
    aws_codecommit as codecommit,
)
# from pipeline_stage import PipelineStage

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'WorkshopRepo'
        repo = codecommit.Repository(
            self, 'SampleRepo',
            repository_name= "SampleRepo"
        )