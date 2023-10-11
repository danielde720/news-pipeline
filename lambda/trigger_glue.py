import boto3
from error_handler import Utils  # Import the Utils class

def lambda_handler(event, context):
    utils = Utils()  # Create an instance of Utils
    try:
        client = boto3.client('glue')
        response = client.start_job_run(JobName='news-glue')
        
        return {
            'statusCode': 200,
            'body': f"Glue job started with response: {response}"
        }
    except Exception as e:
        utils.send_notification(f"Error in trigger_glue_job: {str(e)}")  # Send error notification
        raise  # Re-raise the exception to AWS Lambda

