<h2>🛠️ Installation Steps:</h2>

<p>1. add google secret at secrets/google_secret.json</p>

<p>2. initialize container airflow</p>

```
run docker compose up airflow-init
```

<p>3. run using docker</p>

```
run docker compose up
```


<p>4. open http://localhost:(your_port_for_airflow) at web browser </p>


<p>4. run dags</p>

```
docker exec <your_airflow_container_name> airflow dags trigger chinook_to_google_sheet
```
