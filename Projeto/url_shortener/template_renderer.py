from flask import render_template
from typing import List, Tuple


class TemplateRenderer:
    """Classe responsável por renderizar templates HTML e gerar conteúdo HTML."""
    
    def __init__(self):
        pass
    
    def render_home_form(self) -> str:
        """
        Renderiza o formulário da página inicial.
        
        Returns:
            str: HTML do formulário
        """
        return render_template('home.html')
    
    def render_success_message(self, short_url: str, host_url: str) -> str:
        """
        Renderiza a mensagem de sucesso após encurtar uma URL.
        
        Args:
            short_url: URL encurtada
            host_url: URL base do host
            
        Returns:
            str: HTML da mensagem de sucesso
        """
        return render_template('success.html', short_url=short_url, host_url=host_url)
    
    def render_error_message(self, original_url: str, error_type: str = "malicious") -> Tuple[str, int]:
        """
        Renderiza mensagem de erro.
        
        Args:
            original_url: URL original que causou o erro
            error_type: Tipo do erro ("malicious", "invalid", "save_error")
            
        Returns:
            Tuple[str, int]: HTML da mensagem de erro e código HTTP
        """
        status_codes = {
            "malicious": 400,
            "invalid": 400,
            "save_error": 500,
            "not_found": 404
        }
        
        status_code = status_codes.get(error_type, 500)
        
        return render_template(
            'error.html', 
            original_url=original_url, 
            error_type=error_type
        ), status_code
    
    def render_admin_page(self, urls: List[Tuple[str, str, str, str]], host_url: str) -> str:
        """
        Renderiza a página de administração usando template.
        
        Args:
            urls: Lista de URLs com (original_url, short_id, criador, data_criacao)
            host_url: URL base do host
            
        Returns:
            str: HTML renderizado
        """
        return render_template('admin.html', urls=urls, host=host_url)
    
    def render_not_found(self) -> Tuple[str, int]:
        """
        Renderiza página de URL não encontrada.
        
        Returns:
            Tuple[str, int]: HTML da mensagem e código HTTP 404
        """
        return render_template('error.html', error_type="not_found", original_url=""), 404
