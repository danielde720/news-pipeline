## <p align='center'> News-pipeline Architecture </p>
<br>
<br>
<br>


![Your Diagram's Alt Text](https://github.com/danielde720/news-pipeline/assets/141448979/155872ae-0e18-469e-af6c-50c176f2d388) 


## <p align="center"> Overview </p>


This project is an event-driven, decoupled architecture designed to fetch the latest news about the boxer Canelo Alvarez, who recently had a significant fight. The pipeline leverages various AWS services and is built to be resilient,scalable and easily maintainable.

### Event-Driven Architecture

The pipeline is initiated by an AWS EventBridge that triggers a Lambda function (`fetch_load`) to fetch the latest news from a News API. Subsequently, an S3 event notification triggers another Lambda function to initiate a Glue job for data transformation. This event-driven approach allows each component to operate independently, making the system highly decoupled and scalable.

### Decoupled Components

Each component in this pipeline is designed to be loosely coupled, allowing for greater flexibility and easier maintenance. The components react to events rather than being directly invoked, making the system more robust and easier to manage.

### News API

The news data is sourced from a News API that provides up-to-date information about Canelo Alvarez. You can get your own API key from [News API](https://newsapi.org/).

### Monitoring with Slack Notifications

The pipeline is monitored using Slack notifications. If any component fails, a notification is sent immediately, enabling quick troubleshooting and resolution.

### Development and Deployment

- **AWS CDK**: The Lambda functions are defined and deployed using the AWS Cloud Development Kit (CDK), providing an infrastructure-as-code approach.
  
- **AWS SAM**: Before deploying, the Lambda functions are tested locally using the AWS Serverless Application Model (SAM), ensuring that they work as expected.

By combining these technologies, this pipeline offers a reliable and efficient way to stay updated on the latest news about Canelo Alvarez.

