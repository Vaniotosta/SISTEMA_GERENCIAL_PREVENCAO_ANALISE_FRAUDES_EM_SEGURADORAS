# Sistema Gerencial de Prevenção e Análise de Fraudes em Seguradoras

<p align="center">

## 🚀 ACESSE A APLICAÇÃO ONLINE

### [CLIQUE AQUI PARA ACESSAR O SISTEMA](https://rqgbtxw7jddgpbc4gjz9mn.streamlit.app/)

**Aplicação interativa desenvolvida em Streamlit, com modelos de Machine Learning para apoiar a análise, a identificação e a priorização de possíveis fraudes em sinistros.**

</p>

---

## 1. Visão geral do projeto

O **Sistema Gerencial de Prevenção e Análise de Fraudes em Seguradoras** é uma solução analítica desenvolvida para apoiar a gestão de riscos e o processo de tomada de decisão na área de sinistros de companhias seguradoras.

A proposta é transformar dados operacionais em informações gerenciais, combinando análise de dados, indicadores de desempenho, Machine Learning e estimativas de impacto econômico.

Mais do que realizar classificações preditivas, o sistema foi concebido para oferecer uma visão integrada da operação, permitindo acompanhar indicadores, comparar modelos, identificar padrões de risco e simular cenários de possíveis fraudes.

A solução utiliza dois algoritmos de classificação:

- **Regressão Logística:** modelo estatístico utilizado como referência de desempenho e identificação de padrões associados à ocorrência de fraudes.
- **Random Forest:** algoritmo baseado em árvores de decisão, utilizado para capturar relações mais complexas entre as variáveis.

Os resultados são apresentados em uma aplicação gerencial interativa, facilitando a interpretação das informações por profissionais de dados, analistas de sinistros, equipes de prevenção a fraudes e gestores.

## 2. Objetivos estratégicos

O sistema foi desenvolvido com os seguintes objetivos:

- Apoiar a identificação de sinistros com maior probabilidade de fraude.
- Priorizar casos que merecem investigação especializada.
- Comparar o desempenho de diferentes modelos preditivos.
- Disponibilizar indicadores para acompanhamento gerencial.
- Simular previsões individuais de risco.
- Explorar possíveis impactos econômicos associados à prevenção de fraudes.
- Apoiar decisões orientadas por dados nas operações de seguradoras.

**Proposta de valor:** transformar a análise de sinistros em um processo mais analítico, estruturado e orientado por evidências, contribuindo para uma gestão de riscos mais eficiente.

## 3. Arquitetura e tecnologias utilizadas

O projeto foi desenvolvido com ferramentas utilizadas em projetos de Ciência de Dados e Machine Learning.

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem principal para desenvolvimento e análise |
| Databricks | Ambiente de desenvolvimento e treinamento dos modelos |
| Apache Spark | Ecossistema de processamento de dados disponível na plataforma Databricks |
| MLflow | Rastreamento de experimentos, métricas e gerenciamento dos artefatos dos modelos |
| Scikit-learn | Desenvolvimento e avaliação dos algoritmos |
| Pandas | Manipulação e organização dos dados |
| PyArrow | Suporte à integração e ao processamento de dados |
| Streamlit | Desenvolvimento da aplicação gerencial interativa |
| Git e GitHub | Versionamento e disponibilização do código |
| Streamlit Community Cloud | Hospedagem da aplicação online |

### Databricks: ambiente de desenvolvimento analítico

O Databricks foi utilizado como ambiente de desenvolvimento da solução de Machine Learning.

Nesse ambiente, foram conduzidas as etapas de preparação dos dados, desenvolvimento dos modelos, experimentação e avaliação dos resultados.

A utilização da plataforma permite estruturar um fluxo de trabalho de Ciência de Dados alinhado às práticas de desenvolvimento de soluções analíticas em ambientes corporativos.

### MLflow: rastreabilidade dos experimentos

O MLflow foi utilizado para acompanhar o desenvolvimento dos modelos e organizar seus resultados.

A estratégia contempla o registro e a organização de experimentos, parâmetros, métricas e artefatos produzidos durante o treinamento.

Os modelos treinados foram exportados em formato compatível com MLflow e disponibilizados na estrutura do projeto para utilização na aplicação.

Essa abordagem facilita a rastreabilidade dos experimentos e a reutilização dos modelos treinados.

## 4. Estratégia de Ciência de Dados e Machine Learning

A estratégia analítica foi organizada em etapas.

### 4.1. Preparação e análise dos dados

