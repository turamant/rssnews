import os
import asyncio
import feedparser
import aiohttp
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Подключение к MongoDB
# Подключение к MongoDB
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB = os.getenv('MONGODB_DB')
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
news_collection = db['news']
metadata_collection = db['metadata']  # Коллекция для хранения метаданных

# Список RSS-лент
rss_urls = [
    'https://www.vedomosti.ru/rss/rubric/politics',
    'https://www.vedomosti.ru/rss/rubric/politics/official',
    'https://www.vedomosti.ru/rss/rubric/politics/democracy',
    'https://www.vedomosti.ru/rss/rubric/politics/international',
    'https://www.vedomosti.ru/rss/rubric/politics/security_law',
    'https://www.vedomosti.ru/rss/rubric/politics/social',
    'https://www.vedomosti.ru/rss/rubric/politics/foreign'
]

async def fetch_feed(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_rss_and_save():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for rss_url in rss_urls:
            tasks.append(fetch_feed(session, rss_url))
        
        responses = await asyncio.gather(*tasks)

        # Получаем время последнего парсинга
        last_parsed_time = get_last_parsed_time()

        for rss_url, response in zip(rss_urls, responses):
            feed = feedparser.parse(response)
            category = rss_url.split('/')[-1]  # Получаем категорию из URL
            for entry in feed.entries:
                published_time = datetime(*entry.published_parsed[:6])  # Преобразуем в datetime

                # Проверяем, если новость была опубликована после последнего парсинга
                if published_time > last_parsed_time:
                    news_data = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published,
                        'category': category  # Добавляем категорию
                    }
                    try:
                        news_collection.insert_one(news_data)
                    except Exception as e:
                        print(f"Error inserting data: {e}")

            # Обновляем время последнего парсинга
            update_last_parsed_time(datetime.now())

def get_last_parsed_time():
    metadata = metadata_collection.find_one({'_id': 'last_parsed_time'})
    if metadata:
        return metadata['last_parsed']
    return datetime.min  # Если нет данных, возвращаем минимальное время

def update_last_parsed_time(last_parsed):
    metadata_collection.update_one(
        {'_id': 'last_parsed_time'},
        {'$set': {'last_parsed': last_parsed}},
        upsert=True
    )

if __name__ == "__main__":
    asyncio.run(parse_rss_and_save())