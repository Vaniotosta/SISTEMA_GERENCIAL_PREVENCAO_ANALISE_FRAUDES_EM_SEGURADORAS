# Problema de Negócio e Estratégia Analítica

## 1. Contextualização do problema de negócio

A prevenção e a identificação de fraudes constituem desafios relevantes para as organizações do mercado segurador. O processo de análise de sinistros exige a avaliação de informações cadastrais, contratuais, financeiras e circunstanciais para determinar a consistência das solicitações de indenização.

A identificação de possíveis irregularidades pode ser complexa, especialmente quando o volume de solicitações é elevado e os indícios de fraude não são evidentes em uma análise isolada.

Nesse cenário, a Ciência de Dados oferece recursos para identificar padrões, estimar probabilidades e priorizar registros que merecem investigação adicional.

O projeto propõe utilizar modelos preditivos como instrumentos de apoio à análise de sinistros, buscando melhorar a capacidade de identificação de ocorrências fraudulentas e fornecer indicadores que contribuam para decisões operacionais e gerenciais.

## 2. Formulação do problema analítico

Do ponto de vista de aprendizado de máquina, o problema foi estruturado como uma tarefa de classificação supervisionada.

Cada registro é associado a uma variável-alvo que representa duas situações:

- **Classe 0 — Não fraude:** registro classificado como não fraudulento.
- **Classe 1 — Fraude:** registro classificado como fraudulento.

O objetivo dos modelos é estimar a probabilidade de cada registro pertencer à classe fraudulenta.

Formalmente, considerando um vetor de características \(X\), o problema consiste em estimar:

\[
P(Y=1\mid X)
\]

Em que:

- \(X\) representa as variáveis explicativas do registro;
- \(Y\) representa a classe de interesse;
- \(Y=1\) indica fraude;
- \(P(Y=1\mid X)\) representa a probabilidade estimada de fraude.

A probabilidade estimada é posteriormente comparada a um limiar de classificação para produzir uma decisão binária.

É importante destacar que uma previsão positiva representa um alerta estatístico, não uma confirmação de fraude. A confirmação depende de investigação e validação apropriadas.

## 3. Desbalanceamento entre classes

A base considerada no projeto apresenta 20.000 registros, dos quais:

| Classe | Registros | Participação |
|---|---:|---:|
| Não fraude | 18.648 | 93,24% |
| Fraude | 1.352 | 6,76% |
| Total | 20.000 | 100% |

A distribuição demonstra uma predominância expressiva de registros classificados como não fraudulentos.

Esse comportamento caracteriza um problema de desbalanceamento de classes.

Uma consequência importante é que um classificador que previsse todos os registros como não fraude alcançaria uma acurácia de 93,24% na base completa, mesmo sem identificar qualquer ocorrência fraudulenta.

Portanto, uma acurácia elevada, isoladamente, não seria evidência suficiente de capacidade efetiva de prevenção de fraudes.

A estratégia de avaliação deve considerar indicadores que expressem diretamente a capacidade de identificar a classe minoritária.

## 4. Consequências dos erros de classificação

Em um sistema de identificação de fraudes, os erros de classificação apresentam consequências operacionais distintas.

### 4.1 Falso positivo

O falso positivo ocorre quando um registro não fraudulento é classificado pelo modelo como suspeito.

\[
FP = \text{Não fraude classificada como fraude}
\]

Esse erro pode gerar:

- Investigações desnecessárias;
- Aumento do volume de trabalho das equipes;
- Maior tempo de análise dos sinistros;
- Custos operacionais adicionais;
- Possíveis atrasos na conclusão de processos legítimos.

### 4.2 Falso negativo

O falso negativo ocorre quando um registro fraudulento é classificado pelo modelo como não fraudulento.

\[
FN = \text{Fraude classificada como não fraude}
\]

Esse erro pode representar:

- Fraudes não encaminhadas para investigação;
- Maior exposição financeira potencial;
- Oportunidades perdidas de identificação de irregularidades;
- Redução da efetividade do processo de prevenção.

### 4.3 Relação entre os erros

Os dois tipos de erro precisam ser avaliados conjuntamente.

Um modelo que identifica mais fraudes pode produzir mais alertas incorretos. Por outro lado, um modelo que reduz o volume de alertas pode deixar de identificar uma parcela maior das ocorrências fraudulentas.

Assim, a decisão gerencial não deve buscar apenas maximizar uma métrica isolada. Deve considerar os custos associados aos erros e a capacidade operacional da seguradora para investigar os alertas produzidos.

## 5. Justificativa para a utilização de modelos preditivos

A utilização de aprendizado de máquina permite identificar relações estatísticas entre características dos registros e a ocorrência histórica de fraude.

Diferentemente de uma estratégia baseada exclusivamente em regras fixas, os modelos podem estimar padrões a partir dos dados utilizados no treinamento.

