# 🌐Encurtador-de-URL🌐



## Minhas considerações 🌠
Trabalhar nesse projeto foi uma experiência incrível de aprendizado de API, principalmente porque foi o meu primeiro contato prático com a ideia de criar um encurtador de URLs funcional.Pude aprender mais sobre a integração entre Python, banco de dados SQLite, templates HTML e consumo de API externa, além de entender melhor como estruturar um projeto em camadas separadas (responsabilidades bem definidas entre módulos). Foi um desafio puxado, mas também muito divertido e gratificante.



## OBJETIVO DO DESAFIO :
Criar um serviço de encurtamento de URL que possa reduzir a URL original longa em uma URL curta, a finalidade é criar e utilizar um identificador único para a URL original e chamar o serviço de encurtador passando o identificador único gerado, redirecionar para a URL original.
Nesse sentido, o encurtador deve atender usuários comuns que necessitem gerar e utilizar poucas URLs encurtadas, talvez apenas uma, ou ainda usuários profissionais que necessitem gerar e utilizar muitas URLs encurtadas.



## O projeto possui:

✅ Organização em módulos (separação de responsabilidades);

✅ Banco de dados SQLite para guardar as URLs;

✅ Templates HTML para interação do usuário (Home, Admin, Sucesso, Erro);

✅ Integração com API externa para checagem de segurança das URLs;

✅ Capacidade de encurtar, consultar e gerenciar URLs criadas.



## 📦 Requerimentos

Flask

sqlite3 (já incluso no Python)

requests

string

random

datetime

os

(mais informações podem ser vistas no arquivo requirements.txt)



## ⚙️ Instalações necessárias

Certifique-se de ter o Python instalado.

Crie um ambiente virtual:
```
py -m venv {nome_da_venv}
.\{nome_da_venv}\Scripts\activate
```

Instale as dependências:
```
pip install -r requirements.txt
```

Comando do flask:
```
pip install Flask requests
```


## 🌐 API utilizada
A API escolhida foi a Google Safe Browsing API, que tem como função verificar se uma URL é segura ou não. Assim, ao tentar encurtar um link, o sistema consulta a API e valida se o endereço não está listado como malicioso ou perigoso. Essa integração garante que os usuários não encurtem nem compartilhem links inseguros, aumentando a confiabilidade do sistema.



## 🚀 Como rodar o projeto

Dentro da pasta principal, basta executar:
```
python url_shortener/app.py
```

Depois, acesse no navegador:
```
http://127.0.0.1:5000
```




## 🌐 Funcionalidades principais

Página inicial (home.html): onde o usuário insere a URL que deseja encurtar.

Validação via API: checa se o link é seguro antes de salvar.

Encurtamento: gera um código único e armazena no banco de dados.

Página de sucesso (success.html): exibe a URL encurtada gerada.

Página de erro (error.html): caso a URL seja inválida ou insegura.

Página de administração (admin.html): lista e gerencia as URLs já cadastradas.
