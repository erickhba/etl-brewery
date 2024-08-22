# Brewery ETL

## Objective
This project serves as a demonstration of the ability to handle data ingestion and transformation workflows. It involves fetching data from an ## Project Overview

This project serves as a demonstration of the ability to handle data ingestion and transformation workflows. It involves fetching data from an API, processing and storing it in a data lake following the medallion architecture. This architecture includes three key layers:

- **Raw Data**: The initial layer where data is stored in csv format.
- **Curated Data**: A refined layer where the data is transformed and organized by specific attributes such as location.
- **Analytical Aggregated Data**: The final layer where data is aggregated to provide insightful metrics and summaries.

Through this project, the focus is on implementing and managing a complete ETL (Extract, Transform, Load) pipeline that adheres to best practices in data engineering.


## How to Run

### Prerequisites
- Docker
- Docker Compose

1. Clone the repository:
    ```sh
    git clone https://github.com/erickhba/etl-brewery
    ```
2. Build and run using docker:
    ```sh
    docker-compose up --build
    ```

3. Access Airflow UI at `http://localhost:8080`

4. Run the Pipeline:
    - Trigger the DAG `DAG_brewery_ingestion` to execute the ETL pipeline.

## Monitoring and Data Quality (for the future)

To ensure the reliability and performance of the pipeline, several monitoring and data quality measures are recommended:

### Monitoring Actions

1. **Error Callbacks and Alerts**:
   - Implement error callbacks to send alerts via Slack to the owner or use `sla_miss_callback` for handling missed service level agreements (SLAs).
   
2. **Airflow Features**:
   - Utilize Airflow's built-in functionalities such as `email_on_failure` and `email_on_retry` to receive notifications on task failures and retries.

3. **Retry Delays**:
   - Configure `retry_delay` to define the time interval between retry attempts, which is crucial for handling API request failures.

4. **External Monitoring Tools**:
   - Use tools like Datadog to monitor the Airflow instance for performance metrics and health checks.

### Data Quality

1. **Great Expectations**:
   - Integrate [Great Expectations](https://greatexpectations.io/) for custom data testing to ensure the integrity and accuracy of the pipeline.

2. **Explicit Data Contracts**:
   - Define and document data contracts to clearly specify the expected structure and quality of data at different stages of the pipeline.

These practices will help in maintaining the robustness and accuracy of the ETL pipeline, ensuring timely alerts and effective data quality management.

