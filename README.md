## Case Técnico - Intuitive Care

Esse README contém as informações do teste técnico da Intuitive Care. O objetivo é criar um backend que conversa com a API pública do *Dados Aberto*. Essa parte demonstra o setup de configuração de ambiente e execução de acesso com os arquivos *PDF's* e *CSV*

### Setup Inicial

Requisitos:
- **Docker** 
- **Python 3.10 ou superior**

## Fase 1: TESTE DE INTEGRAÇÃO COM API PÚBLICA

Essa parte do projeto está ligada a construção inicial do script Python que conversa com a API pública, baixa os dados zipados e os organiza. Em seguida, padroniza todos eles para serem armazenados futuramente no banco de dados. O banco, por sua vez, está construído com o *Docker* para criar uma imagem usando o *Postgres*. 

### Execução
Para testar o download e processar os dados da ANS, siga os passos abaixo:
1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:lucasblima-dev/teste-intuitive-care.git
    ```
2.  **Criar e ativar ambiente virtual:**
    ```bash
    cd backend
    python -m venv venv
    
    # Ativar ambiente virtual (Windows):

    venv\Scripts\activate
    
    # Ativar ambiente virtual (Linux):
    source venv/bin/activate
    ```
3 **Instalar as dependÊncias**
  ```bash
  pip install -r requirements.txt
  ```
4 **Subir o container no Docker**
  ```bash
  docker-compose up -d
  ```
5 **Executar a aplicação**
  ```bash
  python src/etl/process.py
  ```
O resultado deve estar em `data/processed/consolidado_despesas.zip`. O diretório *raw* contém os arquivos originais.

#### Trade-offs Técnicos (Parte 1)
**Processamento em memória vs Streaming**

*Decisão:* DEcidi utilizar a biblioteca `pandas` junto de um `concat`.

*Justificativa:* Levando em consideração que são apenas 3 trimestres de dados, percebi que a utilização da "in memory" fazia mais sentido pela quantidade de dados. O uso dessa abordagem me gera um código mais rápido quando converto para um vetor. Se eu tivesse usando um intervalo de tempo maior, uma opção mais adequada seria uma abordagem de streaming (arquivo por arquivo), fazendo inserção diretamente no banco, por exemplo. Isso evitaria problema com espaço de memória.

**Identificação de arquivos**

*Decisão:* Iteração por diretórios e subdiretórios utilizando o `os.walk` para encontrar separadores, como: `;` ou `,` e encoding `utf-8`.

*Justificativa:* Dados governamentais geralmente não possuem padronização e isso geraria erros sem fim. Tentar inserir os nomes "hardcoded" deixaria o script frágil e propenso a erros nas atualizações ou mudanças de padrões. 

**Tratamento de Dados**

*Decisão:* Conversão de vírgula para ponto e remoção de valores <= 0.

*Justificativa:* Para uma melhor análise das despesas brutas, estornos, etc., contábeis valores negativos foram desconsiderados para simplificar a visualização de "onde o dinheiro foi gasto".