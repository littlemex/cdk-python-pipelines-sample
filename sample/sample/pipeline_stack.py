from aws_cdk import (
    core,
    #aws_codecommit as codecommit,
    #aws_codepipeline as codepipeline,
    #aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    pipelines as pipelines,
    #aws_secretsmanager as secretmanager
)

import aws_cdk.core as cdk

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #source_artifact = codepipeline.Artifact()
        #cloud_assembly_artifact = codepipeline.Artifact()

        # ソースアクション作成

        cdk.CfnOutput(self, 'hogehoge', value='huga')

        pipeline = pipelines.CodePipeline(self, "Pipeline",
            self_mutation=False,
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.connection("littlemex/cdk-python-pipelines-sample", "feature/init",
                    connection_arn="arn:aws:codestar-connections:us-east-1:067150986393:connection/e8560a96-ffdc-48a0-97be-331b7994a041"
                ),
                primary_output_directory = "sample",
                commands=["ls", "env"],
                env={ "hoge": "huga" }
            ),
            docker_enabled_for_self_mutation=True
        )
        
        pipeline.add_wave("MyWave",
            post=[
                pipelines.CodeBuildStep("RunApproval",
                    commands=["echo build", "ls"],
                    build_environment=codebuild.BuildEnvironment(
                    # The user of a Docker image asset in the pipeline requires turning on
                    # 'dockerEnabledForSelfMutation'.
                        build_image=codebuild.LinuxBuildImage.from_asset(self, "Image",
                            directory="./docker-image"
                        )
                    ),
                    primary_output_directory = "sample",
                    env={ "EXECID": "#{codepipeline.PipelineExecutionId}" }
                )
            ]
        ),
        pipeline.add_wave("Approve",
            pre=[
                pipelines.ManualApprovalStep("PromoteToProd")
            ]
        )
        
        