- Organização da base de sinistros.
- Análise das variáveis disponíveis.
- Preparação das características utilizadas pelos algoritmos.
- Estruturação da variável-alvo relacionada à ocorrência de fraude.
- Preparação dos dados para treinamento e avaliação.

### 4.2. Estratégia de validação temporal

Foi adotada uma divisão temporal dos dados, buscando aproximar a avaliação de um cenário em que modelos treinados com informações históricas são utilizados para analisar períodos posteriores.

- **Treinamento:** dados de 2023 e 2024.
- **Teste:** dados de 2025.

Essa estratégia permite avaliar a capacidade de generalização dos modelos em um período posterior ao utilizado no treinamento.

### 4.3. Desenvolvimento dos modelos

Foram desenvolvidos dois modelos:

**Regressão Logística**

Utilizada como modelo de referência, oferecendo uma abordagem estatística para estimar a probabilidade de fraude.

**Random Forest**

Utilizado para capturar padrões e interações não lineares entre as características dos sinistros.

### 4.4. Avaliação comparativa

Os modelos foram avaliados utilizando indicadores que permitem observar diferentes aspectos do desempenho preditivo:

- Acurácia (Accuracy).
- Precisão (Precision).
- Revocação (Recall).
- F1-Score.
- ROC-AUC.
- PR-AUC.

A comparação considera especialmente o contexto de classificação desbalanceada, no qual a identificação de fraudes pode ser mais importante do que simplesmente maximizar a quantidade de classificações corretas.

## 5. Resultados dos modelos

Os resultados obtidos no conjunto de teste de 2025 foram:

| Indicador | Regressão Logística | Random Forest |
|---|---:|---:|
| Acurácia | 69,24% | **77,56%** |
| Precisão | 14,32% | **17,64%** |
| Recall | **66,18%** | 58,19% |
| F1-Score | 23,55% | **27,08%** |
| ROC-AUC | **0,7631** | 0,7462 |
| PR-AUC | **0,2244** | 0,1954 |

### Interpretação gerencial

Os resultados demonstram diferenças importantes entre os modelos.

**Random Forest:**
- Apresentou maior acurácia.
- Obteve maior precisão.
- Apresentou o melhor F1-Score.
- Gerou menor quantidade de alertas em comparação à Regressão Logística.

**Regressão Logística:**
- Apresentou maior Recall.
- Obteve maior ROC-AUC.
- Apresentou maior PR-AUC.
- Identificou mais ocorrências de fraude no conjunto de teste.

Na avaliação realizada, a Regressão Logística identificou 315 casos positivos, enquanto o Random Forest identificou 277.

Por outro lado, o Random Forest apresentou 1.570 alertas, contra 2.199 da Regressão Logística.

**Conclusão:** a escolha do modelo depende da estratégia operacional da seguradora. Se a prioridade for ampliar a identificação de possíveis fraudes, o Recall assume maior importância. Se a prioridade for reduzir o volume de alertas e melhorar a precisão das sinalizações, outras métricas devem receber maior peso.

Não existe um modelo universalmente superior para todas as estratégias de prevenção.

## 6. Funcionalidades do sistema gerencial

A aplicação foi organizada em módulos para facilitar a análise e a interpretação dos resultados.

### 6.1. Visão Geral

Apresenta uma visão consolidada do cenário analisado, com indicadores e informações relevantes para acompanhamento gerencial.

### 6.2. Desempenho Preditivo

Disponibiliza indicadores de desempenho dos modelos, permitindo acompanhar as taxas de acerto e outras métricas de avaliação.

### 6.3. Comparação de Modelos

Permite comparar a Regressão Logística e o Random Forest, identificando diferenças de desempenho e características operacionais.

### 6.4. Impacto Econômico

Apresenta estimativas econômicas associadas aos cenários de prevenção e identificação de fraudes.

Os resultados devem ser interpretados como estimativas gerenciais baseadas nas premissas da simulação, e não como economia financeira efetivamente realizada.

### 6.5. Simulação e Predição Individual

Permite informar características de um sinistro e obter previsões dos modelos, apoiando a análise individual de casos.

### 6.6. Relatórios

Reúne informações e indicadores que facilitam a consulta e a interpretação dos resultados apresentados pelo sistema.

## 7. Estratégia de utilização na operação de uma seguradora

A proposta é utilizar a solução como instrumento de apoio à gestão de sinistros e prevenção a fraudes.

Um possível fluxo operacional é:

