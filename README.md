# 🛒 Mini Market Flet

Sistema desktop de gerenciamento de vendas desenvolvido em Python utilizando o framework Flet para interface gráfica e SQLite como banco de dados local.

O projeto simula o funcionamento de um mini mercado, permitindo seleção de produtos, gerenciamento de carrinho e finalização de vendas com persistência em banco de dados.

---

## 🎯 Objetivo Acadêmico

Este projeto foi desenvolvido com o objetivo de:

- Praticar arquitetura modular em Python
- Aplicar Programação Orientada a Objetos
- Trabalhar separação de responsabilidades (views, services, components)
- Utilizar SQLite para persistência de dados
- Implementar lógica de negócio isolada da interface
- Simular fluxo real de sistema comercial

---

## 🧱 Estrutura do Projeto

MINI-MARKET-FLET/
│
├── components/ # Componentes reutilizáveis (cards, botões, navbar)
├── database/ # Configuração e acesso ao banco de dados
├── services/ # Regras de negócio (vendas, carrinho, produtos)
├── utils/ # Funções auxiliares e constantes
├── views/ # Telas da aplicação
│
├── main.py # Ponto de entrada da aplicação
├── router.py # Controle de navegação
├── mercado.db # Banco de dados SQLite
└── pyproject.toml


---

## 🔧 Funcionalidades

- Listagem de produtos
- Seleção de produtos
- Adição e remoção do carrinho
- Cálculo automático do total
- Finalização de venda
- Histórico de vendas
- Organização em múltiplas camadas

---

## 🛠 Tecnologias Utilizadas

- Python 3.x
- Flet
- SQLite
- Arquitetura modular

---

## 🧠 Conceitos Aplicados

- Separação de camadas
- Services para regra de negócio
- Componentização de interface
- Manipulação de banco relacional
- Organização orientada a domínio simples

---

## 📌 Observações

Projeto desenvolvido para fins de estudo e aprimoramento técnico.

## ⚙️ Como Executar

### 1️⃣ Clone o repositório

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio


### 2️⃣ Crie um ambiente virtual (opcional, recomendado)

python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows


### 3️⃣ Instale as dependências

pip install flet


### 4️⃣ Execute o projeto

python main.py ou flet run
