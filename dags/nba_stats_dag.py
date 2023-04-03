from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from nba_stats_collector.etl import NBAStatsETL


nba_stats_etl = NBAStatsETL(-1)

# Define the main function for each task
def run_store_game_day_data(task_instance, *args, **kwargs):
    keyword = task_instance.xcom_pull(key="keyword")
    nba_stats_etl.store_game_day_data(keyword)


def run_store_single_game_data(*args, **kwargs):
    nba_stats_etl.store_single_game_data()


# Define the DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 3, 23),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "nba_stats_dag",
    default_args=default_args,
    description="A DAG to retrieve and store NBA stats",
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Define the tasks
tasks = [
    PythonOperator(
        task_id=f"store_{keyword}_data",
        python_callable=run_store_game_day_data,
        op_args=[],
        op_kwargs={"keyword": keyword},
        provide_context=True,
        dag=dag,
    )
    for keyword in nba_stats_etl.game_day_data_config.keys()
]

store_single_game_data_task = PythonOperator(
    task_id="store_single_game_data",
    python_callable=run_store_single_game_data,
    dag=dag,
)

# Set task dependencies
for i in range(len(tasks) - 1):
    tasks[i] >> tasks[i + 1]
tasks[-1] >> store_single_game_data_task
