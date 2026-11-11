# Arquitetura Tecnológica e Integração dos Componentes

## 1. Introdução

A arquitetura tecnológica define a organização dos componentes responsáveis pelo processamento dos dados, treinamento e disponibilização dos modelos preditivos, apresentação dos resultados e manutenção da solução.

Em projetos de Machine Learning aplicados à prevenção de fraudes em seguradoras, a arquitetura precisa atender a requisitos de:

- Reprodutibilidade;
- Escalabilidade;
- Rastreabilidade;
- Segurança;
- Manutenibilidade;
- Integração entre componentes;
- Governança dos dados;
- Confiabilidade das previsões.

Este capítulo apresenta a arquitetura identificada na implementação atual, a função de cada tecnologia e uma proposta de evolução para uma estrutura corporativa baseada em Databricks.

É importante distinguir os componentes efetivamente identificados no projeto daqueles que fazem parte do planejamento arquitetural.

## 2. Visão geral da arquitetura atual

A implementação disponibiliza uma aplicação gerencial construída com Streamlit, responsável por carregar modelos previamente serializados e apresentar resultados de análise e classificação.

Os principais componentes identificados são:

| Componente | Tecnologia | Responsabilidade |
|---|---|---|
| Linguagem principal | Python | Desenvolvimento da solução |
| Manipulação de dados | Pandas | Organização e transformação de dados |
| Modelos preditivos | Scikit-learn | Algoritmos de classificação |
| Gestão de artefatos | MLflow | Formato e carregamento dos modelos |
| Interface gerencial | Streamlit | Apresentação dos indicadores |
| Controle de versão | Git | Histórico de alterações |
| Repositório remoto | GitHub | Armazenamento e compartilhamento do código |
| Hospedagem da aplicação | Streamlit Community Cloud | Disponibilização da interface |

A arquitetura atual prioriza a disponibilização dos modelos e a apresentação de informações em uma interface acessível.

O repositório organiza os componentes da aplicação, os modelos serializados, os arquivos de configuração e a documentação técnica.

## 3. Organização lógica do projeto

A estrutura identificada no repositório é organizada da seguinte forma:

```text
prevencao_fraude_databricks/
│
├── .gitignore
├── requirements.txt
│
├── app/
│   ├── app.py
│   └── app_inicial.py
│
├── docs/
│   ├── 00_visao_geral.md
│   ├── 01_problema_negocio.md
│   ├── 02_dados_e_variaveis.md
│   ├── 03_analise_exploratoria.md
│   ├── 04_preprocessamento.md
│   ├── 05_modelagem.md
│   ├── 06_avaliacao_estatistica.md
│   ├── 07_analise_economico_financeira.md
│   ├── 08_interpretacao_gerencial_graficos.md
│   └── 09_validacao_temporal_monitoramento_drift.md
│
├── models/
│   ├── regressao_logistica/
│   └── random_forest/
│
└── reports/
```

A estrutura demonstra uma separação entre interface, modelos, documentação e relatórios.

Essa organização facilita a manutenção do código e a evolução gradual da solução.

A pasta `reports` está reservada para relatórios e evidências analíticas que poderão ser produzidos posteriormente.

## 4. Python como linguagem central

Python é a linguagem utilizada para desenvolver a solução.

Sua utilização permite integrar diferentes etapas do ciclo de Machine Learning:

1. Manipulação dos dados;
2. Preparação das variáveis;
3. Construção de modelos;
4. Avaliação estatística;
5. Serialização dos artefatos;
6. Disponibilização das previsões;
7. Construção da interface gerencial.

A linguagem possui um ecossistema amplo de bibliotecas para ciência de dados, aprendizado de máquina e desenvolvimento de aplicações.

Sua flexibilidade facilita a integração futura com plataformas de processamento distribuído e serviços corporativos.

## 5. Pandas: manipulação e análise dos dados

A biblioteca Pandas é utilizada para operações tabulares.

Sua principal estrutura, o DataFrame, permite organizar observações em linhas e variáveis em colunas.

Entre as operações que podem compor o fluxo analítico estão:

- Leitura de arquivos;
- Seleção de variáveis;
- Filtragem de registros;
- Tratamento de dados;
- Agregações;
- Cálculos estatísticos;
- Construção de tabelas;
- Preparação de informações para visualização.

No contexto da prevenção de fraudes, o Pandas permite trabalhar com informações cadastrais, contratuais, financeiras e relacionadas aos sinistros.

A implementação atual utiliza Pandas para estruturar tabelas e indicadores apresentados na aplicação.

