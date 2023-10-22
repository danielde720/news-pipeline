from error_handler import Utils  #our error handling function
import logging
import requests
import json
import boto3
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from urllib3.exceptions import LocationValueError

# Initialize logging and environment variables
logging.basicConfig(filename='application.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")
URL = f"https://newsapi.org/v2/everything?q=canelo&apiKey={API_KEY}"
s3 = boto3.client('s3')

#function to fetch data from the api 
def fetch_news(current_date):
    all_articles = [] #Initialize a empty list 
    utils = Utils()  # Initialize Utils class
    article_count = 0 
    sent_notification = False 

    for i in range(1, 6): 
        logging.info(f"Fetching news, page {i}")  
        response = requests.get(URL) #fetching from the api
        if response.status_code == 200: #Success 
            articles = response.json().get("articles", [])
            if articles: #if not empty
                logging.info(f"Successfully fetched {len(articles)} articles.")  
                all_articles.extend(articles)
                article_count += len(articles) #incrementing our counter
            else:
                logging.warning("Received an empty list of articles from the API.")  
                if not sent_notification:
                #Slack notification with date since the function is scheduled to run once a day, we can identify which batch was empty 
                    utils.send_notification(f"Fetched an empty list of articles on {current_date}")
                    sent_notification = True
        else:
            logging.error(f"Failed to fetch news: {response.status_code}")
        
        #check to see if we reached 5 articles 
        if article_count >= 5:
            break #exits the loop

        
    return all_articles[:5] #Returns only the first 5 articles 

#function to save the data 
def save_articles_to_file(articles, current_date):
    if not articles:
        logging.warning('No articles to save.')
    file_name = f"/tmp/all_news_{current_date}.json"
    logging.info(f"Saving articles to {file_name}")  
    with open(file_name, 'w') as f:
        json.dump(articles, f)
    logging.info(f"Successfully saved articles to {file_name}")  
    return True

#function to upload to s3
def upload_file_to_s3(current_date):
    file_name = f"/tmp/all_news_{current_date}.json"
    s3_key = f"raw-data/{current_date}/all_news_{current_date}.json"
    logging.info(f"Uploading {file_name} to S3")
    s3.upload_file(
        Filename=file_name,
        Bucket='news-etl-09-08-23',
        Key=s3_key
    )
    logging.info(f"Successfully uploaded {file_name} to S3")
    
#defining the handler for lambda 
def lambda_handler(event, context):
    utils = Utils()
    try:
        logging.info("Starting Lambda function")
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        articles = fetch_news(current_date)
        file_saved = save_articles_to_file(articles, current_date)  
        if file_saved:  # Only upload if the file was saved
            upload_file_to_s3(current_date)
        
        
        logging.info("Lambda function executed successfully")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Lambda function executed successfully')
        }
    
    except LocationValueError:
        logging.error("No host specified for HTTP request.")
        utils.send_notification("No host specified for HTTP request.")
        raise

        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        utils.send_notification(f"An error occurred in the fetch_load Lambda function: {str(e)}")
        raise  # Re-raise the exception to AWS Lambda

