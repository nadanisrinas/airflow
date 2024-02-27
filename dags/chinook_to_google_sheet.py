from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.providers.google.suite.transfers.sql_to_sheets import SQLToGoogleSheetsOperator
from datetime import datetime
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG('chinook_to_google_sheet', 
         default_args=default_args, 
         schedule_interval='@once', 
         catchup=False,
        #  template_searchpath='/Users/nadanisrinaseptiana/belajar/dibimbing/dibimbing-airflow/dags/templates'
         ) as dag:
    sql_query = """ 
    SELECT 
        t.id AS TrackId,
        t.name AS Track,
        a.title AS AlbumName,
        ar.name AS ArtistName,
        -- Assuming MediaType and Genre tables are linked with appropriate foreign keys in the tracks table
        t.media_type_id AS MediaType,
        t.genre_id AS GenreId,
        t.composer AS Composer,
        t.milliseconds AS Milliseconds,
        t.bytes AS Bytes,
        t.unit_price AS UnitPrice,
        -- Additional columns for calculated duration in minutes, if needed
        t.milliseconds / 60000.0 AS DurationMinutes,
        -- Additional columns for etl_timestamp and StudentName if needed
        -- Assuming these columns exist in the tracks table
        CURRENT_TIME,
        -- Assuming StudentName is a column in the tracks table
        'dataonlytrue'
    FROM 
        tracks t
    LEFT JOIN 
        albums a ON t.album_id = a.id
    LEFT JOIN 
        artists ar ON a.artist_id = ar.id;
            """
   
    # Task to export data to Google Sheets
    export_to_sheets_task = SQLToGoogleSheetsOperator(
        task_id='export_to_sheets_task',
        sql=sql_query,
        spreadsheet_range='Staging!A41',  
        sql_conn_id='dibimbing_assignment_12',
        spreadsheet_id='1CDqjVawY8aKLQD6ycQoQ6mUQ4TSbdrO5lh6MuxdaLhQ',
        gcp_conn_id='google_cloud_conn',
        # data_only=True
    )

    # export to sheet
    export_to_sheets_task