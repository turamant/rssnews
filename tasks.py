from celery_app import app
from rss_parser import parse_rss_and_save
import asyncio

@app.task
def update_news():
    print("Starting update_news task...")
    asyncio.run(parse_rss_and_save())
