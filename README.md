# airflow-template
A template for streamlining airflow DAGs specifically for Google Cloud Composer environments. This template is intended to refactor airflow for more structure and readability. To use this template, create a folder specific to a DAG in the **dags/** folder within the Cloud Composer storage bucket and drop these files into it.

## config.yaml
The config.yaml file is where global variables are defined and the DAG and DAG components are configured. The majority of development occurs in this file, which reduces the amount of coding required and makes auditing the workflow much more readable:

### GLOBAL  

The **GLOBAL** section stores global parameters for the DAG that can be reused later in the config file, specifically a BigQuery project, Cloud Storage bucket and connection IDs (which must be configured within the Airflow environment: Admin -> Connections).

### DAG_PARAMS

The **DAG_PARAMS** section contains DAG-level parameters, including the DAG ID and schedule it should be run. The *start_date* parameter must be defined in the airflow.py script.

### DAG_COMPONENT_PARAMS

This section contains templates for the parameters of three airflow functions: **PostgresToGoogleCloudStorageOperator**, **GoogleCloudStorageToBigQueryOperator** and **BigQueryOperator**. The contents of these sections are used to fill DAG component parameters downstream in **airflow.py**, and should be named to reflect the specific function they are serving within the DAG. Any additional airflow functions can be added to this section.

## SQL/

In this template, SQL queries written to perform ETL either from a source system or within BigQuery are kept in separate files within the **SQL/** folder, and are extracted in **airflow.py**. Depending on the complexity of the DAG, you could have multiple subfolders within the SQL folder; for example, one folder for extracting data from a source database and another folder for performing transformations within BigQuery. However it's organized, the path to the SQL query must be specified within the appropriate DAG component in **config.yaml** for which the query is intended to run.

## airflow.py

In this template most of the heavy lifting is performed within **config.yaml** and individual SQL files, but a few things must be configured within the **airflow.py** file itself. First, at the top of the script the **DAG_BUCKET_NAME**, **DAG_FOLDER_NAME** and **DAG_START_DATE** fields must be filled in manually. After that there is some code before to automatically extract the parameters config file and the SQL queries within the SQL/ folder. Finally, the specific DAG components and the order in which they should be executed is defined in airflow.py.




