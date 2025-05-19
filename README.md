# 🔐 Verifica Dados

**Projeto Flask para detecção e visualização de dados pessoais potencialmente vazados na web.**

Este sistema permite que o usuário insira dados como CPF, e-mail, senha ou IP para verificar possíveis vazamentos e visualizar estatísticas em um dashboard interativo e responsivo.

---

## 🧠 Funcionalidades

- ✅ Verificação de CPF, e-mail, IP e senhas..
- 📊 Dashboard com visualizações gráficas interativas usando Plotly.
- 🔍 Filtros dinâmicos por data, tipo de dado e status.
- 🧱 Backend em Flask

---


## 🚀 Como Rodar o Projeto

### 🔧 Pré-requisitos

- Python 3.10 ou superior
- Git instalado

---

### 🖥️ 1. Clone o repositório

```bash
# Clona o repositório para sua máquina local
git clone https://github.com/CarlosVLemos/Verifica-dados.git

# Acessa o diretório do projeto
cd Verifica-dados


# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente virtual no Windows
venv\Scripts\activate


# Instala todas as bibliotecas necessárias listadas em requirements.txt
pip install -r requirements.txt


# Inicia o servidor Flask
python run.py

# Acesse em:
http://127.0.0.1:5000/
