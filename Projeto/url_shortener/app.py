from flask import Flask, request, redirect, url_for, jsonify
import os

# Importar nossas classes de responsabilidades específicas
from database import Database
from url_shortener import URLShortener
from template_renderer import TemplateRenderer
from config import Config

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Instanciar as classes de responsabilidades
db = Database()
url_shortener = URLShortener()
template_renderer = TemplateRenderer()


# Rota de API para encurtar URL e retornar JSON
@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'missing_url'}), 400
    original_url = data.get('url')
    criador = data.get('criador', 'api')

    # Usar flags de configuração se desejar
    if getattr(Config, "VALIDATE_URL_FORMAT", True):
        if not url_shortener.validate_url(original_url):
            return jsonify({'error': 'invalid_url'}), 400

    if getattr(Config, "CHECK_MALICIOUS_URLS", True):
        if not url_shortener.is_url_safe(original_url):
            return jsonify({'error': 'malicious_url'}), 400

    short_id = url_shortener.generate_unique_short_id(db.short_id_exists)

    if not db.save_url(original_url, short_id, criador):
        return jsonify({'error': 'save_error'}), 500

    return jsonify({
        'short_id': short_id,
        'short_url': request.host_url.rstrip('/') + '/' + short_id
    }), 201


# Rota API: obter informação da URL encurtada (JSON)
@app.route('/api/<short_id>', methods=['GET'])
def get_api_url(short_id):
    original_url = db.get_original_url(short_id)
    if original_url:
        return jsonify({'original_url': original_url}), 200
    return jsonify({'error': 'not_found'}), 404


# Rota API: deletar URL encurtada
@app.route('/api/<short_id>', methods=['DELETE'])
def delete_api_url(short_id):
    # Tenta deletar; retorna confirmação JSON (cliente atual espera JSON)
    success = db.delete_url(short_id)
    if success:
        return jsonify({'deleted': True, 'short_id': short_id}), 200
    return jsonify({'error': 'not_found_or_delete_failed'}), 404


# Rota API: listar URLs (opcionalmente filtrar por criador)
@app.route('/api/urls', methods=['GET'])
def get_api_urls():
    criador = request.args.get('criador')
    urls = db.get_all_urls()  # List[Tuple(original_url, short_id, criador, data_criacao)]
    result = []
    for original_url, short_id, owner, data_criacao in urls:
        if criador and owner != criador:
            continue
        result.append({
            'original_url': original_url,
            'short_id': short_id,
            'criador': owner,
            'data_criacao': data_criacao
        })
    return jsonify(result), 200


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        criador = request.form['criador']

        # Validar formato da URL
        if not url_shortener.validate_url(original_url):
            return template_renderer.render_error_message(original_url, "invalid")

        # Verificar segurança da URL
        if not url_shortener.is_url_safe(original_url):
            return template_renderer.render_error_message(original_url, "malicious")

        # Gerar ID único
        short_id = url_shortener.generate_unique_short_id(db.short_id_exists)

        # Salvar no banco de dados
        if not db.save_url(original_url, short_id, criador):
            return template_renderer.render_error_message(original_url, "save_error")

        # Retornar mensagem de sucesso
        return template_renderer.render_success_message(short_id, request.host_url)

    # GET - exibir formulário
    return template_renderer.render_home_form()

@app.route('/<short_id>')
def redirect_url(short_id):
    original_url = db.get_original_url(short_id)
    if original_url:
        return redirect(original_url)
    return template_renderer.render_not_found()

@app.route('/admin')
def admin():
    urls = db.get_all_urls()
    return template_renderer.render_admin_page(urls, request.host_url)

@app.route('/delete/<short_id>')
def delete_url(short_id):
    db.delete_url(short_id)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # O banco já é inicializado no construtor da classe Database
    app.run(debug=Config.DEBUG)