Neste projeto, foram selecionados dois algoritmos complementares:

**Regressão Logística**

É um modelo estatístico utilizado em problemas de classificação binária. Estima probabilidades por meio da função logística e permite estabelecer uma referência metodológica para comparação.

Sua utilização é relevante pela estrutura relativamente simples e pela possibilidade de interpretação dos efeitos das variáveis, desde que sejam examinados os coeficientes e as condições do modelo.

**Random Forest**

É um algoritmo de aprendizado de máquina baseado na combinação de múltiplas árvores de decisão.

Sua estrutura permite representar relações não lineares e interações entre características, oferecendo uma abordagem alternativa à estrutura paramétrica da Regressão Logística.

A comparação dos dois métodos permite analisar diferentes comportamentos preditivos diante do mesmo problema.

## 6. Estratégia de avaliação temporal

A avaliação apresentada na aplicação utiliza uma divisão temporal dos registros:

- Treinamento: anos de 2023 e 2024.
- Teste: ano de 2025.

O conjunto de teste possui 6.649 registros, incluindo 476 ocorrências classificadas como fraude e 6.173 como não fraude.

A utilização de um período posterior ao treinamento é relevante porque aproxima a avaliação de uma situação operacional em que o modelo é aplicado a registros de um período futuro.

Essa estratégia reduz o risco de uma avaliação baseada exclusivamente em uma divisão aleatória que misture períodos anteriores e posteriores.

Entretanto, a validade dessa avaliação depende de aspectos que precisam ser verificados na implementação original, especialmente a ausência de vazamento temporal e a utilização exclusiva de informações disponíveis no momento da análise do sinistro.

## 7. Estratégia de decisão e limiar de classificação

Os modelos produzem probabilidades estimadas. Para transformá-las em classificações, é necessário estabelecer um limiar.

A aplicação utiliza os seguintes valores:

| Modelo | Limiar |
|---|---:|
| Regressão Logística | 0,50 |
| Random Forest | 0,25 |

De forma geral, um registro é classificado como suspeito quando sua probabilidade estimada atinge ou supera o limiar definido.

A redução do limiar tende a aumentar a quantidade de registros encaminhados como suspeitos, podendo elevar o recall, mas também aumentar os falsos positivos.

O aumento do limiar tende a reduzir a quantidade de alertas, mas pode elevar o número de fraudes não identificadas.

Como os modelos utilizam limiares diferentes, a comparação de suas classificações deve considerar essa diferença metodológica. As métricas de discriminação, como ROC-AUC e PR-AUC, complementam a análise porque avaliam o comportamento dos escores em diferentes limiares.

## 8. Critérios para a tomada de decisão

A seleção do modelo mais adequado depende dos objetivos operacionais da seguradora.

Entre os critérios relevantes estão:

1. Capacidade de identificar ocorrências fraudulentas;
2. Volume de alertas encaminhados para investigação;
3. Proporção de alertas que efetivamente correspondem a fraudes;
4. Quantidade de fraudes não identificadas;
5. Exposição financeira potencial associada aos casos não detectados;
6. Capacidade operacional das equipes de investigação.

A Regressão Logística apresentou recall superior no teste, enquanto o Random Forest apresentou maior precisão, acurácia e F1-score.

Essas diferenças demonstram que a escolha deve considerar o equilíbrio entre identificação de fraudes e eficiência operacional, e não apenas a classificação geral dos registros.

## 9. Hipótese de valor para o negócio

A hipótese central do projeto é que o uso de modelos preditivos pode contribuir para uma priorização mais estruturada dos sinistros que merecem investigação.

A geração de alertas baseada em probabilidades permite organizar o processo de análise, direcionando a atenção das equipes para registros com maior suspeição estatística.

O benefício econômico potencial depende de fatores que precisam ser validados em ambiente operacional, como:

- Taxa de confirmação dos alertas;
- Custo médio de investigação;
- Valor efetivamente recuperado ou evitado;
- Tempo adicional de análise;
- Impacto sobre o tratamento de sinistros legítimos.

Portanto, o desempenho estatístico dos modelos constitui uma dimensão importante, mas não é suficiente para comprovar isoladamente o retorno financeiro da solução.

## 10. Síntese estratégica

O problema de prevenção de fraudes foi estruturado como uma tarefa de classificação supervisionada, com atenção especial ao desbalanceamento entre classes e às consequências dos erros de classificação.

A estratégia combina dois algoritmos de características distintas, avaliação temporal e análise de indicadores estatísticos e gerenciais.

A principal contribuição esperada é oferecer suporte à priorização de investigações, com maior transparência sobre o desempenho dos modelos e os compromissos envolvidos na tomada de decisão.

A evolução dessa estratégia deverá incorporar validação operacional, análise de custos, calibração das probabilidades e monitoramento contínuo do desempenho preditivo.