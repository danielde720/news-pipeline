from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_s3 as s3,
    Duration
    
    
)


from constructs import Construct

class NewsPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dotenv_layer = lambda_.LayerVersion(self, "DotenvLayer",
            code=lambda_.Code.from_asset("lambda_layers/python_dotenv"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_11],
            layer_version_name="python-dotenv-layer"
        )
        requests_layer = lambda_.LayerVersion(self, "RequestsLayer",
            code=lambda_.Code.from_asset("lambda_layers/requests"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_11],
            layer_version_name="requests-layer"
        )


        fetch_load_lambda = lambda_.Function(
            self,
            "fetch_load_cdk",
            code=lambda_.Code.from_asset("lambda"),
            handler="fetch_load.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
             layers=[dotenv_layer,requests_layer],
             environment={
                 'NEWS_API_KEY':'f46c462188cd4171a81f3895e8b6e48c',
                 'SLACK_WEBHOOK_URL':'https://hooks.slack.com/services/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'
             },
            timeout=Duration.seconds(20)
        )


        trigger_glue_lambda = lambda_.Function(
            self,
            "trigger_glue_CDK",
            code=lambda_.Code.from_asset("lambda"),
            handler="trigger_glue.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            layers=[dotenv_layer,requests_layer],
            environment={
                'SLACK_WEBHOOK_URL':'https://hooks.slack.com/services/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'
            }
        )