## 6. Scikit-learn: desenvolvimento dos modelos

O Scikit-learn fornece ferramentas para construção e avaliação de modelos de aprendizado de máquina.

No projeto, os algoritmos documentados são:

- Regressão Logística;
- Random Forest.

A biblioteca oferece recursos para:

- Treinamento supervisionado;
- Classificação;
- Geração de probabilidades;
- Avaliação de desempenho;
- Validação de modelos;
- Construção de pipelines;
- Transformação de variáveis.

Os modelos utilizados na aplicação foram disponibilizados como artefatos compatíveis com o ecossistema Scikit-learn.

A escolha dos algoritmos considera a natureza tabular dos dados, a necessidade de classificação binária e a possibilidade de comparação entre modelos com características distintas.

## 7. MLflow: gestão e carregamento dos modelos

O MLflow é uma plataforma voltada ao gerenciamento do ciclo de vida de modelos de Machine Learning.

Entre suas funcionalidades estão:

- Rastreamento de experimentos;
- Registro de parâmetros;
- Armazenamento de métricas;
- Armazenamento de artefatos;
- Versionamento de modelos;
- Organização de experimentos;
- Gestão do ciclo de vida dos modelos.

Na implementação atual, a aplicação utiliza `mlflow.sklearn.load_model` para carregar os modelos armazenados nos diretórios locais.

A estrutura de caminhos identificada no código é:

```python
MODEL_LR_PATH = BASE_DIR / "models" / "regressao_logistica"

MODEL_RF_PATH = BASE_DIR / "models" / "random_forest"
```

O carregamento é realizado a partir desses diretórios.

Essa organização permite manter os artefatos separados da interface, facilitando a substituição dos modelos sem a necessidade de concentrar toda a lógica de modelagem no arquivo principal da aplicação.

### 7.1 Evolução do gerenciamento de modelos

Como evolução, recomenda-se estabelecer um fluxo formal de rastreabilidade que registre:

- Identificador do experimento;
- Versão do modelo;
- Algoritmo;
- Parâmetros;
- Métricas de avaliação;
- Período de treinamento;
- Data de criação;
- Artefatos utilizados;
- Responsável pela aprovação.

Essa estrutura permitirá reconstruir as condições de desenvolvimento e comparar versões de maneira controlada.

## 8. Streamlit: interface gerencial

O Streamlit é responsável pela apresentação da solução ao usuário.

Sua utilização permite desenvolver aplicações interativas utilizando Python, sem exigir a construção integral de uma interface web tradicional.

No projeto, a aplicação apresenta informações relacionadas a:

- Visão geral da operação;
- Desempenho preditivo;
- Comparação entre modelos;
- Indicadores estatísticos;
- Matrizes de confusão;
- Exposição financeira apresentada;
- Análise dos resultados.

A interface permite aproximar os resultados técnicos da rotina de análise e gestão de riscos.

### 8.1 Papel estratégico da interface

O Streamlit atua como camada de apresentação e interação.

Não deve ser confundido com a plataforma responsável por armazenar e governar toda a base corporativa.

Em uma arquitetura mais avançada, poderá consumir dados e resultados processados em uma infraestrutura analítica externa, mantendo sua função de interface gerencial.

## 9. Git e GitHub: controle de versão e reprodutibilidade

O Git é utilizado para controlar as alterações realizadas no código-fonte.

Entre suas principais contribuições estão:

- Histórico de alterações;
- Identificação de versões;
- Recuperação de estados anteriores;
- Organização do desenvolvimento;
- Colaboração entre desenvolvedores.

O GitHub disponibiliza o repositório remoto e facilita o compartilhamento do código, da documentação e dos componentes da solução.

A utilização de controle de versão é importante para garantir rastreabilidade das mudanças realizadas no projeto.

### 9.1 Boas práticas recomendadas

Recomenda-se:

1. Registrar alterações com mensagens descritivas.
2. Evitar arquivos temporários no repositório.
3. Não publicar credenciais ou dados sensíveis.
4. Manter o arquivo `requirements.txt` atualizado.
5. Documentar mudanças relevantes.
6. Separar versões experimentais e estáveis.
7. Registrar alterações nos modelos e dependências.

Os artefatos de modelos e os arquivos de dados devem seguir políticas de armazenamento e acesso compatíveis com seu tamanho, sensibilidade e finalidade.

## 10. Streamlit Community Cloud: disponibilização da aplicação

A aplicação está disponibilizada por meio do Streamlit Community Cloud.

Endereço público:

