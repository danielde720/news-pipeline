import boto3
from moto import mock_s3
import pytest
from requests.exceptions import Timeout,MissingSchema, InvalidURL
import json
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
sys.path.append('/Users/drod/de_projects/news_pipeline/lambda')
from fetch_load import fetch_news, save_articles_to_file, upload_file_to_s3,lambda_handler
from error_handler import Utils



#mocking the expected response from the api 
@pytest.fixture
def mock_fetch_articles(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "status": "ok",
        "articles": [
            {
                "source": {"id": "bleacher-report", "name": "Bleacher Report"},
                "author": "Jack Murray",
                "title": "Mocked Title 1",
                "description": "Mocked Description 1",
                "url": "https://bleacherreport.com/mock-article-1",
                "urlToImage": "https://media.bleacherreport.com/mock-image-1.jpg",
                "publishedAt": "2023-08-18T19:32:41Z",
                "content": "Mocked Content 1"
            },
        
            {
                "source": {"id": None, "name": "Forbes"},
                "author": "Brian Mazique",
                "title": "Mocked Title 2",
                "description": "Mocked Description 2",
                "url": "https://www.forbes.com/mock-article-2",
                "urlToImage": "https://imageio.forbes.com/mock-image-2.jpg",
                "publishedAt": "2023-09-05T16:25:30Z",
                "content": "Mocked Content 2"

            },
            {
                 "source": {"id": "cnn", "name": "CNN"},
                "author": "Mocked Author 3",
                "title": "Mocked Title 3",
                "description": "Mocked Description 3",
                "url": "https://mockurl3.com",
                "urlToImage": "https://mockurltoimage3.com",
                "publishedAt": "2023-07-20T19:32:41Z",
                "content": "Mocked Content 3"

            },
            {
                "source": {"id": None, "name": "BBC"},
                "author": None,
                "title": "Mocked Title 4",
                "description": "Mocked Description 4",
                "url": "https://mockurl4.com",
                "urlToImage": None,
                "publishedAt": "2023-08-18T19:32:41Z",
                "content": "Mocked Content 4"
            },
            {
                "source": {"id": "fox-news", "name": "Fox News"},
                "author": "Mocked Author 5",
                "title": None,
                "description": None,
                "url": "https://mockurl5.com",
                "urlToImage": "https://mockurltoimage5.com",
                "publishedAt": "2023-09-05T16:25:30Z",
                "content": None

            },

        ]
    }
    mock_response.status_code = 200
    return mocker.patch('fetch_load.requests.get', return_value=mock_response)


#Testing for article amount and making it sure its only 5 
def test_fetch_news_returns_correct_number_of_articles(mock_fetch_articles):
    articles = fetch_news(current_date=None) #Since current date is only required for slack 
    assert len(articles) == 5 

#Testing on failure to see if the slack notification will be sent 
def test_fetch_news_handles_empty_list(mocker):
        #Mock the slack notification 
        mock_send_notification = mocker.patch('fetch_load.Utils.send_notification')

        
    
     # Mock the API response to return a 200 status code and an empty list of articles
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"status": "ok", "articles": []}
        mock_response.status_code = 200
        mocker.patch('requests.get', return_value=mock_response)
    
    # Call the lambda_handler 
        lambda_handler(None, None)

    # Assert that the Slack notification function was called
        mock_send_notification.assert_called_once()

#API failure
def test_fetch_news_handles_api_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch('fetch_load.requests.get', return_value=mock_response)
    
    
    mock_date = "2023-10-14"
    
    articles = fetch_news(current_date=mock_date)
    assert articles == []


    
#Class to mock the response object returned by request.get
class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

    def json(self):
        return json.loads(self.text)
#testing for invalid json response
def test_fetch_news_handles_invalid_json(mocker):
    # Mock the API to return invalid JSON
    mocker.patch('fetch_load.requests.get', return_value=MockResponse(text="invalid_json", status_code=200))
    
    # Call the lambda_handler and capture the exception
    with pytest.raises(json.JSONDecodeError):
        lambda_handler(None, None)

#Testing for timeouts
def test_fetch_news_handles_timeout(mocker):
    # Mock the API to raise a Timeout exception
    mocker.patch('fetch_load.requests.get', side_effect=Timeout)
    
    # Call the lambda_handler and capture the exception
    with pytest.raises(Timeout):
        lambda_handler(None, None)



    ''''                Testing save_article function               '''


# Test saving empty articles
def test_save_empty_articles():
    m = mock_open()
    with patch('builtins.open', m), patch('logging.warning') as mock_log:
        result = save_articles_to_file([], '2023-09-12')
        mock_log.assert_called_with('No articles to save.')
        assert result is True

# Test file name generation
def test_file_name_generation():
    m = mock_open()
    with patch('builtins.open', m):
        save_articles_to_file([{"title": "Article 1", "content": "Content 1"}], '2023-09-12')
        m.assert_called_once_with('/tmp/all_news_2023-09-12.json', 'w')

# Test logging for successful save
def test_logging_for_successful_save():
    m = mock_open()
    with patch('builtins.open', m), patch('logging.info') as mock_log:
        save_articles_to_file([{"title": "Article 1", "content": "Content 1"}], '2023-09-12')
        mock_log.assert_any_call('Successfully saved articles to /tmp/all_news_2023-09-12.json')



    '''                     Test Upload file to s3              '''

#test the s3 upload functionality
@mock_s3
def test_upload_file_to_s3():
    # Setup
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='news-etl-09-08-23')

    current_date = "2023-10-14"
    file_content = '{"key": "value"}'
    file_name = f"/tmp/all_news_{current_date}.json"
    s3_key = f"raw-data/{current_date}/all_news_{current_date}.json"

    # Create a mock file in /tmp
    with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
        with open(file_name, 'w') as f:
            f.write(file_content)

    # Call the function
    upload_file_to_s3(current_date)

    # Validate the result
    s3_client = boto3.client('s3', region_name='us-east-1')
    result = s3_client.list_objects(Bucket='news-etl-09-08-23')

    uploaded_file = result['Contents'][0]['Key']
    assert uploaded_file == s3_key


'''                         Test Lambda Handler                 '''


# Test for successful execution
def test_lambda_handler_success(mocker):
    mocker.patch('fetch_load.fetch_news', return_value=[...])  # Mocked articles
    mocker.patch('fetch_load.save_articles_to_file', return_value=True)
    mocker.patch('fetch_load.upload_file_to_s3')
    mocker.patch('fetch_load.Utils.send_notification')
    
    response = lambda_handler(None, None)
    
    assert response['statusCode'] == 200
    assert response['body'] == json.dumps('Lambda function executed successfully')

# Test for MissingSchema
def test_lambda_handler_missing_schema(mocker):
    mocker.patch('fetch_load.fetch_news', side_effect=MissingSchema)
    mock_send_notification = mocker.patch('fetch_load.Utils.send_notification')
    
    with pytest.raises(MissingSchema):
        lambda_handler(None, None)
    
    mock_send_notification.assert_called_once_with("An error occurred in the fetch_load Lambda function: ")


# Test for generic exception
def test_lambda_handler_generic_exception(mocker):
    mocker.patch('fetch_load.fetch_news', side_effect=Exception("Some error"))
    mock_send_notification = mocker.patch('fetch_load.Utils.send_notification')
    
    with pytest.raises(Exception):
        lambda_handler(None, None)
    
    mock_send_notification.assert_called_once_with("An error occurred in the fetch_load Lambda function: Some error")
