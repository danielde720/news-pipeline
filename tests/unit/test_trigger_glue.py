import pytest
from unittest.mock import patch
from trigger_glue  import lambda_handler 
from botocore.exceptions import ClientError

# Test successful Glue job start
def test_lambda_handler_success(mocker):
    mock_boto_client = mocker.patch('boto3.client')
    mock_start_job_run = mocker.Mock()
    mock_start_job_run.return_value = {'JobRunId': 'test_id'}
    mock_boto_client.return_value.start_job_run = mock_start_job_run

    response = lambda_handler(None, None)

    assert response['statusCode'] == 200
    assert 'Glue job started with response' in response['body']

# Test Glue job start failure
def test_lambda_handler_failure(mocker):
    mock_boto_client = mocker.patch('boto3.client')
    mock_start_job_run = mocker.Mock()
    mock_start_job_run.side_effect = ClientError({"Error": {"Code": "400", "Message": "Test Error"}}, "start_job_run")
    mock_boto_client.return_value.start_job_run = mock_start_job_run

    mock_send_notification = mocker.patch('error_handler.Utils.send_notification')

    with pytest.raises(ClientError):
        lambda_handler(None, None)

    mock_send_notification.assert_called_once()