https://rqgbtxw7jddgpbc4gjz9mn.streamlit.app/

A hospedagem permite disponibilizar a interface pela internet, facilitando o acesso à solução.

O ambiente de hospedagem executa a aplicação e instala as dependências especificadas no projeto.

É importante distinguir hospedagem da interface de infraestrutura corporativa de dados.

A disponibilização da aplicação não significa que exista uma arquitetura completa de processamento distribuído, armazenamento analítico ou monitoramento de produção.

## 11. Fluxo funcional da arquitetura atual

O fluxo de funcionamento da aplicação pode ser representado conceitualmente:

```text
             REPOSITÓRIO DO PROJETO
                     |
                     v
          CÓDIGO E DEPENDÊNCIAS
                     |
                     v
             APLICAÇÃO STREAMLIT
                     |
          +----------+----------+
          |                     |
          v                     v
   MODELO REGRESSÃO       MODELO RANDOM
      LOGÍSTICA              FOREST
          |                     |
          +----------+----------+
                     |
                     v
             GERAÇÃO DE RESULTADOS
                     |
                     v
          INDICADORES E GRÁFICOS
                     |
                     v
             USUÁRIO GERENCIAL
```

O fluxo representa a organização lógica da aplicação de inferência.

A origem e o processo de preparação da base utilizada no treinamento não estão integralmente documentados no repositório atual.

Por isso, não se deve interpretar o diagrama como uma descrição comprovada de toda a infraestrutura de engenharia de dados.

## 12. Limitações arquiteturais atuais

A implementação atual atende à finalidade de disponibilização da aplicação, mas apresenta oportunidades de evolução.

Entre os principais pontos estão:

- Ausência de uma camada corporativa de armazenamento documentada;
- Ausência de um pipeline automatizado de ingestão demonstrado;
- Ausência de processamento distribuído comprovado;
- Ausência de monitoramento contínuo de dados;
- Ausência de uma política automatizada de retreinamento;
- Necessidade de fortalecer a rastreabilidade entre dados, previsões e investigações;
- Necessidade de formalizar a gestão de versões dos modelos.

Essas limitações representam oportunidades de amadurecimento arquitetural.

## 13. Arquitetura futura proposta com Databricks

A evolução proposta considera o Databricks como núcleo da infraestrutura de dados e processamento analítico.

A proposta busca separar claramente as responsabilidades de engenharia de dados, ciência de dados, gerenciamento de modelos e apresentação gerencial.

### 13.1 Camada de ingestão

Responsável pela entrada dos dados provenientes dos sistemas da seguradora.

Possíveis fontes:

- Sistemas de gestão de apólices;
- Sistemas de regulação de sinistros;
- Sistemas financeiros;
- Sistemas cadastrais;
- Registros históricos;
- Fontes externas autorizadas.

A ingestão deverá contemplar controles de qualidade, rastreabilidade, segurança e periodicidade.

### 13.2 Camada de armazenamento

O Delta Lake pode ser utilizado para organizar os dados em tabelas com suporte a transações ACID, histórico e evolução controlada dos dados.

Uma organização possível utiliza a arquitetura Medallion:

**Bronze**

Dados brutos recebidos das fontes.

**Silver**

Dados tratados, padronizados e submetidos a regras de qualidade.

**Gold**

Dados consolidados e organizados para análises, indicadores e treinamento dos modelos.

Essa estrutura permite separar diferentes níveis de processamento e facilitar a governança.

### 13.3 Camada de engenharia de dados

O processamento poderá utilizar Apache Spark por meio do Databricks.

Entre as atividades previstas:

- Limpeza dos dados;
- Padronização de variáveis;
- Tratamento de inconsistências;
- Integração de fontes;
- Construção de atributos;
- Agregações;
- Preparação de conjuntos de treinamento;
- Construção de tabelas analíticas.

O processamento distribuído poderá ser utilizado conforme o volume e a complexidade dos dados.

Para volumes menores, o uso de processamento distribuído deve ser justificado pelo custo e pela necessidade operacional.

### 13.4 Camada de ciência de dados

O ambiente Databricks poderá concentrar:

- Análise exploratória;
- Engenharia de atributos;
- Treinamento;
- Validação temporal;
- Avaliação estatística;
- Comparação de algoritmos;
- Análise de desempenho;
- Experimentos.

A organização dos notebooks e pipelines deverá permitir a reprodução dos experimentos.

### 13.5 Camada de gerenciamento de modelos

O MLflow poderá ser integrado ao ambiente Databricks para rastreamento dos experimentos e gerenciamento das versões dos modelos.

