# Interpretação Gerencial dos Gráficos e Indicadores

## 1. Introdução

A visualização de dados desempenha papel fundamental na transformação de resultados analíticos em informações compreensíveis para gestores e equipes operacionais.

Em uma seguradora, a prevenção de fraudes exige decisões que envolvem risco financeiro, eficiência operacional, qualidade da regulação e priorização de investigações.

Por essa razão, os gráficos da aplicação devem ser interpretados considerando três dimensões:

1. Desempenho estatístico dos modelos;
2. Consequências operacionais das classificações;
3. Potencial impacto financeiro para a organização.

A visualização não deve ser entendida apenas como elemento estético da aplicação. Cada indicador precisa responder a uma pergunta gerencial específica.

Este documento estabelece uma referência de interpretação dos principais indicadores apresentados pela solução.

## 2. Visão geral gerencial

A visão geral deve permitir que um gestor compreenda rapidamente o cenário da operação antifraude.

Entre as informações relevantes estão:

- Quantidade de registros analisados;
- Distribuição entre fraudes e não fraudes;
- Proporção de ocorrências fraudulentas;
- Desempenho dos modelos;
- Volume de alertas;
- Quantidade de fraudes identificadas;
- Exposição financeira apresentada.

### Interpretação gerencial

A primeira leitura deve considerar a dimensão da base e a frequência de fraudes.

Na base analisada, existem 20.000 registros, dos quais 1.352 correspondem à classe fraudulenta, representando 6,76%.

Esse resultado demonstra que a classe positiva é minoritária.

Para a gestão, isso significa que a operação não deve utilizar somente a quantidade total de classificações corretas como critério de avaliação.

É necessário acompanhar a capacidade de identificação das fraudes e o esforço operacional gerado pelos alertas.

## 3. Distribuição das classes

Um gráfico de distribuição das classes permite visualizar a proporção entre registros fraudulentos e não fraudulentos.

| Classe | Registros | Participação |
|---|---:|---:|
| Fraude | 1.352 | 6,76% |
| Não fraude | 18.648 | 93,24% |

### Interpretação

A concentração de registros na classe não fraudulenta caracteriza um problema de classificação desbalanceada.

Esse cenário possui duas implicações gerenciais:

- Um modelo pode apresentar elevada acurácia sem identificar adequadamente as fraudes.
- A operação precisa equilibrar a capacidade de detecção com o volume de investigações.

O gráfico deve ser utilizado para contextualizar os indicadores de desempenho e evitar interpretações equivocadas.

## 4. Indicadores de desempenho preditivo

A comparação entre modelos deve ser apresentada de forma integrada.

| Indicador | Regressão Logística | Random Forest |
|---|---:|---:|
| Acurácia | 69,24% | 77,56% |
| Precisão | 14,32% | 17,64% |
| Recall | 66,18% | 58,19% |
| F1-score | 23,55% | 27,08% |
| ROC-AUC | 0,7631 | 0,7462 |
| PR-AUC | 0,2244 | 0,1954 |

### Interpretação gerencial

A Regressão Logística apresenta maior recall, o que significa maior proporção de fraudes identificadas no conjunto de teste.

O Random Forest apresenta maior precisão e menor volume de alertas.

A escolha depende da prioridade operacional da seguradora.

Se a prioridade for ampliar a identificação de fraudes, a Regressão Logística apresenta vantagem no limiar utilizado.

Se a prioridade for reduzir o volume de alertas, o Random Forest apresenta uma configuração mais econômica em termos de quantidade de registros encaminhados à investigação.

Essa decisão deve ser acompanhada por uma análise dos custos associados aos erros.

## 5. Interpretação da matriz de confusão

A matriz de confusão é uma das visualizações mais importantes da aplicação.

Ela permite identificar como os modelos classificaram os registros em comparação com os resultados de referência.

### Regressão Logística

- Verdadeiros positivos: 315.
- Falsos positivos: 1.884.
- Verdadeiros negativos: 4.289.
- Falsos negativos: 161.

### Random Forest

- Verdadeiros positivos: 277.
- Falsos positivos: 1.293.
- Verdadeiros negativos: 4.880.
- Falsos negativos: 199.

### Interpretação gerencial

A Regressão Logística identificou 38 fraudes adicionais, mas gerou 591 falsos positivos adicionais.

O Random Forest apresentou menor volume de alertas e maior quantidade de registros não fraudulentos corretamente classificados.

A matriz deve ser interpretada como instrumento de análise do equilíbrio entre detecção e eficiência operacional.

## 6. Indicador de volume de alertas

O volume de alertas representa a quantidade de registros encaminhados para análise a partir das classificações positivas.

| Modelo | Alertas |
|---|---:|
| Regressão Logística | 2.199 |
| Random Forest | 1.570 |

A quantidade de alertas é calculada pela soma de verdadeiros positivos e falsos positivos.

\[
Alertas=TP+FP
\]

### Interpretação gerencial

O Random Forest gera 629 alertas a menos.

Isso representa uma redução aproximada de 28,60% no volume de alertas em relação à Regressão Logística.

Entretanto, a redução do volume de alertas não deve ser considerada automaticamente uma melhoria global.

É necessário observar que o Random Forest também identificou menos fraudes.

A gestão deve avaliar se a redução da carga operacional compensa a quantidade adicional de fraudes não identificadas.

