from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlalchemy as sa
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}")
engine = sa.create_engine(DATABASE_URL)

app = FastAPI(title="EthioMed Analytics API")

@app.get("/api/reports/top-products")
def top_products(limit: int = 10):
    # naive example: products are tokens in messages; in production use an NER table
    q = f"""
    with tokens as (
      select unnest(string_to_array(lower(text),' ')) as token from marts.fct_messages
    )
    select token, count(*) as cnt
    from tokens
    where token ~ '^[a-zA-Z0-9]+' and char_length(token)>3
    group by token order by cnt desc limit {limit}
    """
    with engine.connect() as conn:
        res = conn.execute(sa.text(q)).fetchall()
    return [{"product": r[0], "count": r[1]} for r in res]

@app.get("/api/channels/{channel_name}/activity")
def channel_activity(channel_name: str, days: int = 30):
    q = f"""
    select message_date::date as day, count(*) as cnt
    from marts.fct_messages fm
    join marts.dim_channels dc on fm.channel_id = dc.channel_id
    where dc.channel_name = :cn and message_date > now() - interval '{days} day'
    group by day order by day;
    """
    with engine.connect() as conn:
        res = conn.execute(sa.text(q), {"cn": channel_name}).fetchall()
    return [{"date": str(r[0]), "count": r[1]} for r in res]

@app.get("/api/search/messages")
def search_messages(query: str, limit: int = 50):
    q = """
    select message_id, channel_id, message_date, text from marts.fct_messages
    where text ilike :kw limit :lim
    """
    with engine.connect() as conn:
        res = conn.execute(sa.text(q), {"kw": f"%{query}%", "lim": limit}).fetchall()
    return [{"message_id":r[0],"channel_id": r[1],"message_date":str(r[2]),"text":r[3]} for r in res]
