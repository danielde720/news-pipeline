## <p align='center'> News-pipeline Project </p>
<br>
<br>
<br>

<div align="center">
  <img src="https://github.com/danielde720/news-pipeline/assets/141448979/0054a735-b023-47cf-ab20-5ac965119f46)" alt="model">
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
<br>
<br>



## <p align="center"> Overview </p>

This project employs an event-driven and decoupled architecture to fetch the latest news about the boxer Canelo Alvarez, who recently had a big fight. Designed for resilience, scalability, and easy maintenance, the pipeline leverages a variety of AWS services. We use the [News API](https://newsapi.org/) as our data source, which provides a wide range of topics but comes with a 24-hour latency period. Our data storage solution involves an s3 bucket for data coming in and redshift to store our transformed data. 

We've implemented two Lambda functions: `fetch_load`, which fetches data from the News API in batches and stores it in s3, and `trigger_glue`,which triggers a glue job that transforms and loads the data into redshift. A utility function serves as an error handler for both `fetch_load` and `trigger_glue`, enhancing the robustness of our pipeline. The incoming data has a semi-structured format, and the schema is represented in the table below.
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


Following the data retrieval, we proceed to transform the semi-structured news data into a normalized form. Specifically, we aim to achieve Fifth Normal Form (5NF) to ensure the highest level of data integrity and efficiency. In this process, we create multiple tables, each designed so that every column is an attribute solely of its primary key.

We start by isolating the columns with multiple values, such as the 'source' column, and restructure them into atomic units. This ensures that each table represents a unique entity and eliminates any multi-valued attributes.

By achieving 5NF, we eliminate any dependencies and ensure that there is no data redundancy. This results in a schema where each piece of information is stored in its most logical location.

Below is the Entity-Relationship Diagram (ERD) that visually represents this normalized schema.  

<br>
<br>
<br>
<div align="center">
  <img src="https://github.com/danielde720/news-pipeline/assets/141448979/cd04338c-4c5b-4a41-bf06-20dcb523a939" alt="model">
</div>
<br>
<br>
<br>


## <p align="center"> Entity-Relationship Diagram (ERD) Explanation </p>

As shown in the ERD above, we have established one-to-many relationships for both `source_id` and `author_id`. This means that a single source can be associated with multiple articles, and similarly, a single author can write multiple articles.

By structuring the data this way, we achieve several key benefits:

1. **Elimination of Redundancy**:  
   Storing the source and author information in their respective tables and referencing them via foreign keys in the `Article` table eliminates the need to repeat this information for each article, thereby reducing data redundancy.

2. **Data Integrity**:  
   Using unique identifiers (`source_id` and `author_id`) as foreign keys ensures that any updates to a source or an author's details only need to be made in one place. This maintains data consistency across the database.

3. **Query Efficiency**:  
   The one-to-many relationships enable more efficient queries. For example, if you want to find all articles from a particular source or by a specific author, you can easily do so without scanning through the entire `Article` table.

4. **Scalability**:  
   This normalized structure is easier to scale, as adding new articles, sources, or authors involves inserting new records without the need to modify existing ones.

By adhering to these normalization principles, we create a robust and scalable database schema that is well-suited for transactional operations.
<br>
<br>


### <p align="center"> Event-Driven Architecture </p>

The pipeline is initiated by an AWS EventBridge that triggers a Lambda function (`fetch_load`) to fetch the latest news from a News API. Subsequently, an S3 event notification triggers another Lambda function to initiate a Glue job for data transformation. This event-driven approach allows each component to operate independently, making the system highly decoupled and scalable.
Each component in this pipeline is designed to be loosely coupled, allowing for greater flexibility and easier maintenance. The components react to events rather than being directly invoked, making the system more robust and easier to manage.

<br>
<br>

### <p align="center"> Monitoring Slack Notifications </p>


The pipeline is monitored using Slack notifications. If any component fails, a notification is sent immediately, enabling quick troubleshooting and resolution. We've implemented a utility function that both `fetch_load` and `trigger_glue` Lambda functions import, allowing for consistent and centralized monitoring across different components of the pipeline.

<br>
<br>

### <p align="center"> Development and Deployment </p>

- **AWS CDK**: The Lambda functions are defined and deployed using the AWS Cloud Development Kit (CDK), providing an infrastructure-as-code approach.
  
- **AWS SAM**: Before deploying, the Lambda functions are tested locally using the AWS Serverless Application Model (SAM), ensuring that they work as expected.

By combining these technologies, this pipeline offers a reliable and efficient way to stay updated on the latest news about Canelo Alvarez.


<br>
<br>

## <p align="center"> Testing </p> 
We have implemented unit tests for each Lambda function to ensure that they work as expected. These tests cover various scenarios and edge cases to validate the functionality and reliability of our code. In addition to unit tests, we've also incorporated data validation checks into our pipeline. These checks are designed to handle missing data and identify anomalies, ensuring that the data processed by our Lambdas is both accurate and reliable. By combining unit tests with data validation checks, this pipeline aims to create a robust and fault-tolerant system.
![Screenshot 2023-10-22 at 1 13 54 AM](https://github.com/danielde720/news-pipeline/assets/141448979/51660f6a-cdeb-4d57-959b-c2780de5870a)

<br>
<br>


## <p align="center">Development Challenges and Solutions</p>

<p align="justify">

When I initially started using AWS Lambda via its UI, debugging was very time consuming. The process involved deleting old zip files, creating new ones, and downloading them locally for each debugging attempt since I was operating on a virtual machine and not locally. This is where AWS Cloud Development Kit (CDK) came to the rescue, streamlining the entire process and allowing for immediate debugging.

The architecture of Lambda functions posed another challenge. Whether to have a separate Lambda for each pipeline component or use less lambdas and have each running multiple components. While having individual Lambdas offers advantages like better scalability, parallel execution, and easier debugging, ideal for large-scale applications, in my specific use case since this is a pretty small application and is not that complex, I went with fewer Lambdas to be more resource efficent.

Lastly, during the data transformation stage, the system was initially set to transform all the data in the raw S3 bucket, including previously processed data. Although options like job bookmarks and versioning were available, partitioning the data by dates emerged as the most straightforward and organized solution.

</p>


