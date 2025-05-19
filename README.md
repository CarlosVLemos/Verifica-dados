# 🔐 Verifica Dados

**Projeto Flask para detecção e visualização de dados pessoais potencialmente vazados na web.**

Um sistema feito para consulta de segurança de dados, o usuario pode inserir seus dados e verificar se eles foram vazados na internete, se esses dados forem vazados em algum local que tenha sido inserido no datset. Junto a isso os dados pegos pelos sistema são colocados em um Dashboard para melhorar a visualização, ver qual o dado mais vazados, e verificar os vazamentos por meio de filtros 

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
