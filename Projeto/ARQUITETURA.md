# Encurtador de URL - Documentação da Arquitetura

## Visão Geral

O projeto foi refatorado seguindo o princípio de **Separação de Responsabilidades**, dividindo o código em classes específicas para cada funcionalidade.

## Estrutura da Arquitetura

### 1. Classe `Database` (database.py)
**Responsabilidade**: Gerenciar todas as operações de banco de dados

**Métodos principais**:
- `init_db()`: Inicializa o banco de dados
- `save_url()`: Salva uma nova URL
- `get_original_url()`: Busca URL original pelo ID curto
- `get_all_urls()`: Retorna todas as URLs
- `delete_url()`: Remove uma URL
- `short_id_exists()`: Verifica se um ID já existe

### 2. Classe `URLShortener` (url_shortener.py)
**Responsabilidade**: Gerar e validar URLs encurtadas

**Métodos principais**:
- `generate_short_id()`: Gera um ID curto aleatório
- `generate_unique_short_id()`: Gera um ID curto único
- `is_url_safe()`: Verifica se a URL é segura (Google Safe Browsing)
- `validate_url()`: Valida formato básico da URL

### 3. Classe `TemplateRenderer` (template_renderer.py)
**Responsabilidade**: Gerenciar todos os templates HTML

**Métodos principais**:
- `render_home_form()`: Renderiza o formulário inicial
- `render_success_message()`: Renderiza mensagem de sucesso
- `render_error_message()`: Renderiza mensagens de erro
- `render_admin_page()`: Renderiza página de administração
- `render_not_found()`: Renderiza página de URL não encontrada

### 4. Classe `Config` (config.py)
**Responsabilidade**: Centralizar todas as configurações do sistema

**Configurações incluídas**:
- Configurações do banco de dados
- Configurações do gerador de URLs
- Configurações da API de segurança
- Configurações do Flask

### 5. Aplicação Principal (app.py)
**Responsabilidade**: Coordenar as classes e definir as rotas

**Benefícios da nova arquitetura**:
- Código mais organizad e modular
- Fácil manutenção e teste
- Reutilização de componentes
- Separação clara de responsabilidades

## Templates HTML

### Novos templates criados:
1. `home.html`: Página inicial com formulário estilizado
2. `admin.html`: Página de administração aprimorada
3. `success.html`: Mensagem de sucesso padronizada
4. `error.html`: Mensagens de erro padronizadas

## Como usar

1. Execute o arquivo principal:
```bash
python app.py
```

2. Acesse no navegador:
- Página inicial: http://localhost:5000
- Painel admin: http://localhost:5000/admin

## Configuração

As configurações podem ser ajustadas no arquivo `config.py` ou através de variáveis de ambiente:

- `GOOGLE_SAFE_BROWSING_API_KEY`: Chave da API do Google Safe Browsing
- `SECRET_KEY`: Chave secreta do Flask

## Vantagens da nova arquitetura

1. **Manutenibilidade**: Cada classe tem uma responsabilidade específica
2. **Testabilidade**: Classes podem ser testadas independentemente
3. **Escalabilidade**: Fácil adicionar novas funcionalidades
4. **Reutilização**: Componentes podem ser usados em outros projetos
5. **Legibilidade**: Código mais claro e organizado
