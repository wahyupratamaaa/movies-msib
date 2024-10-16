import os
from os.path import join, dirname
from dotenv import load_dotenv
from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

try:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    MONGODB_URL = os.getenv("MONGODB_URL")
    DB_NAME = os.getenv("DB_NAME")

    # env sambungan (perbaikan di sini)
    client = MongoClient(MONGODB_URL) 
    db = client[DB_NAME] 

    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route("/movie", methods=["POST"])
    def movie_post():
        url_receive = request.form['url_give']
        star_receive = request.form['star_give']
        comment_receive = request.form['comment_give']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        data = requests.get(url_receive, headers=headers)

        soup = BeautifulSoup(data.text, 'html.parser')

        og_image = soup.select_one('meta[property="og:image"]')
        og_title = soup.select_one('meta[property="og:title"]')
        og_description = soup.select_one('meta[name="description"]')

        image = og_image['content']
        title = og_title['content']
        desc = og_description['content']
        doc = {
            'image': image,
            'title': title,
            'desc': desc,
            'star': star_receive,
            'comment': comment_receive
        }
        db.movies.insert_one(doc)

        return jsonify({'msg': 'POST request!'})

    @app.route("/movie", methods=["GET"])
    def movie_get():
        movie_list = list(db.movies.find({}, {'_id': False}))
        return jsonify({'movies': movie_list})

    if __name__ == '__main__':
        app.run('0.0.0.0', port=4000, debug=True)

except Exception as e:  
    print(f"Error: {e}")  



# blinker==1.4
# click==7.1.2
# dnspython==1.16.0  # Versi yang sesuai dengan Python 2.7
# Flask==1.1.4
# importlib_metadata==1.6.0
# itsdangerous==1.1.0
# Jinja2==2.11.3
# MarkupSafe==1.1.1
# pymongo==3.11.4
# python-dotenv==0.17.0
# Werkzeug==1.0.1
# zipp==1.2.0  # Ganti dengan versi yang kompatibel, versi 1.2.0 untuk Python 2.7
#!/bin/bash

# # Activate your virtual environment if necessary
# source /path/to/your/venv/bin/activate

# # Run your Flask application
# python3 app.py

#!/bin/bash
# pip install -r requirements.txt
# python app.py
