import os


class Config:
    """Classe de configuração centralizada para o aplicativo."""
    
    # Configurações do banco de dados
    DATABASE_PATH = 'database.db'
    
    # Configurações do URL Shortener
    SHORT_ID_LENGTH = 6
    
    # Configurações da API de Safe Browsing
    GOOGLE_API_KEY = os.environ.get("GOOGLE_SAFE_BROWSING_API_KEY", "")
    SAFE_BROWSING_ENDPOINT = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    
    # Configurações do Flask
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Configurações de segurança
    VALIDATE_URL_FORMAT = True
    CHECK_MALICIOUS_URLS = True
