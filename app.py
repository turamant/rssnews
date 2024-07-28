import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# Подключение к MongoDB
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB = os.getenv('MONGODB_DB')
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
news_collection = db['news']

@app.route('/')
def index():
    # Получение параметров пагинации и категории
    page = int(request.args.get('page', 1))
    category = request.args.get('category', 'all')
    per_page = 10

    # Получение новостей из MongoDB
    if category == 'all':
        news_items = list(news_collection.find().skip((page - 1) * per_page).limit(per_page))
    else:
        news_items = list(news_collection.find({'category': category}).skip((page - 1) * per_page).limit(per_page))

    # Получение общего количества новостей
    if category == 'all':
        total_news = news_collection.count_documents({})
    else:
        total_news = news_collection.count_documents({'category': category})

    # Вычисление количества страниц
    total_pages = (total_news + per_page - 1) // per_page

    # Получение списка категорий
    categories = news_collection.distinct('category')

    return render_template('index.html', news_items=news_items, page=page, total_pages=total_pages, categories=categories, selected_category=category)

if __name__ == '__main__':
    app.run(debug=True)
