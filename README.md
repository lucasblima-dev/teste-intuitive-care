# Case Técnico - Intuitive Care

Esse README contém as informações do teste técnico da Intuitive Care. O objetivo é criar uma aplicação fullstack de visualização de dados financeiros de operadoras de saúde, processados a partir de dados abertos da ANS. É possível visualizar um gráfico resumido ou informações completas de todas as operadoras.

## Setup Inicial

### Tecnologias utilizadas:
- **Frontend:** Vue.js 3, TypeScript, Tailwind CSS, Vite, Chart.js.
- **Backend:** Python 3.10+, FastAPI, SQLAlchemy, Pydantic.
- **Banco de Dados:** PostgreSQL 15 (Docker).
- **Infraestrutura:** Docker Compose.

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+
- Node.js 22+

## Executar a Aplicação

Para executar a aplicação localmente, após checar os pré-requesitos e tecnologias necessárias, siga o passo a passo abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:lucasblima-dev/teste-intuitive-care.git
    ```

### Após isso, iremos começar pelo backend + banco

2.  **Criar e ativar ambiente virtual:**
    ```bash
    cd ./backend
    python -m venv venv

    # Ativar ambiente virtual (Windows):

    venv\Scripts\activate

    # Ativar ambiente virtual (Linux):
    source venv/bin/activate
    ```
    
3. **Instalar as dependÊncias**
    ```bash
    pip install -r requirements.txt
    ```

4. **Ajustar o *.env* do backend**
    ```bash
    # ALTERE AS INFORMAÇÕES COMO QUISER
    POSTGRES_USER=seu-user
    POSTGRES_PASSWORD=sua-senha
    POSTGRES_DB=nome-do-banco
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    ```

5. **Subir o container no Docker**
    ```bash
    docker-compose up -d
    ```

6. **Rodar script de download e persistência**
    ```bash
    python activate.py
    ```

7. **Iniciar o backend**
    ```bash
    uvicorn src.api.main:app --reload
    ```

### Com o backend e banco estruturados, retornar ao frontend e inicia-lo:

8. **Acessar o front**
    ```bash
    cd ../frontend
    ```

9 **COnfigurar a URL da API no .env**
```bash
# A PORTA GERALMENTE É 8000
VITE_API_URL=http://localhost:PORTA_DO_BACKEND/api
```

10. **Instale as dependências**
    ```bash
    npm install
    ```

11. **Execute o frontend**
    ```bash
    npm run dev
    ```
## 
### O backend estará rodando em: 
```bash
http://localhost:8000**
```
### O frontend estára acessível em:
```bash
http://localhost:5173
``