## 7. Interpretação da exposição financeira

A aplicação apresenta os seguintes valores:

| Modelo | Exposição apresentada |
|---|---:|
| Regressão Logística | R$ 2.935.123,43 |
| Random Forest | R$ 3.951.496,83 |

A diferença apresentada é de R$ 1.016.373,40.

### Interpretação gerencial

O indicador procura oferecer uma perspectiva financeira para a análise dos modelos.

Entretanto, os valores apresentados na aplicação ainda precisam ter sua origem e metodologia de cálculo validadas.

A implementação consultada utiliza valores fixos na construção do gráfico.

Por essa razão, o indicador deve ser tratado como uma referência exibida pela interface, e não como comprovação de perda efetiva, economia ou retorno financeiro.

A interpretação gerencial definitiva dependerá da associação entre os resultados dos modelos e os valores individuais dos sinistros.

## 8. Relação entre os gráficos e as decisões gerenciais

As visualizações devem apoiar decisões específicas.

| Visualização | Pergunta gerencial | Decisão apoiada |
|---|---|---|
| Distribuição das classes | Qual a frequência de fraudes? | Dimensionamento do risco |
| Indicadores de desempenho | Qual modelo apresenta melhor resultado em cada métrica? | Seleção de estratégia |
| Matriz de confusão | Quais erros cada modelo produz? | Avaliação de riscos |
| Volume de alertas | Quantos casos exigem investigação? | Dimensionamento da equipe |
| Exposição financeira | Qual exposição a interface atribui aos modelos? | Investigação da metodologia financeira |

A interpretação deve considerar o contexto da operação e não apenas a posição de um modelo em um ranking.

## 9. Recomendações de aprimoramento das visualizações

Para ampliar a qualidade gerencial da aplicação, recomenda-se desenvolver gradualmente as seguintes visualizações:

### 9.1 Indicadores executivos

Apresentar cartões com:

- Total de sinistros analisados;
- Quantidade de fraudes identificadas;
- Percentual de detecção;
- Volume de alertas;
- Taxa de confirmação das investigações;
- Valor de pagamentos efetivamente evitados.

Os indicadores financeiros devem ser apresentados somente quando sua metodologia estiver validada.

### 9.2 Comparação de métricas

Utilizar gráficos comparativos para apresentar as métricas dos modelos.

É importante manter escalas e unidades coerentes, evitando que diferenças pequenas sejam visualmente exageradas.

### 9.3 Matrizes de confusão

Apresentar as matrizes com valores absolutos e, quando possível, percentuais por classe real.

Essa combinação facilita a compreensão do volume de erros e da proporção de fraudes identificadas.

### 9.4 Evolução temporal

Recomenda-se acompanhar:

- Quantidade de alertas por mês;
- Fraudes confirmadas por período;
- Evolução do recall;
- Evolução da precisão;
- Valor financeiro confirmado;
- Tempo médio de investigação.

Esses indicadores permitem identificar mudanças no comportamento da carteira e possíveis alterações no desempenho dos modelos.

### 9.5 Análise por segmento

Quando houver dados suficientes, recomenda-se segmentar os resultados por:

- Estado;
- Tipo de sinistro;
- Tipo de cobertura;
- Canal de venda;
- Faixa de valor segurado;
- Perfil temporal das ocorrências.

A segmentação deve respeitar critérios de qualidade estatística, privacidade e governança.

## 10. Princípios de comunicação visual

A interface gerencial deve seguir princípios que favoreçam a interpretação correta dos resultados:

1. Priorizar clareza e legibilidade.
2. Utilizar títulos que expliquem o significado dos indicadores.
3. Informar unidades de medida.
4. Apresentar períodos de referência.
5. Diferenciar valores absolutos de percentuais.
6. Evitar escalas que distorçam comparações.
7. Exibir ressalvas metodológicas quando necessárias.
8. Utilizar cores de forma consistente.
9. Evitar excesso de informações em uma única visualização.
10. Destacar os indicadores que apoiam decisões operacionais.

## 11. Limitações de interpretação

As visualizações refletem os dados e os cálculos utilizados pela aplicação.

Portanto, a confiabilidade da interpretação depende de:

- Qualidade dos dados de entrada;
- Correção dos cálculos;
- Consistência dos modelos;
- Representatividade do conjunto de teste;
- Definição dos limiares;
- Validação das informações financeiras;
- Atualização dos indicadores.

Um gráfico visualmente sofisticado não garante validade estatística.

A qualidade analítica depende da consistência entre dados, métodos, resultados e conclusões.

## 12. Conclusão

A interpretação gerencial dos gráficos permite conectar o desempenho dos modelos às necessidades de uma operação de prevenção de fraudes em seguradoras.

Os resultados demonstram que a Regressão Logística apresenta maior sensibilidade à identificação de fraudes, enquanto o Random Forest reduz o volume de alertas e apresenta maior precisão.

Essas diferenças devem ser analisadas em conjunto com a capacidade operacional, os custos de investigação e os riscos financeiros.

A evolução da aplicação deve priorizar indicadores rastreáveis, atualização periódica e integração entre resultados preditivos e informações operacionais.

Dessa forma, a solução poderá evoluir de uma ferramenta de classificação para um instrumento de apoio à gestão de riscos e à tomada de decisão baseada em dados.