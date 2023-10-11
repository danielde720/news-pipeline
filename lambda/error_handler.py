import json
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

class Utils:
    def send_notification(self, message):
        '''Send notification about failure to Slack channel.'''
        _url = SLACK_WEBHOOK_URL
        _msg = {'text': message}
        http = urllib3.PoolManager()
        resp = http.request(method='POST', url=_url, body=json.dumps(_msg).encode('utf-8'))

# Lambda handler function
def lambda_handler(event, context):
    try:
        
        pass
    except Exception as e:
        # On failure, send a Slack notification
        utils = Utils()
        utils.send_notification(f"An error occurred: {str(e)}")

