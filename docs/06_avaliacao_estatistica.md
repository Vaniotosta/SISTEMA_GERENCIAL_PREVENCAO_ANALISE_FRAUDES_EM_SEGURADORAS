# Avaliação Estatística dos Modelos Preditivos

## 1. Introdução

A avaliação estatística é uma etapa essencial para determinar a capacidade de generalização e a qualidade preditiva dos modelos de classificação.

Em problemas de prevenção de fraudes, a análise não deve se limitar à acurácia, pois a distribuição desbalanceada das classes pode produzir resultados aparentemente elevados sem que o modelo apresente capacidade adequada de identificação das ocorrências fraudulentas.

Este capítulo apresenta a avaliação comparativa da Regressão Logística e do Random Forest, considerando métricas de classificação, matrizes de confusão, desempenho discriminatório e consequências operacionais dos erros.

Os resultados apresentados correspondem aos indicadores disponibilizados pela aplicação para o conjunto de teste de 2025.

## 2. Caracterização do conjunto de teste

O conjunto utilizado na avaliação apresenta:

| Indicador | Quantidade |
|---|---:|
| Total de registros | 6.649 |
| Registros fraudulentos | 476 |
| Registros não fraudulentos | 6.173 |
| Prevalência de fraude | 7,16% |

A proporção de registros fraudulentos demonstra que a classe positiva permanece minoritária no conjunto de teste.

Esse cenário exige atenção especial à interpretação das métricas, principalmente à precisão, ao recall e à área sob a curva Precision-Recall.

## 3. Métricas de avaliação

### 3.1 Acurácia (Accuracy)

A acurácia representa a proporção de classificações corretas em relação ao total de observações.

\[
Accuracy=\frac{TP+TN}{TP+TN+FP+FN}
\]

Em que:

- TP: verdadeiros positivos;
- TN: verdadeiros negativos;
- FP: falsos positivos;
- FN: falsos negativos.

A métrica oferece uma visão geral do desempenho, mas pode ser inadequada quando existe forte desbalanceamento entre classes.

### 3.2 Precisão (Precision)

A precisão representa a proporção de registros classificados como positivos que realmente pertencem à classe positiva.

\[
Precision=\frac{TP}{TP+FP}
\]

No contexto do projeto, indica a proporção de alertas de fraude que corresponde a ocorrências classificadas como fraudulentas na base de referência.

Uma precisão reduzida significa que uma parcela significativa dos alertas poderá exigir investigação sem corresponder a uma fraude identificada no conjunto de referência.

### 3.3 Sensibilidade ou Recall

O recall representa a proporção de fraudes identificadas corretamente em relação ao total de fraudes existentes no conjunto avaliado.

\[
Recall=\frac{TP}{TP+FN}
\]

É uma métrica especialmente relevante para prevenção de fraudes, pois expressa a capacidade de identificação da classe minoritária.

Um recall elevado significa que uma parcela maior das fraudes foi identificada pelo modelo.

### 3.4 F1-score

O F1-score corresponde à média harmônica entre precisão e recall.

\[
F1=2\times\frac{Precision\times Recall}{Precision+Recall}
\]

A métrica procura equilibrar a capacidade de identificar fraudes com a proporção de alertas corretos.

É útil quando existe interesse simultâneo em reduzir falsos negativos e falsos positivos.

### 3.5 ROC-AUC

A curva ROC representa a relação entre a taxa de verdadeiros positivos e a taxa de falsos positivos para diferentes limiares de classificação.

A taxa de verdadeiros positivos corresponde ao recall:

\[
TPR=\frac{TP}{TP+FN}
\]

A taxa de falsos positivos é:

\[
FPR=\frac{FP}{FP+TN}
\]

A área sob a curva ROC, conhecida como ROC-AUC, resume a capacidade discriminatória do modelo ao longo de diferentes limiares.

Quanto maior o valor, melhor tende a ser a capacidade de distinguir registros positivos e negativos.

Entretanto, em bases muito desbalanceadas, a ROC-AUC deve ser interpretada conjuntamente com métricas mais sensíveis ao desempenho na classe minoritária.

### 3.6 PR-AUC

