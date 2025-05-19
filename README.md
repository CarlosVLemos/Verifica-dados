# 🔐 Verifica Dados

**Projeto Flask para detecção e visualização de dados pessoais potencialmente vazados na web.**

Este sistema permite que o usuário insira dados como CPF, e-mail, senha ou IP para verificar possíveis vazamentos e visualizar estatísticas em um dashboard interativo e responsivo.

---

## 🧠 Funcionalidades

- ✅ Verificação de CPF, e-mail, IP e senhas.
- 🌐 Integração com a API [HaveIBeenPwned](https://haveibeenpwned.com/API).
- 📊 Dashboard com visualizações gráficas interativas usando Plotly.
- 🗂️ Histórico de buscas realizadas pelo usuário.
- 🔍 Filtros dinâmicos por data, tipo de dado e status.
- 🧱 Backend leve e modular usando Flask.

---

## 📁 Estrutura do Projeto




---

## 📁 Estrutura do Projeto


---

## 🚀 Como Rodar o Projeto

### 🔧 Pré-requisitos

- Python 3.10 ou superior
- Git instalado

---

### 🖥️ 1. Clone o repositório

```bash
git clone https://github.com/CarlosVLemos/Verifica-dados.git
cd Verifica-dados


python -m venv venv
venv\Scripts\activate


python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python run.py

http://127.0.0.1:5000/
