from flask import Flask, render_template, request, redirect, url_for, jsonify

import psycopg2
import os
import requests
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = os.urandom(24)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

try:
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
except psycopg2.OperationalError as e:
    print(f"Error connecting to the database: {e}")

@app.route('/')
def index():
    success = request.args.get('success')
    return render_template('index.html', success=success)

@app.route('/admin')
def admin():
    success = request.args.get('success')
    return render_template('admin.html', success=success)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('index'))

@app.route('/add_book', methods=['POST'])
def add_book():
    if 'logged_in' in session and session['logged_in']:
        book_name = request.form['book_name']
        author = request.form['author']
        description = request.form['description']
        catalog = request.form['catalog']
        rate = request.form['rate']
        image = request.files['image']

        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        try:
            url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
            files = {'photo': open(image_path, 'rb')}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': f'{book_name} by {author}'}
            response = requests.post(url, files=files, data=data)
            response_data = response.json()

            if not response_data['ok']:
                raise Exception('Failed to send photo to Telegram')

            file_id = response_data['result']['photo'][-1]['file_id']
            file_path_response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}')
            file_path_data = file_path_response.json()

            if not file_path_data['ok']:
                raise Exception('Failed to get file path from Telegram')

            file_path = file_path_data['result']['file_path']
            file_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'

            cursor = conn.cursor()
            query = "INSERT INTO bookstream (book_name, author, description, catalog, rating, img) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (book_name, author, description, catalog, rate, file_url))
            conn.commit()
            cursor.close()

            return redirect(url_for('admin', success='true'))
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return redirect(url_for('admin', success='false'))
    else:
        return redirect(url_for('index'))


@app.route('/api/books', methods=['GET'])
def get_books():
    catalog = request.args.get('catalog', 'All')
    try:
        cursor = conn.cursor()
        if catalog == 'All':
            query = "SELECT book_name, author, img, rating FROM bookstream"
            cursor.execute(query)
        else:
            query = "SELECT book_name, author, img, rating FROM bookstream WHERE catalog = %s"
            cursor.execute(query, (catalog,))
        books = cursor.fetchall()
        cursor.close()

        books_list = []
        for book in books:
            books_list.append({
                "title": book[0],
                "author": book[1],
                "image": book[2],
                "rating": book[3]
            })
        return jsonify({"books": books_list})
    except Exception as e:
        print(f"Error fetching books: {e}")
        return jsonify({"error": "Error fetching books"})





if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)





















