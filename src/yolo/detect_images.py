from ultralytics import YOLO
import os, glob, psycopg2, json
from dotenv import load_dotenv
load_dotenv()

MODEL = YOLO("yolov8n.pt")  # use a small model for speed
conn = psycopg2.connect(...)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS marts.fct_image_detections (
    detection_id SERIAL PRIMARY KEY,
    message_id BIGINT,
    image_path TEXT,
    detected_class TEXT,
    confidence NUMERIC,
    x_min NUMERIC,
    y_min NUMERIC,
    x_max NUMERIC,
    y_max NUMERIC,
    detected_at TIMESTAMP DEFAULT now()
);
""")
conn.commit()

for img in glob.glob("data/raw/images/*/*/*"):
    # infer message_id from filename if naming convention used
    # run detection
    res = MODEL(img)
    for r in res:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1,y1,x2,y2 = box.xyxy[0].tolist()
            cur.execute("""
            INSERT INTO marts.fct_image_detections
            (message_id, image_path, detected_class, confidence, x_min, y_min, x_max, y_max)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (None, img, str(cls), conf, x1,y1,x2,y2))
conn.commit()