A evolução poderá contemplar:

- Registro de experimentos;
- Comparação de métricas;
- Registro de modelos;
- Versionamento;
- Aprovação de modelos;
- Histórico de implantação;
- Monitoramento do ciclo de vida.

### 13.6 Camada de apresentação

O Streamlit poderá permanecer como interface gerencial.

Sua responsabilidade será apresentar os resultados processados pela infraestrutura analítica.

A comunicação entre Streamlit e a camada de dados deverá utilizar mecanismos seguros de autenticação e acesso.

O objetivo é preservar a experiência gerencial da aplicação enquanto a infraestrutura de processamento evolui.

## 14. Diagrama conceitual da arquitetura futura

```text
              FONTES DE DADOS
                     |
                     v
             INGESTÃO DE DADOS
                     |
                     v
              DATABRICKS
                     |
           +---------+---------+
           |                   |
           v                   v
       DELTA LAKE        ENGENHARIA DE DADOS
           |                   |
           +---------+---------+
                     |
                     v
            ANÁLISE EXPLORATÓRIA
                     |
                     v
                MODELAGEM
                     |
                     v
          AVALIAÇÃO ESTATÍSTICA
                     |
                     v
                  MLFLOW
          EXPERIMENTOS E MODELOS
                     |
                     v
            MODELOS APROVADOS
                     |
                     v
                STREAMLIT
                     |
                     v
            GESTÃO E DECISÃO
```

O diagrama representa uma arquitetura-alvo proposta, não uma infraestrutura já implantada integralmente.

## 15. Segurança e governança da arquitetura

Em uma seguradora, os dados utilizados na prevenção de fraudes podem conter informações pessoais, financeiras e contratuais.

A arquitetura deve considerar:

- Controle de acesso por função;
- Princípio do menor privilégio;
- Gestão segura de credenciais;
- Criptografia em trânsito e em repouso;
- Registro de acessos;
- Segregação de ambientes;
- Proteção de informações sensíveis;
- Políticas de retenção;
- Auditoria de operações;
- Conformidade com a LGPD.

Também é importante garantir que os modelos não produzam decisões discriminatórias ou automatizadas sem supervisão adequada.

Os alertas devem apoiar o processo de investigação, respeitando os procedimentos de validação e decisão da seguradora.

## 16. Estratégia de evolução arquitetural

A evolução pode ser organizada em etapas.

### Etapa 1 — Consolidação da aplicação atual

- Organizar o código;
- Manter documentação técnica;
- Revisar dependências;
- Validar carregamento dos modelos;
- Fortalecer o controle de versão;
- Organizar os artefatos.

### Etapa 2 — Estruturação da engenharia de dados

- Definir fontes;
- Formalizar processos de ingestão;
- Implementar regras de qualidade;
- Organizar dados históricos;
- Criar camadas de armazenamento;
- Documentar linhagem dos dados.

### Etapa 3 — Integração com Databricks

- Configurar o ambiente;
- Estruturar tabelas;
- Organizar notebooks;
- Implementar processamento;
- Reproduzir a análise exploratória;
- Automatizar a preparação dos dados.

### Etapa 4 — Integração com MLflow

- Centralizar experimentos;
- Registrar parâmetros;
- Registrar métricas;
- Versionar modelos;
- Formalizar critérios de aprovação.

### Etapa 5 — Operacionalização e monitoramento

- Disponibilizar modelos aprovados;
- Integrar a interface gerencial;
- Monitorar previsões;
- Acompanhar drift;
- Registrar resultados das investigações;
- Avaliar retreinamento.

A implementação deverá considerar os custos de infraestrutura e as necessidades reais da operação.

## 17. Conclusão

A arquitetura tecnológica atual utiliza Python, Pandas, Scikit-learn, MLflow, Streamlit, Git e GitHub para disponibilizar uma solução de prevenção e análise de fraudes.

A separação entre interface, modelos e documentação permite organizar o projeto e estabelecer uma base para sua evolução.

A proposta de integração com Databricks busca ampliar a capacidade de processamento, organização e governança dos dados, mantendo o MLflow como componente de gestão dos experimentos e modelos e o Streamlit como interface gerencial.

A evolução arquitetural deverá ocorrer de forma incremental, priorizando rastreabilidade, segurança, reprodutibilidade e valor operacional.

O objetivo final é estabelecer uma plataforma analítica integrada, capaz de apoiar o ciclo completo de prevenção de fraudes, desde a ingestão dos dados até a geração de informações para tomada de decisão.