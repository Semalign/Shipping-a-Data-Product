from dagster import job, op

@op
def scrape_telegram_data(context):
    context.log.info("scraping")
    # call scraper script or import functions
    import subprocess
    subprocess.run(["python","src/scraper/telegram_scraper.py"], check=True)
    return True

@op
def load_raw_to_postgres(context):
    context.log.info("loading raw to postgres")
    subprocess.run(["python","src/loaders/load_raw_to_postgres.py"], check=True)

@op
def run_dbt_transformations(context):
    context.log.info("running dbt")
    subprocess.run(["dbt","run"], check=True)
    subprocess.run(["dbt","test"], check=True)

@op
def run_yolo_enrichment(context):
    context.log.info("running yolo")
    subprocess.run(["python","src/yolo/detect_images.py"], check=True)

@job
def daily_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
