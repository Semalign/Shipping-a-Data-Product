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