A curva Precision-Recall representa a relação entre precisão e recall em diferentes limiares.

A área sob essa curva é particularmente relevante em problemas de detecção de fraudes, pois concentra a avaliação na classe positiva.

A comparação com a prevalência da classe positiva oferece uma referência adicional.

No conjunto de teste, a prevalência de fraude é de aproximadamente 7,16%.

Os valores de PR-AUC apresentados pelos modelos são superiores a essa referência, indicando capacidade discriminatória acima de uma referência baseada na prevalência.

A interpretação deve considerar também a forma da curva, os limiares e os custos operacionais dos alertas.

## 4. Comparação geral dos resultados

A aplicação apresenta os seguintes resultados:

| Métrica | Regressão Logística | Random Forest |
|---|---:|---:|
| Acurácia | 69,24% | 77,56% |
| Precisão | 14,32% | 17,64% |
| Recall | 66,18% | 58,19% |
| F1-score | 23,55% | 27,08% |
| ROC-AUC | 0,7631 | 0,7462 |
| PR-AUC | 0,2244 | 0,1954 |

A comparação demonstra que os modelos apresentam vantagens distintas.

A Regressão Logística possui maior recall e PR-AUC, enquanto o Random Forest apresenta maior acurácia, precisão, F1-score e ROC-AUC? 

**Correção metodológica:** o valor de ROC-AUC da Regressão Logística é 0,7631, superior ao valor de 0,7462 do Random Forest. Portanto, a Regressão Logística também apresenta maior ROC-AUC.

O Random Forest apresenta vantagem nas métricas de acurácia, precisão e F1-score.

## 5. Análise das matrizes de confusão

A matriz de confusão permite decompor os resultados em quatro categorias.

| Resultado | Significado |
|---|---|
| Verdadeiro positivo (TP) | Fraude corretamente identificada |
| Verdadeiro negativo (TN) | Não fraude corretamente identificada |
| Falso positivo (FP) | Não fraude classificada como suspeita |
| Falso negativo (FN) | Fraude não identificada |

### 5.1 Regressão Logística

A matriz de confusão reportada é:

| Classificação | Previsto: Fraude | Previsto: Não fraude |
|---|---:|---:|
| Real: Fraude | 315 | 161 |
| Real: Não fraude | 1.884 | 4.289 |

Interpretação:

- 315 fraudes foram identificadas corretamente.
- 161 fraudes não foram identificadas.
- 1.884 registros não fraudulentos foram classificados como suspeitos.
- 4.289 registros não fraudulentos foram classificados corretamente.

O modelo gerou 2.199 alertas, considerando verdadeiros positivos e falsos positivos.

### 5.2 Random Forest

A matriz de confusão reportada é:

| Classificação | Previsto: Fraude | Previsto: Não fraude |
|---|---:|---:|
| Real: Fraude | 277 | 199 |
| Real: Não fraude | 1.293 | 4.880 |

Interpretação:

- 277 fraudes foram identificadas corretamente.
- 199 fraudes não foram identificadas.
- 1.293 registros não fraudulentos foram classificados como suspeitos.
- 4.880 registros não fraudulentos foram classificados corretamente.

O modelo gerou 1.570 alertas.

## 6. Comparação operacional dos erros

A análise conjunta das matrizes evidencia diferenças importantes.

| Indicador | Regressão Logística | Random Forest |
|---|---:|---:|
| Verdadeiros positivos | 315 | 277 |
| Falsos positivos | 1.884 | 1.293 |
| Verdadeiros negativos | 4.289 | 4.880 |
| Falsos negativos | 161 | 199 |
| Total de alertas | 2.199 | 1.570 |

A Regressão Logística identificou 38 fraudes a mais que o Random Forest.

Também apresentou 38 falsos negativos a menos.

Em contrapartida, gerou 629 alertas adicionais, dos quais a maior parte correspondeu a falsos positivos.

O Random Forest reduziu o volume de alertas, mas deixou de identificar uma quantidade maior de fraudes.

Esses resultados demonstram o compromisso entre capacidade de detecção e carga operacional de investigação.

## 7. Análise do classificador majoritário

