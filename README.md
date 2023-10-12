## <p align='center'> News-pipeline Architecture </p>
<br>
<br>
<br>


![Your Diagram's Alt Text](https://github.com/danielde720/news-pipeline/assets/141448979/155872ae-0e18-469e-af6c-50c176f2d388) 


## <p align='center'> Tech Stack </p>


<p align='center'> - **EC2**: Elastic Compute Cloud for virtual servers.</p>
<p align='center'> - **S3**: Simple Storage Service for data storage.</p>
<p align='center'> - **Lambda**: Serverless compute service.</p>
<p align='center'> - **CDK**: Cloud Development Kit for infrastructure as code.</p>
<p align='center'> - **SAM**: Serverless Application Model for local testing.</p>
<p align='center'> - **Glue**: Managed ETL (Extract, Transform, Load) service.</p>
<p align='center'> - **EventBridge**: Serverless event bus for application architecture.</p>



## <p align="center"> Overview </p>

This project employs an event-driven and decoupled architecture to fetch the latest news about the boxer Canelo Alvarez, who recently had a big fight. Designed for resilience, scalability, and easy maintenance, the pipeline leverages a variety of AWS services. We use the [News API](https://newsapi.org/) as our data source, which provides a wide range of topics but comes with a 24-hour latency period. Our data storage solution involves an S3 bucket with two prefixes: one for raw data and another for transformed data. 

We've implemented two Lambda functions: `fetch_load`, which fetches data from the News API in batches and stores it in the raw data bucket, and `trigger_glue`, which transforms and loads the data into the transformed data bucket. A utility function serves as an error handler for both `fetch_load` and `trigger_glue`, enhancing the robustness of our pipeline. 

For data transformation, we use a Glue notebook to fetch data from the raw bucket, flatten it, and transform the files from JSON to Parquet format. The data is partitioned by dates for incremental loading and better organization. The pipeline is scheduled to run every 24 hours using EventBridge, which triggers the `fetch_load` Lambda function. An S3 event notification is then configured to run the Glue job whenever new data arrives in the raw bucket.


### <p align="center"> Event-Driven Architecture </p>

The pipeline is initiated by an AWS EventBridge that triggers a Lambda function (`fetch_load`) to fetch the latest news from a News API. Subsequently, an S3 event notification triggers another Lambda function to initiate a Glue job for data transformation. This event-driven approach allows each component to operate independently, making the system highly decoupled and scalable.

### <p align="center"> Decoupled Components  </p>

Each component in this pipeline is designed to be loosely coupled, allowing for greater flexibility and easier maintenance. The components react to events rather than being directly invoked, making the system more robust and easier to manage.


### <p align="center"> Monitoring Slack Notifications </p>


The pipeline is monitored using Slack notifications. If any component fails, a notification is sent immediately, enabling quick troubleshooting and resolution. We've implemented a utility function that both `fetch_load` and `trigger_glue` Lambda functions import, allowing for consistent and centralized monitoring across different components of the pipeline.


### <p align="center"> Development and Deployment </p>

- **AWS CDK**: The Lambda functions are defined and deployed using the AWS Cloud Development Kit (CDK), providing an infrastructure-as-code approach.
  
- **AWS SAM**: Before deploying, the Lambda functions are tested locally using the AWS Serverless Application Model (SAM), ensuring that they work as expected.

By combining these technologies, this pipeline offers a reliable and efficient way to stay updated on the latest news about Canelo Alvarez.


## <p align="center"> Development Challenges and Solutions </p>

### <p align="center"> Initial Struggles with AWS Lambda UI</p>

When I first  with AWS Lambda through its UI, I ran into some challenges. Debugging was a real pain , I had to delete old zip files, create new ones, and download them locally for each debugging attempt since I was on a virtual machine.Enter AWS Cloud Development Kit (CDK). CDK made everything so much more convenient, organized, and efficient. The best part? I could debug issues right then and there, without going through a maze of steps.

### <p align="center">Lambda Functions: To Multiply or Not?</p>

Another puzzle was deciding the architecture of the Lambda functions. Should I have a separate Lambda for each pipeline component, or just a few to handle everything? 

Having a Lambda for each component has its perks—better scalability, parallel execution, and easier debugging. This approach is ideal for large real world applications however for my use case it would 

### <p align="center">The Transformation Challenge</p>

During the data transformation stage, The system wanted to transform all the data in the raw S3 bucket—even the stuff that was already done in previous runs. 

I had a few options like job bookmarks and versioning, but partitioning the data by dates turned out to be the simplest and most organized fix. 

