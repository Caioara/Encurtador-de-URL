import string
import random
import requests
import os
from typing import Optional
from config import Config


class URLShortener:
    """Classe responsável por gerar e validar URLs encurtadas."""
    
    def __init__(self, length: int = None):
        self.length = length or Config.SHORT_ID_LENGTH
        self.chars = string.ascii_letters + string.digits
        
        # Configuração da API de Safe Browsing
        self.google_api_key = Config.GOOGLE_API_KEY
        self.safe_browsing_endpoint = Config.SAFE_BROWSING_ENDPOINT
    
    def generate_short_id(self) -> str:
        """
        Gera um ID curto aleatório.
        
        Returns:
            str: ID curto gerado
        """
        return ''.join(random.choice(self.chars) for _ in range(self.length))
    
    def generate_unique_short_id(self, check_exists_func) -> str:
        """
        Gera um ID curto único, verificando se já existe.
        
        Args:
            check_exists_func: Função que verifica se o ID já existe
            
        Returns:
            str: ID curto único
        """
        short_id = self.generate_short_id()
        while check_exists_func(short_id):
            short_id = self.generate_short_id()
        return short_id
    
    def is_url_safe(self, url: str) -> bool:
        """
        Consulta a Google Safe Browsing API para verificar se a URL é segura.
        
        Args:
            url: URL a ser verificada
            
        Returns:
            bool: True se a URL for segura, False se for maliciosa
        """
        if not self.google_api_key:
            # Não quebrar o fluxo em ambiente de teste
            print("WARN: GOOGLE_SAFE_BROWSING_API_KEY não definida — verificações de segurança desativadas.")
            return True

        payload = {
            "client": {
                "clientId": "url-shortener-interno",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE", 
                    "SOCIAL_ENGINEERING", 
                    "UNWANTED_SOFTWARE", 
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        params = {"key": self.google_api_key}
        
        try:
            resp = requests.post(
                self.safe_browsing_endpoint, 
                params=params, 
                json=payload, 
                timeout=5
            )
            resp.raise_for_status()
            data = resp.json()
            
            # Se existir a chave "matches" com conteúdo, então a URL foi identificada como ameaça
            if data and data.get("matches"):
                return False
            return True
            
        except requests.RequestException as e:
            # Em caso de falha na chamada, optamos por permitir o encurtamento
            print(f"ERROR: falha ao verificar Safe Browsing API: {e}")
            return True
            
        except ValueError:
            # Resposta não-JSON esperada
            print("ERROR: resposta inesperada da Safe Browsing API")
            return True
    
    def validate_url(self, url: str) -> bool:
        """
        Valida se a URL possui formato básico válido.
        
        Args:
            url: URL a ser validada
            
        Returns:
            bool: True se válida, False caso contrário
        """
        if not url:
            return False
            
        # Verificação básica de formato
        if not (url.startswith('http://') or url.startswith('https://')):
            return False
            
        return True
