from flask import Flask, request, redirect, render_template, url_for
import sqlite3
import string
import random
from datetime import datetime
import os

app = Flask(__name__, template_folder="templates")

DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_id TEXT UNIQUE NOT NULL,
            criador TEXT NOT NULL,
            data_criacao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        criador = request.form['criador']
        short_id = generate_short_id()
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        while c.execute("SELECT 1 FROM urls WHERE short_id = ?", (short_id,)).fetchone():
            short_id = generate_short_id()
        c.execute("INSERT INTO urls (original_url, short_id, criador, data_criacao) VALUES (?, ?, ?, ?)",
                  (original_url, short_id, criador, data))
        conn.commit()
        conn.close()

        return f'URL encurtada: <a href="/{short_id}">{request.host_url}{short_id}</a>'

    return '''
        <h1>Encurtador de URL Interno</h1>
        <form method="post">
            URL: <input type="text" name="url" required><br>
            Criador: <input type="text" name="criador" required><br>
            <input type="submit" value="Encurtar">
        </form>
        <br>
        <a href="/admin">Ir para painel administrativo</a>
    '''

@app.route('/<short_id>')
def redirect_url(short_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_id = ?", (short_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return redirect(row[0])
    return 'URL não encontrada', 404

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT original_url, short_id, criador, data_criacao FROM urls")
    urls = c.fetchall()
    conn.close()
    return render_template('admin.html', urls=urls, host=request.host_url)

@app.route('/delete/<short_id>')
def delete_url(short_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM urls WHERE short_id = ?", (short_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
