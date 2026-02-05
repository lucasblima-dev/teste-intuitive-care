# Case Técnico - IntuitiveCare

Esse README contém as informações do teste técnico da IntuitiveCare. O objetivo é criar uma aplicação fullstack de visualização de dados financeiros de operadoras de saúde, processados a partir de dados abertos da ANS. É possível visualizar um gráfico resumido ou informações completas de todas as operadoras.

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

Para executar a aplicação localmente, após checar os pré-requisitos e tecnologias necessárias, siga o passo a passo abaixo:

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

9. **Configurar a URL da API no .env**
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
http://localhost:8000
```
### O frontend estára acessível em:
```bash
http://localhost:5173
```

## Trade-offs Técnicos
### Processamento em memória vs Streaming

**Decisão:** DEcidi utilizar a biblioteca `pandas` junto de um `concat`.

**Justificativa:** Levando em consideração que são apenas 3 trimestres de dados, percebi que a utilização da "in memory" fazia mais sentido pela quantidade de dados. O uso dessa abordagem me gera um código mais rápido quando converto para um vetor. Se eu tivesse usando um intervalo de tempo maior, uma opção mais adequada seria uma abordagem de streaming (arquivo por arquivo), fazendo inserção diretamente no banco, por exemplo. Isso evitaria problema com espaço de memória.

### Identificação de arquivos

**Decisão:** Iteração por diretórios e subdiretórios utilizando o `os.walk` para encontrar separadores, como: `;` ou `,` e encoding `utf-8`.

**Justificativa:** Dados governamentais geralmente não possuem padronização e isso geraria erros sem fim. Tentar inserir os nomes "hardcoded" deixaria o script frágil e propenso a erros nas atualizações ou mudanças de padrões. 

### Tratamento de Dados

**Decisão:** Conversão de vírgula para ponto e remoção de valores <= 0.

**Justificativa:** Para uma melhor análise das despesas brutas, estornos, etc., contábeis valores negativos foram desconsiderados para simplificar a visualização de "onde o dinheiro foi gasto".

### Enriquecimento de Dados (ELT)

**Decisão:** Implementação de um script dedicado `more-data.py` executado após a carga inicial, utilizando o padrão ELT (Extract, Load, Transform).

**Justificativa:** No início, os dados foram simulados porque a ideia era conseguir garantir a visualização de algo no frontend. A solução final baixa o cadastro oficial da ANS, carrega em tabela temporária e atualiza a base com SQL. 

### Modelagem de Banco de Dados

**Decisão:** Normalização das tabelas separando-as entre operadoras e despesas, e uso do tipo DECIMAL para valores monetários.

**Justificativa:** A normalização garante integridade das tabeleas e seus dados e reduz armazenamento ao não repetir strings de Razão Social em cada lançamento financeiro. O uso de DECIMAL foi devido a sua melhor performance em comparação ao FLOAT.

### Framework Backend (FastAPI)

**Decisão:** Uso do FastAPI em em relação ao Flask ou Django.

**Justificativa:** Além da performance superior por ser assíncrono nativamente, a possibilidade de gerar uma documentação (Swagger) também teve poso. Isso é uma vantagem quando pensamos no desenvolvimento de testes.

### Paginação da API
**Decisão:** Adoção de paginação baseada em Offset (page e limit).

**Justificativa:** A simplicidade de implementação da abordagem Offset é maelhor quando pensamos em usuários que gostariam de ir a uma página específica de informações.

### Frontend com Vue 3 + Tailwind

**Decisão:** Utilização de `Vue 3` e `Tailwind CSS` para estilização.

**Justificativa:** O Tailwind facilitou a construção de uma interface responsiva e moderna, principalmente quando pensamos em performance no carregamento do CSS. Já o Vue com a Composition API tem uma melhor performance e organização do código em comparação a outras. 