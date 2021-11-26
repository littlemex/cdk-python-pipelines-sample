from aws_cdk import (
    core,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    pipelines as pipelines,
    aws_secretsmanager as secretmanager
)

import aws_cdk.core as cdk

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        secret = secretmanager.Secret.from_secret_attributes(self, 'Secret',
            secret_arn='arn:aws:secretsmanager:us-east-1:067150986393:secret:githubtoken-yPq40Q' # FIXME
        )

        artifact = codepipeline.Artifact()

        # ソースアクション作成
        repository_name = 'cdk-python-pipelines-sample'
        owner = 'littlemex';
        oauth_token = 'xxxxx';
        branch = 'feature/init';

        source_action = codepipeline_actions.GitHubSourceAction(
            action_name='Github',
            owner='littlemex',
            repo='cdk-python-pipelines-sample',
            branch='feature/init',
            oauth_token=core.SecretValue.secrets_manager("github-token"),
            #oauth_token=oauth_token,
            trigger=codepipeline_actions.GitHubTrigger.POLL,
            output=artifact
        )

        # hoge 
        cdk.CfnOutput(self, 'hogehoge', value=secret.secret_value.to_string())

        #pipeline = pipelines.CdkPipeline(
        #    self, 'Pipeline',
        ##    cloud_assembly_artifact=source_artifact,
        #    source_action=source_action,

            # Builds our source code outlined above into a could assembly artifact
        #    synth_action=pipelines.SimpleSynthAction(
        #        install_commands=[
        #            'npm install -g aws-cdk', # Installs the cdk cli on Codebuild
        #            'pip install -r requirements.txt' # Instructs codebuild to install required packages
        #        ],
        #        synth_command='npx cdk synth',
        #        source_artifact=source_artifact, # Where to get source code to build
        #        cloud_assembly_artifact=artifact2, # Where to place built source
        #    )
        #)