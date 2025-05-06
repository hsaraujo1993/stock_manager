# 📦 Stock Manager

![Status](https://img.shields.io/badge/status-produção-brightgreen)

Sistema de gerenciamento de estoque desenvolvido com Django.

## 🧾 Visão Geral

O Stock Manager é uma aplicação web para controle de estoque, permitindo o gerenciamento de produtos, categorias, preços, vendas e itens de venda.

## 🛠️ Tecnologias Utilizadas

- Python (Django)
- JavaScript
- CSS

## ⚙️ Instalação

### Pré-requisitos

- Python 3.x
- pip
- Virtualenv (opcional)

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/hsaraujo1993/stock_manager.git
   cd stock_manager
2. Crie e ative um ambiente virtual (opcional):
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   
3. Instale as dependências:
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

4. Aplique as migrações:
   python manage.py migrate

5. Crie um superusuário:
   python manage.py createsuperuser

6. Inicie o servidor de desenvolvimento:
   python manage.py runserver

7. Acesse a aplicação:
   - Admin: http://localhost:8000/admin
  
Estrutura do Projeto
O projeto está dividido em várias apps:

- categories/
- core/
- prices/
- products/
- sales/
- sales_items/
- stocks/
- static/
- staticfiles/
- manage.py
- requeriments.txt

📝 Observações
- Certifique-se de que todas as dependências estejam corretamente instaladas.
