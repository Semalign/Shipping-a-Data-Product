# 📡 Telegram Product Detection & Analytics Pipeline

## 📝 Overview
This project is a **full-stack data pipeline** for extracting, enriching, and analyzing product-related content from Telegram channels.  
It covers **data engineering, analytics, and computer vision** in one workflow:

1. **Scrape** messages & media from Telegram using **Telethon**
2. Store raw JSON in a **partitioned data lake**
3. **Load** into **PostgreSQL** (raw schema)
4. **Transform** into a star schema with **dbt**
5. **Enrich** images using **YOLOv8** for object detection
6. **Serve analytics** via **FastAPI**
7. **Orchestrate** everything with **Dagster**

---

## 🛠️ Tech Stack
- **Python** (Telethon, FastAPI, Ultralytics YOLOv8, SQLAlchemy)
- **PostgreSQL** (data warehouse)
- **dbt** (transformations & testing)
- **Dagster** (orchestration)
- **Docker + docker-compose** (reproducible environment)

---

## 📂 Project Structure

2️ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Or run with Docker:

bash
Copy
Edit
docker-compose up --build
🚀 How to Run
Task 1 — Scrape Telegram
bash
Copy
Edit
python src/scrape_telegram.py \
    --channels file://channels.txt \
    --output data/raw/telegram
Downloads messages & media

Writes partitioned JSON files (data/raw/telegram/YYYY/MM/DD/)

Task 2 — Load to Postgres
bash
Copy
Edit
python src/load_to_postgres.py \
    --input data/raw/telegram \
    --schema raw
Task 2.5 — Transform with dbt
bash
Copy
Edit
cd dbt_project
dbt run
dbt test
Task 3 — YOLOv8 Enrichment
bash
Copy
Edit
python src/enrich_yolo.py \
    --input-table stg_images \
    --output-table fct_image_detections
Task 4 — Serve Analytics API
bash
Copy
Edit
uvicorn src.api.main:app --reload
Example endpoints:

/top-products?limit=10

/channel-activity?channel=example_channel

/search-messages?q=keyword

Task 5 — Orchestrate with Dagster
bash
Copy
Edit
dagster dev
Single job to scrape → load → transform → enrich → serve