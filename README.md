## <p align='center'> News-pipeline Project </p>
<br>
<br>
<br>

<div align="center">
  <img src="https://github.com/danielde720/news-pipeline/assets/141448979/c7bde838-3efc-4ca4-9287-89f3bdad818e" alt="model">
</div>





## <p align='center'> Tech Stack </p>


<p align='center'> - EC2</p>
<p align='center'> - S3</p>
<p align='center'> - Lambda</p>
<p align='center'> - CDK</p>
<p align='center'> - SAM</p>
<p align='center'> - Glue</p>
<p align='center'> - EventBridge</p>
<p align='center'> - Redshift</p>



## <p align="center"> Overview </p>

This project employs an event-driven and decoupled architecture to fetch the latest news about the boxer Canelo Alvarez, who recently had a big fight. Designed for resilience, scalability, and easy maintenance, the pipeline leverages a variety of AWS services. We use the [News API](https://newsapi.org/) as our data source, which provides a wide range of topics but comes with a 24-hour latency period. Our data storage solution involves an s3 bucket for data coming in and redshift to store our transformed data. 

We've implemented two Lambda functions: `fetch_load`, which fetches data from the News API in batches and stores it in s3, and `trigger_glue`,which triggers a glue job that transforms and loads the data into redshift. A utility function serves as an error handler for both `fetch_load` and `trigger_glue`, enhancing the robustness of our pipeline. 

For data transformation, we use a Glue notebook to fetch the latest news data from the s3 bucket, we do this by . The incoming data has a semi-structured format, and the schema is represented in the table below.
<br>
<br>
<br>
<div align="center">
  <img src="https://github.com/danielde720/news-pipeline/assets/141448979/1cb364f2-d904-492f-920c-b1ed0f0f9a8e" alt="model">
</div>
<br>
<br>
<br>


For data transformation, we utilize an AWS Glue notebook to fetch the latest news data stored in our S3 bucket. To ensure efficient and accurate processing, we employ a date-based batch system. The incoming data is saved in the S3 bucket and partitioned by date, allowing us to manage it more effectively.

We leverage Python's datetime module within the Glue notebook to dynamically generate today's date. This enables the Glue job to selectively fetch only the data corresponding to the current date, thereby avoiding any issues related to incremental loading. By doing so, we ensure that each Glue job processes only the most recent, relevant data, eliminating the need to sift through older records.


Certainly! Here's a refined version of your explanation that elaborates on the normalization process and its benefits:

Following the data retrieval, we proceed to transform the semi-structured news data into a normalized form. Specifically, we aim to achieve Fifth Normal Form (5NF) to ensure the highest level of data integrity and efficiency. In this process, we create multiple tables, each designed so that every column is an attribute solely of its primary key.

We start by isolating the columns with multiple values, such as the 'source' column, and restructure them into atomic units. This ensures that each table represents a unique entity and eliminates any multi-valued attributes.

By achieving 5NF, we eliminate any transitive dependencies and ensure that there is no data redundancy. This results in a schema where each piece of information is stored in its most logical location.

Below is the Entity-Relationship Diagram (ERD) that visually represents this normalized schema.  
<br>
<br>
<br>











The pipeline is scheduled to run every 24 hours using EventBridge, which triggers the `fetch_load` Lambda function. An S3 event notification is then configured to run the Glue job whenever new data arrives in the raw bucket.



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

When I started using AWS Lambda through its UI, I ran into some challenges. Debugging was a real pain , I had to delete old zip files, create new ones, and download them locally in order to upload it to lambda for each debugging attempt since I was on a virtual machine.Enter AWS Cloud Development Kit (CDK). CDK made everything so much more convenient, organized, and efficient. The best part? I could debug issues right then and there, without going through a maze of steps.

### <p align="center">Lambda Functions: To Multiply or Not?</p>

Another puzzle was deciding the architecture of the Lambda functions. Should I have a separate Lambda for each pipeline component, or just a few to handle everything? 

Having a Lambda for each component has its perks,better scalability, parallel execution, and easier debugging. This approach is ideal for large real world applications however for my use case going with fewer lambdas accomplishes the same thing with fewer resources needed. 

### <p align="center">The Transformation Challenge</p>

During the data transformation stage, The system wanted to transform all the data in the raw S3 bucket—even the stuff that was already done in previous runs. 

I had a few options like job bookmarks and versioning, but partitioning the data by dates turned out to be the simplest and most organized fix. 

