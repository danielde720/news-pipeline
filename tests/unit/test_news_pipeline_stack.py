import aws_cdk as core
import aws_cdk.assertions as assertions
from news_pipeline.news_pipeline_stack import NewsPipelineStack

def test_lambda_layers_created():
    app = core.App()
    stack = NewsPipelineStack(app, "news-pipeline")
    template = assertions.Template.from_stack(stack)

    # Test for DotenvLayer
    template.resource_count_is("AWS::Lambda::LayerVersion", 2)

def test_lambda_environment_variables():
    app = core.App()
    stack = NewsPipelineStack(app, "news-pipeline")
    template = assertions.Template.from_stack(stack)

    # Test for fetch_load_cdk Lambda function
    template.has_resource_properties("AWS::Lambda::Function", {
        "Environment": {
            "Variables": {
                "NEWS_API_KEY": "f46c462188cd4171a81f3895e8b6e48c",
                "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/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"
            }
        }
    })

def test_lambda_timeout():
    app = core.App()
    stack = NewsPipelineStack(app, "news-pipeline")
    template = assertions.Template.from_stack(stack)

    # Test for fetch_load_cdk Lambda function
    template.has_resource_properties("AWS::Lambda::Function", {
        "Timeout": 20
    })