1. **Recebimento do sinistro:** registro das informações relacionadas à ocorrência.
2. **Análise de dados:** organização das características relevantes do sinistro.
3. **Predição de risco:** aplicação dos modelos de Machine Learning.
4. **Priorização:** identificação dos casos que merecem maior atenção.
5. **Investigação especializada:** avaliação dos alertas pelas equipes responsáveis.
6. **Decisão gerencial:** utilização das informações para apoiar decisões e aperfeiçoar os processos de prevenção.

O modelo não deve ser utilizado isoladamente para negar indenizações ou acusar segurados de fraude. As previsões representam sinais estatísticos de risco e devem ser submetidas à análise humana, aos procedimentos internos e às evidências disponíveis.

## 8. Estrutura do projeto

```text
prevencao_fraude_databricks/
│
├── app/
│   ├── app.py
│   └── app_inicial.py
│
├── models/
│   ├── random_forest/
│   │   ├── MLmodel
│   │   ├── model.pkl
│   │   ├── conda.yaml
│   │   └── requirements.txt
│   │
│   └── regressao_logistica/
│       ├── MLmodel
│       ├── model.pkl
│       ├── conda.yaml
│       └── requirements.txt
│
├── .gitignore
└── requirements.txt
```

## 9. Como executar localmente

### Pré-requisitos

- Python 3.12.
- Git.
- Ambiente virtual ou Anaconda.

### Clonar o repositório

```bash
git clone https://github.com/Vaniotosta/SISTEMA_GERENCIAL_PREVENCAO_ANALISE_FRAUDES_EM_SEGURADORAS.git
```

### Acessar a pasta

```bash
cd SISTEMA_GERENCIAL_PREVENCAO_ANALISE_FRAUDES_EM_SEGURADORAS
```

### Instalar as dependências

```bash
pip install -r requirements.txt
```

### Executar a aplicação

```bash
streamlit run app/app.py
```

A aplicação será disponibilizada localmente pelo Streamlit.

## 10. Possibilidades de evolução

A arquitetura e a estratégia analítica permitem evoluções futuras, como:

- Incorporação de novas variáveis de risco.
- Otimização dos limiares de classificação conforme a capacidade operacional da seguradora.
- Calibração das probabilidades preditivas.
- Monitoramento de desempenho e mudanças no perfil dos dados.
- Integração com sistemas corporativos de gestão de sinistros.
- Acompanhamento de indicadores de investigação e confirmação de fraudes.
- Avaliação de custos de investigação, perdas evitadas e retorno econômico efetivo.
- Implementação de processos de governança e versionamento de modelos.

Essas possibilidades representam caminhos de evolução, não funcionalidades já implementadas na versão atual.

## 11. Considerações finais

O projeto demonstra a aplicação integrada de Engenharia e Ciência de Dados, Machine Learning e desenvolvimento de aplicações analíticas em um contexto de negócio do setor segurador.

A principal contribuição da solução está em aproximar os resultados dos modelos preditivos das necessidades de gestão, oferecendo uma estrutura para análise de indicadores, comparação de algoritmos, identificação de riscos e apoio à tomada de decisão.

O desenvolvimento também envolveu a utilização do Databricks e do MLflow para organizar o fluxo de experimentação e treinamento, além da disponibilização dos modelos em uma aplicação interativa.

**O resultado é um Sistema Gerencial de Prevenção e Análise de Fraudes em Seguradoras, concebido para transformar dados em inteligência analítica e apoiar decisões orientadas por evidências.**

---

## 12. Acesso ao projeto

| Recurso | Link |
|---|---|
| **Aplicação online** | [Acessar o Sistema Gerencial](https://rqgbtxw7jddgpbc4gjz9mn.streamlit.app/) |
| Repositório GitHub | [Visualizar código-fonte](https://github.com/Vaniotosta/SISTEMA_GERENCIAL_PREVENCAO_ANALISE_FRAUDES_EM_SEGURADORAS) |

## 13. Referências tecnológicas

- [Databricks — Machine Learning](https://docs.databricks.com/aws/en/machine-learning/)
- [Databricks — MLflow Tracking](https://docs.databricks.com/aws/en/mlflow/tracking)
- [MLflow — Documentação oficial](https://mlflow.org/docs/latest/)
- [Scikit-learn — Documentação oficial](https://scikit-learn.org/stable/)
- [Streamlit — Documentação oficial](https://docs.streamlit.io/)

---

**Desenvolvido por Vânio Tosta**

*Ciência de Dados | Machine Learning | Análise de Dados | Inteligência de Negócios*
