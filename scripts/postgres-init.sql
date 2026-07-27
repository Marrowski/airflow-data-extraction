-- Create metadata database user and database
CREATE USER airflow_meta_user WITH PASSWORD 'VNXkgKEPBn69yYwA';
CREATE DATABASE airflow_metadata_db OWNER airflow_meta_user;

-- Create celery results database user and database
CREATE USER celery_user WITH PASSWORD 'L4PYpRNq6mxSQfyj';
CREATE DATABASE celery_results_db OWNER celery_user;
