from flask import Flask, request, redirect, render_template, url_for
import sqlite3
import string
import random
from datetime import datetime
import os
import requests

app = Flask(__name__, template_folder="templates")

DATABASE = 'database.db'

# Configure sua chave aqui (recomendado: usar variável de ambiente)
GOOGLE_API_KEY = os.environ.get("AIzaSyAL9571FYEuMjTqA298qfXhtGvA7jw9H-4", "")  # use env var
SAFE_BROWSING_ENDPOINT = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

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

def is_url_safe(url):
    """
    Consulta a Google Safe Browsing API.
    Retorna True se a URL for segura (nenhuma correspondência encontrada),
    False se a API reportar ameaça.
    Caso a API key não esteja definida, retorna True (permitir) mas registra aviso.
    """
    if not GOOGLE_API_KEY:
        # Não quebrar o fluxo em ambiente de teste — permitir, mas avisar
        print("WARN: GOOGLE_SAFE_BROWSING_API_KEY não definida — verificações de segurança desativadas.")
        return True

    payload = {
        "client": {
            "clientId": "url-shortener-interno",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    params = {"key": GOOGLE_API_KEY}
    try:
        resp = requests.post(SAFE_BROWSING_ENDPOINT, params=params, json=payload, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # Se existir a chave "matches" com conteúdo, então a URL foi identificada como ameaça
        if data and data.get("matches"):
            return False
        return True
    except requests.RequestException as e:
        # Em caso de falha na chamada (timeout, rede), optamos por:
        # - permitir o encurtamento (para não quebrar a UX interna), e logar o erro.
        # Você pode mudar esse comportamento para bloquear em produção.
        print(f"ERROR: falha ao verificar Safe Browsing API: {e}")
        return True
    except ValueError:
        # resposta não-JSON esperada
        print("ERROR: resposta inesperada da Safe Browsing API")
        return True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        criador = request.form['criador']
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Verifica segurança antes de gerar/guardar
        safe = is_url_safe(original_url)
        if not safe:
            # Retornamos uma mensagem clara com link para voltar à página inicial
            return f'''
                <h2>❌ A URL fornecida foi detectada como potencialmente maliciosa e foi bloqueada.</h2>
                <p>URL: {original_url}</p>
                <br>
                <a href="/"><button type="button">⬅ Voltar para página inicial</button></a>
            ''', 400

        short_id = generate_short_id()

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        # Garante que não exista colisão
        while c.execute("SELECT 1 FROM urls WHERE short_id = ?", (short_id,)).fetchone():
            short_id = generate_short_id()
        c.execute("INSERT INTO urls (original_url, short_id, criador, data_criacao) VALUES (?, ?, ?, ?)",
                  (original_url, short_id, criador, data))
        conn.commit()
        conn.close()

        # Exibe o resultado com botão de voltar para a página inicial
        return f'''
            <h2>✅ URL encurtada com sucesso!</h2>
            <p><a href="/{short_id}">{request.host_url}{short_id}</a></p>
            <br>
            <a href="/"><button type="button">⬅ Voltar para página inicial</button></a>
        '''

    # GET — exibe o formulário (mantive seu HTML inline como antes)
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
