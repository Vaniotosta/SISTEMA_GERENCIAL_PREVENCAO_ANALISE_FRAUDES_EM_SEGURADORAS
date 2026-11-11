# Sistema Gerencial de Prevenção e Análise de Fraudes em Seguradoras

## 1. Apresentação

O Sistema Gerencial de Prevenção e Análise de Fraudes em Seguradoras é uma solução baseada em Ciência de Dados e Aprendizado de Máquina (Machine Learning), desenvolvida para apoiar a identificação de possíveis ocorrências fraudulentas em processos de análise de sinistros.

A proposta consiste em utilizar modelos preditivos para estimar a probabilidade de fraude, produzir indicadores de desempenho e oferecer informações que auxiliem equipes de investigação e gestores na priorização de casos.

O sistema integra modelos estatísticos e algoritmos de aprendizado de máquina a uma interface gerencial desenvolvida em Streamlit, permitindo consultar resultados, comparar modelos e realizar análises de casos individuais.

## 2. Contextualização do problema

A ocorrência de fraudes representa um desafio relevante para o setor de seguros, pois pode provocar perdas financeiras, elevar custos operacionais, comprometer a eficiência dos processos de regulação de sinistros e afetar o equilíbrio econômico das carteiras.

A identificação de comportamentos suspeitos envolve um problema analítico complexo. Em geral, as ocorrências fraudulentas representam uma parcela menor do total de sinistros, o que caracteriza um cenário de desbalanceamento entre classes.

Nesse contexto, modelos tradicionais de classificação podem apresentar elevada acurácia global sem necessariamente identificar adequadamente os casos fraudulentos.

Por esse motivo, o projeto considera métricas específicas para a classe positiva, como recall, precision, F1-score e área sob a curva Precision-Recall, além da análise de indicadores financeiros e operacionais.

## 3. Objetivo geral

Desenvolver uma solução analítica capaz de apoiar a prevenção e a análise de fraudes em seguradoras por meio da aplicação de técnicas de Ciência de Dados, modelagem preditiva e visualização gerencial.

## 4. Objetivos específicos

- Aplicar modelos de classificação para estimar a probabilidade de ocorrência de fraude.
- Comparar o desempenho da Regressão Logística e do Random Forest.
- Avaliar os modelos considerando diferentes dimensões de desempenho estatístico.
- Analisar o equilíbrio entre identificação de fraudes e geração de alertas.
- Apresentar indicadores gerenciais e estimativas de exposição financeira.
- Disponibilizar uma interface para consulta e interpretação dos resultados.
- Estabelecer uma base metodológica para futuras versões do sistema.

## 5. Estratégia analítica

A solução utiliza uma abordagem de aprendizado supervisionado, na qual os modelos são treinados para distinguir registros classificados como fraudulentos e não fraudulentos.

Foram considerados dois algoritmos com características complementares:

**Regressão Logística:** modelo estatístico de classificação que estima a probabilidade de ocorrência de uma classe a partir de uma combinação das variáveis explicativas. É utilizado como referência interpretável para comparação.

**Random Forest:** algoritmo baseado em um conjunto de árvores de decisão, capaz de representar relações não lineares e interações entre variáveis.

A comparação entre os algoritmos permite avaliar diferentes compromissos entre capacidade de identificação, volume de alertas e desempenho geral.

## 6. Caracterização quantitativa do projeto

Os resultados disponibilizados na aplicação indicam a seguinte caracterização:

| Indicador | Resultado |
|---|---:|
| Registros da base | 20.000 |
| Registros classificados como fraude | 1.352 |
| Registros classificados como não fraude | 18.648 |
| Participação de fraudes | 6,76% |
| Variáveis inicialmente disponíveis | 33 |
| Variáveis utilizadas como entradas | 22 |
| Registros do conjunto de teste | 6.649 |
| Fraudes no conjunto de teste | 476 |

A proporção de fraudes de 6,76% evidencia o desbalanceamento entre as classes e justifica a utilização de métricas complementares à acurácia.

A avaliação reportada considera uma separação temporal: dados de 2023 e 2024 para treinamento e dados de 2025 para teste. Essa estratégia busca avaliar a capacidade de generalização dos modelos em um período posterior ao utilizado no treinamento.

