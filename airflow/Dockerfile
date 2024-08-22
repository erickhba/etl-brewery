FROM apache/airflow:2.10.0
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt



RUN mkdir /opt/airflow/layers
RUN mkdir /opt/airflow/layers/bronze
RUN mkdir /opt/airflow/layers/bronze/brewery
RUN mkdir /opt/airflow/layers/silver
RUN mkdir /opt/airflow/layers/silver/brewery
RUN mkdir /opt/airflow/layers/gold
RUN mkdir /opt/airflow/layers/gold/brewery



#docker run -p 8080:8080 -v /c/local/clone/path/airflow-examples/dags:/opt/airflow/dags  -d airflow-local