A acurácia precisa ser comparada com uma referência simples.

Se todos os registros fossem classificados como não fraude, o desempenho seria:

| Conjunto | Acurácia majoritária |
|---|---:|
| Base completa | 93,24% |
| Conjunto de teste | 92,84% |

Esse classificador não identificaria nenhuma fraude.

Consequentemente, sua precisão e recall para a classe fraude seriam nulos, e ele não teria utilidade para o objetivo central do projeto.

Esse exemplo demonstra por que a acurácia isolada não deve orientar a seleção de modelos em bases desbalanceadas.

Embora os modelos apresentem acurácias inferiores à referência majoritária, eles identificam ocorrências fraudulentas, característica essencial para a finalidade da solução.

## 8. Interpretação do desempenho da Regressão Logística

A Regressão Logística apresentou:

- Recall de 66,18%;
- Precisão de 14,32%;
- F1-score de 23,55%;
- ROC-AUC de 0,7631;
- PR-AUC de 0,2244.

O recall indica que aproximadamente dois terços das fraudes presentes no conjunto de teste foram identificados.

A precisão demonstra que somente uma parcela dos alertas correspondeu à classe positiva na referência utilizada.

O resultado sugere uma estratégia mais sensível à identificação de fraudes, mas com maior necessidade de investigação dos registros sinalizados.

## 9. Interpretação do desempenho do Random Forest

O Random Forest apresentou:

- Recall de 58,19%;
- Precisão de 17,64%;
- F1-score de 27,08%;
- ROC-AUC de 0,7462;
- PR-AUC de 0,1954.

O modelo apresentou maior precisão, indicando uma proporção superior de acertos entre os alertas emitidos.

Também apresentou menor volume total de alertas e maior quantidade de verdadeiros negativos.

Entretanto, identificou menos fraudes do que a Regressão Logística.

O resultado pode ser interessante em operações com capacidade limitada de investigação, desde que a maior quantidade de fraudes não identificadas seja considerada aceitável sob os critérios de risco da organização.

## 10. Considerações sobre os limiares

A aplicação utiliza limiares diferentes:

- Regressão Logística: 0,50.
- Random Forest: 0,25.

Esses valores influenciam diretamente as matrizes de confusão e as métricas dependentes do limiar.

Portanto, a comparação das classificações não representa uma comparação dos modelos sob uma condição idêntica de decisão.

Para aprofundar a avaliação, recomenda-se testar diferentes limiares para ambos os algoritmos, utilizando critérios previamente definidos.

Uma possibilidade é construir curvas de custo que relacionem:

- Quantidade de fraudes identificadas;
- Quantidade de falsos positivos;
- Custo médio de investigação;
- Valor associado aos falsos negativos;
- Capacidade operacional da equipe.

## 11. Limitações da avaliação

Os resultados disponíveis oferecem uma comparação quantitativa relevante, mas existem aspectos que devem ser considerados:

1. Os resultados dependem da qualidade e da representatividade da base.
2. As métricas dependentes do limiar são influenciadas pelos valores utilizados em cada modelo.
3. A comparação econômica depende de informações adicionais sobre os custos reais dos erros.
4. ROC-AUC e PR-AUC não substituem a validação operacional.
5. A capacidade de generalização deve ser reavaliada em novos períodos.
6. A avaliação deverá ser complementada por calibração das probabilidades e análise de estabilidade.

Também é necessário confirmar os procedimentos originais de validação e treinamento para completar a auditoria metodológica.

## 12. Conclusão da avaliação estatística

A avaliação demonstra que a Regressão Logística e o Random Forest apresentam comportamentos distintos diante do problema de identificação de fraudes.

A Regressão Logística apresentou maior capacidade de identificação da classe positiva, medida pelo recall, além de maiores valores de ROC-AUC e PR-AUC.

O Random Forest apresentou maior acurácia, precisão e F1-score, com menor volume de alertas.

A escolha depende das prioridades da seguradora: ampliar a detecção de fraudes ou controlar a quantidade de investigações geradas.

A decisão deverá integrar desempenho estatístico, custos operacionais, exposição financeira, capacidade investigativa e critérios de governança.