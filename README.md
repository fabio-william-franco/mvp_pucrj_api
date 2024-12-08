
# Solução de Atribuição de Tarefas - API (Backend)

Este repositório contém a API do MVP de atribuição de tarefas, que resolve o problema de alocação de tarefas a trabalhadores minimizando os custos associados. A API gerencia o cadastro de trabalhadores, tarefas e custos e processa a melhor solução de atribuição com base nas especialidades dos trabalhadores e no menor custo.

**Este projeto faz parte da avaliação da pós-graduação em Engenharia de Software da PUC-Rio.**

---

## Como Funciona

1. **Entrada de Dados**:
   - **Trabalhadores**: Registrados com especialidades que definem as tarefas que podem executar.
   - **Tarefas**: Definidas com as especialidades necessárias para sua execução.
   - **Custos**: Associados aos trabalhadores para cada tarefa compatível.

2. **Processamento**:
   - Utiliza algoritmos de otimização para encontrar a melhor alocação de tarefas aos trabalhadores, garantindo:
     - Menor custo total.
     - Compatibilidade de especialidades.

3. **Retorno**:
   - Um mapa de alocações indicando qual trabalhador foi designado para cada tarefa e os custos totais.

---

## Cenário Simulado

O MVP utiliza um exemplo do setor de telecomunicações, onde tarefas como suporte técnico e atendimento ao cliente precisam ser atribuídas a trabalhadores com base em suas especialidades e custos.

---

## Como Executar a API

Será necessário ter todas as dependências Python listadas no `requirements.txt` instaladas. É recomendado utilizar um ambiente virtual como o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

### Passos para Configuração

1. Crie um ambiente virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a API:
   ```bash
   flask run --host 0.0.0.0 --port 5000
   ```

4. Acesse o sistema:
   - Status da API: [http://localhost:5000/#/](http://localhost:5000/#/)

**Nota**: Em modo de desenvolvimento, utilize o parâmetro `--reload` para reiniciar automaticamente após alterações:
```bash
flask run --host 0.0.0.0 --port 5000 --reload
```

---

## Funcionalidades da API
1. **Cadastro de Trabalhadores**: API para gerenciar trabalhadores e suas especialidades.
2. **Cadastro de Tarefas**: Endpoint para adicionar tarefas com especialidades requeridas.
3. **Cadastro de Custos**: API para associar custos a trabalhadores para tarefas específicas.
4. **Processamento de Solução**: Endpoint para processar a alocação ótima com base nos menores custos.

---

## Tecnologias Utilizadas
- Python
- Flask

---

