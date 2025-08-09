# src/loaders/load_raw_to_postgres.py
import os, glob, json, psycopg2
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST","db"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT", 5432)
)
cur = conn.cursor()
cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    message_date TIMESTAMP,
    text TEXT,
    media_path TEXT,
    raw_json JSONB,
    ingested_at TIMESTAMP DEFAULT now()
);
""")
conn.commit()

def ingest_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as fh:
        for line in fh:
            rec = json.loads(line)
            try:
                cur.execute("""
                    INSERT INTO raw.telegram_messages (message_id, channel_name, message_date, text, media_path, raw_json)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (message_id) DO NOTHING
                """, (
                    rec.get("id"),
                    os.path.basename(filepath).replace(".jsonl", ""),
                    rec.get("date"),
                    rec.get("text"),
                    rec.get("media"),
                    json.dumps(rec.get("raw"))
                ))
            except Exception as e:
                print("error", e)
    conn.commit()

for path in glob.glob("data/raw/telegram_messages/*/*.jsonl"):
    ingest_file(path)
