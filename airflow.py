#IMPORT PACKAGES---------------------------------------------------------------
from airflow import DAG
from airflow.contrib.operators.postgres_to_gcs_operator import PostgresToGoogleCloudStorageOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.operators.dummy_operator import DummyOperator
from google.cloud import storage
from datetime import *
import yaml
#------------------------------------------------------------------------------

### FILL THESE OUT ###
DAG_BUCKET_NAME = '' #Storage bucket for Cloud Composer environment
DAG_FOLDER_NAME = '' #Sub-folder within Cloud Composer environment for DAG 
DAG_START_DATE = datetime.now() #Edit with python datetime package



#GET CONFIG--------------------------------------------------------------------
client = storage.Client()
bucket = client.get_bucket(DAG_BUCKET_NAME)
blob = bucket.get_blob('dags/{}/config.yaml'.format(DAG_FOLDER_NAME))
config = yaml.safe_load(blob.download_as_string())
#------------------------------------------------------------------------------


#GET PARAMS--------------------------------------------------------------------
dag_params = config['DAG_PARAMS']
dag_params['start_date'] = DAG_START_DATE
dag_component_params = config['DAG_COMPONENT_PARAMS']
#------------------------------------------------------------------------------


#GET SQL-----------------------------------------------------------------------
client = storage.Client()
bucket = client.get_bucket(config['GLOBAL']['dag_bucket'])
for component in dag_component_params:
    if 'sql' in dag_component_params[component]:
        dag_component_params[component]['sql'] = bucket.get_blob('dags/'+DAG_FOLDER_NAME+'/'+dag_component_params[component]['sql']).download_as_text()
#------------------------------------------------------------------------------


#CONFIGURE DAG-----------------------------------------------------------------
#An example DAG that loads data from an external PostgreSQL database to Cloud Storage,
#then processes the data in BigQuery
with DAG(**dag_params) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    postgres_to_gcs = PostgresToGoogleCloudStorageOperator(
        **dag_component_params['POSTGRES_TO_GCS']
        )

    gcs_to_bigquery = GoogleCloudStorageToBigQueryOperator(
        **dag_component_params['GCS_TO_BQ']
        )

    bigquery_to_bigquery = BigQueryOperator(
        **dag_component_params['BQ_TO_BQ']
    )
    

#CONFIGURE DAG DEPENDENCIES-----------------------------------------------------
start >> postgres_to_gcs >> gcs_to_bigquery >> bigquery_to_bigquery >> end