## 7. Resultados preliminares dos modelos

A aplicação apresenta os seguintes resultados para o conjunto de teste:

| Métrica | Regressão Logística | Random Forest |
|---|---:|---:|
| Acurácia | 69,24% | 77,56% |
| Precisão | 14,32% | 17,64% |
| Recall | 66,18% | 58,19% |
| F1-score | 23,55% | 27,08% |
| ROC-AUC | 0,7631 | 0,7462 |
| PR-AUC | 0,2244 | 0,1954 |

Os resultados demonstram que os modelos apresentam características distintas.

A Regressão Logística possui maior recall e maior PR-AUC, indicando melhor capacidade de identificação da classe fraudulenta segundo essas métricas.

O Random Forest apresenta maior acurácia, precisão e F1-score, além de produzir menor volume de alertas no limiar utilizado pela aplicação.

A interpretação dos resultados deve considerar o contexto operacional da seguradora, pois a escolha do modelo depende dos custos relativos dos falsos positivos e falsos negativos.

## 8. Contribuição gerencial

O sistema procura transformar resultados preditivos em informações úteis à tomada de decisão.

Entre os principais elementos gerenciais estão:

- Comparação do desempenho dos modelos;
- Identificação de fraudes detectadas e não detectadas;
- Quantificação dos alertas gerados;
- Análise de indicadores de desempenho;
- Apresentação de estimativas de exposição financeira;
- Consulta individual de registros para apoio à análise.

A aplicação também apresenta uma estimativa de exposição financeira associada a fraudes não identificadas, com valores reportados de aproximadamente R$ 2,94 milhões para a Regressão Logística e R$ 3,95 milhões para o Random Forest.

Esses valores são indicadores apresentados pela aplicação e devem ser interpretados com cautela. Não representam, por si só, perdas efetivamente realizadas, economia comprovada ou recuperação financeira.

## 9. Arquitetura tecnológica

A versão atual utiliza:

- **Python:** linguagem principal de desenvolvimento.
- **Pandas:** manipulação e organização de dados.
- **MLflow:** carregamento e gerenciamento dos artefatos dos modelos.
- **Scikit-learn:** ecossistema de algoritmos de aprendizado de máquina.
- **Streamlit:** desenvolvimento da interface gerencial.
- **Git e GitHub:** versionamento e disponibilização do projeto.

Os modelos serializados são disponibilizados em diretórios próprios, separados por algoritmo, e carregados pela aplicação.

Como evolução arquitetural, está planejada a ampliação do uso do Databricks como ambiente central de processamento, exploração de dados, treinamento e avaliação, mantendo o Streamlit como interface gerencial.

Essa arquitetura futura deverá ser implementada e validada antes de ser considerada parte da infraestrutura operacional atual.

## 10. Limitações e cuidados de interpretação

Os resultados apresentados devem ser interpretados considerando as seguintes limitações:

1. A qualidade das previsões depende da representatividade e da qualidade dos dados utilizados no treinamento.
2. A baixa prevalência de fraudes torna insuficiente a avaliação baseada exclusivamente em acurácia.
3. A definição do limiar de classificação influencia diretamente o número de alertas e a quantidade de fraudes identificadas.
4. As métricas apresentadas não substituem a validação operacional dos casos suspeitos.
5. As estimativas financeiras não devem ser interpretadas como perdas ou economias efetivamente realizadas.
6. A documentação metodológica deverá ser complementada com evidências dos processos originais de preparação dos dados, treinamento e avaliação.

O sistema deve ser entendido como ferramenta de apoio à decisão, e não como mecanismo autônomo de confirmação de fraude.

## 11. Considerações finais

O projeto demonstra a aplicação de técnicas de Ciência de Dados a um problema relevante do setor de seguros, articulando modelagem preditiva, avaliação estatística e indicadores gerenciais.

A comparação entre Regressão Logística e Random Forest evidencia que a escolha de um modelo de prevenção de fraudes não deve ser baseada apenas na acurácia. É necessário considerar a capacidade de identificação de fraudes, o custo operacional dos alertas e a exposição financeira potencial.

A evolução da solução deverá priorizar rastreabilidade dos experimentos, validação temporal, monitoramento de desempenho, governança dos dados e integração estruturada com plataformas de engenharia e ciência de dados.