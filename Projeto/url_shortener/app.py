from flask import Flask, request, redirect, url_for
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
