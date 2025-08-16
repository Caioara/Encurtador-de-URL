import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional
from config import Config


class Database:
    """Classe responsável por todas as operações de banco de dados."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_db()
    
    def init_db(self):
        """Inicializa o banco de dados criando as tabelas necessárias."""
        conn = sqlite3.connect(self.db_path)
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
    
    def save_url(self, original_url: str, short_id: str, criador: str) -> bool:
        """
        Salva uma nova URL no banco de dados.
        
        Args:
            original_url: URL original a ser encurtada
            short_id: ID curto gerado
            criador: Nome do criador da URL
            
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        try:
            data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                "INSERT INTO urls (original_url, short_id, criador, data_criacao) VALUES (?, ?, ?, ?)",
                (original_url, short_id, criador, data)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def get_original_url(self, short_id: str) -> Optional[str]:
        """
        Busca a URL original pelo ID curto.
        
        Args:
            short_id: ID curto da URL
            
        Returns:
            str: URL original ou None se não encontrada
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT original_url FROM urls WHERE short_id = ?", (short_id,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    
    def get_all_urls(self) -> List[Tuple[str, str, str, str]]:
        """
        Retorna todas as URLs cadastradas.
        
        Returns:
            List[Tuple]: Lista de tuplas (original_url, short_id, criador, data_criacao)
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT original_url, short_id, criador, data_criacao FROM urls")
        urls = c.fetchall()
        conn.close()
        return urls
    
    def delete_url(self, short_id: str) -> bool:
        """
        Remove uma URL do banco de dados.
        
        Args:
            short_id: ID curto da URL a ser removida
            
        Returns:
            bool: True se removida com sucesso, False caso contrário
        """
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM urls WHERE short_id = ?", (short_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def short_id_exists(self, short_id: str) -> bool:
        """
        Verifica se um ID curto já existe no banco.
        
        Args:
            short_id: ID curto a ser verificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT 1 FROM urls WHERE short_id = ?", (short_id,))
        exists = c.fetchone() is not None
        conn.close()
        return exists
