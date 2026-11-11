# Estratégia de Modelagem Preditiva

## 1. Introdução

A modelagem preditiva constitui o núcleo analítico do Sistema Gerencial de Prevenção e Análise de Fraudes em Seguradoras.

Seu objetivo é identificar padrões estatísticos associados à ocorrência de fraudes e estimar a probabilidade de que determinado registro pertença à classe fraudulenta.

O problema foi estruturado como uma tarefa de classificação binária supervisionada, utilizando dois algoritmos com abordagens distintas: Regressão Logística e Random Forest.

A utilização desses modelos permite comparar uma abordagem estatística paramétrica com um método de aprendizado baseado em conjuntos de árvores de decisão.

Essa comparação é relevante porque o desempenho de um sistema de prevenção de fraudes não depende apenas da capacidade de classificação, mas também do equilíbrio entre identificação de ocorrências, volume de alertas e custos operacionais.

## 2. Formulação matemática do problema

Considere uma base de dados composta por observações:

\[
D=\{(X_i,Y_i)\}_{i=1}^{n}
\]

Em que:

- \(X_i\) representa o conjunto de características do registro;
- \(Y_i\) representa a classe observada;
- \(n\) representa o número total de observações.

A variável-alvo assume dois valores:

\[
Y_i \in \{0,1\}
\]

Onde:

- \(Y_i=0\): não fraude;
- \(Y_i=1\): fraude.

O objetivo dos algoritmos é estimar uma função:

\[
f(X_i)=P(Y_i=1\mid X_i)
\]

Essa função produz uma probabilidade estimada de fraude, que posteriormente pode ser transformada em uma classificação por meio de um limiar de decisão.

## 3. Regressão Logística

### 3.1 Fundamentação estatística

A Regressão Logística é um modelo estatístico utilizado em problemas de classificação binária.

Diferentemente da regressão linear tradicional, que estima valores contínuos sem restrição ao intervalo unitário, a Regressão Logística utiliza uma função que limita as probabilidades estimadas ao intervalo entre zero e um.

A função logística é definida por:

\[
P(Y=1\mid X)=
\frac{1}{1+e^{-z}}
\]

Em que:

\[
z=\beta_0+\beta_1X_1+\beta_2X_2+\cdots+\beta_pX_p
\]

Os elementos representam:

- \(\beta_0\): intercepto;
- \(\beta_j\): coeficientes estimados;
- \(X_j\): variáveis explicativas;
- \(p\): quantidade de variáveis utilizadas.

A função logística transforma a combinação linear das características em uma probabilidade estimada.

### 3.2 Interpretação dos coeficientes

Os coeficientes representam a relação entre cada variável explicativa e o logaritmo das chances de ocorrência da classe positiva, considerando as demais variáveis do modelo.

A interpretação pode ser realizada por meio da razão de chances, conhecida como *odds ratio*:

\[
OR=e^{\beta_j}
\]

Em termos gerais:

- \(OR>1\): associação positiva com as chances da classe positiva;
- \(OR<1\): associação negativa;
- \(OR=1\): ausência de alteração nas chances associada ao coeficiente.

Essa interpretação depende da codificação das variáveis, da escala utilizada e das condições estatísticas do modelo.

Os coeficientes do modelo específico deste projeto ainda precisam ser inspecionados antes de qualquer interpretação sobre quais características aumentam ou reduzem a probabilidade estimada de fraude.

### 3.3 Função de perda

A estimação dos parâmetros da Regressão Logística pode ser realizada por máxima verossimilhança.

A função de perda correspondente pode ser expressa pela entropia cruzada binária:

\[
L=-\frac{1}{n}\sum_{i=1}^{n}
\left[
y_i\log(p_i)+(1-y_i)\log(1-p_i)
\right]
\]

Em que:

- \(y_i\) representa a classe observada;
- \(p_i\) representa a probabilidade estimada;
- \(n\) representa a quantidade de observações.

O processo busca encontrar parâmetros que reduzam a perda entre as probabilidades estimadas e as classificações observadas.

### 3.4 Vantagens

- Estrutura estatística relativamente simples.
- Produção de probabilidades estimadas.
- Possibilidade de interpretação dos coeficientes.
- Facilidade de comparação com outros classificadores.
- Menor complexidade computacional em muitos cenários.

### 3.5 Limitações

- Representação linear no espaço dos preditores transformados.
- Necessidade de atenção à multicolinearidade.
- Dependência da representação adequada das variáveis categóricas.
- Possibilidade de desempenho limitado diante de relações complexas e não lineares.
- Sensibilidade à escala das variáveis em determinadas configurações de treinamento.

## 4. Random Forest

### 4.1 Fundamentação algorítmica

Random Forest é um algoritmo de aprendizado de máquina baseado em um conjunto de árvores de decisão.

Sua construção utiliza duas ideias principais:

1. Amostragem aleatória das observações de treinamento.
2. Seleção aleatória de subconjuntos de variáveis durante a construção das árvores.

Cada árvore produz uma previsão e o conjunto combina os resultados para produzir a classificação final ou uma estimativa probabilística.

Essa estratégia busca reduzir a variância de uma árvore individual e melhorar a capacidade de generalização.

### 4.2 Funcionamento das árvores de decisão

Uma árvore de decisão realiza divisões sucessivas do espaço de características.

Em cada divisão, o algoritmo procura uma condição que separe os registros em grupos mais homogêneos em relação à variável-alvo.

Uma medida frequentemente utilizada em árvores de classificação é a impureza de Gini:

\[
Gini=1-\sum_{k=1}^{K}p_k^2
\]

Em que:

- \(K\) representa o número de classes;
- \(p_k\) representa a proporção de observações da classe \(k\) no nó.

Quanto menor a impureza, maior a concentração de observações em uma mesma classe.

### 4.3 Agregação das previsões

Em um problema de classificação, o Random Forest combina as previsões das árvores.

De maneira simplificada, a probabilidade estimada pode ser representada pela média das probabilidades produzidas pelas árvores:

\[
\hat{P}(Y=1\mid X)=
\frac{1}{T}\sum_{t=1}^{T}P_t(Y=1\mid X)
\]

Em que:

- \(T\) representa a quantidade de árvores;
- \(P_t\) representa a estimativa produzida pela árvore \(t\).

A implementação específica do Scikit-learn utiliza os mecanismos de agregação definidos pelo classificador.

### 4.4 Vantagens

- Capacidade de representar relações não lineares.
- Possibilidade de identificar interações entre variáveis.
- Combinação de múltiplas árvores de decisão.
- Menor dependência de hipóteses lineares.
- Disponibilidade de medidas de importância de variáveis.

### 4.5 Limitações

- Maior complexidade em comparação com modelos lineares simples.
- Menor facilidade de interpretação global.
- Potencial aumento do custo computacional.
- Necessidade de controle dos hiperparâmetros.
- Importância de variáveis não deve ser interpretada automaticamente como causalidade.

## 5. Comparação metodológica dos algoritmos

Os dois modelos apresentam características complementares.

| Critério | Regressão Logística | Random Forest |
|---|---|---|
| Natureza | Estatística paramétrica | Aprendizado baseado em árvores |
| Relações não lineares | Limitada sem transformações | Maior capacidade |
| Interpretação | Coeficientes e odds ratios | Importância e análise das árvores |
| Interações | Dependem da especificação | Podem ser representadas pelas árvores |
| Escalonamento | Pode ser relevante | Geralmente menos necessário |
| Complexidade | Geralmente menor | Geralmente maior |
| Probabilidades | Saída probabilística | Probabilidades agregadas |

A comparação permite investigar se uma estrutura estatística mais simples apresenta desempenho competitivo em relação a um conjunto de árvores de decisão.

## 6. Estratégia de treinamento e teste

A aplicação reporta uma estratégia de separação temporal:

- Dados de 2023 e 2024: treinamento.
- Dados de 2025: teste.

Essa abordagem procura avaliar os modelos em registros de um período posterior ao treinamento.

A estratégia é especialmente relevante em seguradoras, nas quais os padrões de ocorrência de sinistros e fraude podem sofrer alterações ao longo do tempo.

A avaliação temporal também permite investigar a capacidade de generalização diante de mudanças na população observada.

Entretanto, para uma auditoria metodológica completa, é necessário confirmar nos códigos originais:

- Os critérios exatos de separação dos dados;
- A execução das transformações;
- A seleção de hiperparâmetros;
- A eventual utilização de validação cruzada;
- A ausência de vazamento de informações.

## 7. Limiar de classificação

Os modelos produzem probabilidades estimadas. A decisão de classificar um registro como suspeito depende de um limiar.

A aplicação utiliza:

| Modelo | Limiar |
|---|---:|
| Regressão Logística | 0,50 |
| Random Forest | 0,25 |

A regra geral de classificação é:

\[
\hat{Y}=
\begin{cases}
1, & \text{se } \hat{P}(Y=1\mid X)\geq t\\
0, & \text{caso contrário}
\end{cases}
\]

Em que \(t\) representa o limiar adotado.

A redução do limiar tende a aumentar a quantidade de registros classificados como suspeitos, podendo elevar o recall e também o volume de falsos positivos.

A elevação do limiar tende a reduzir o número de alertas, mas pode aumentar a quantidade de fraudes não identificadas.

Os limiares atuais são configurações utilizadas pela aplicação. Não há evidência suficiente para afirmar que foram selecionados por otimização econômica ou por um processo formal de calibração.

## 8. Relação entre modelagem e desbalanceamento

A base apresenta 6,76% de registros classificados como fraude.

Esse desbalanceamento pode influenciar o processo de aprendizagem e a interpretação das métricas.

Uma estratégia de modelagem precisa considerar que a classe majoritária não deve dominar a avaliação do desempenho.

Entre as abordagens que podem ser investigadas em futuras versões estão:

- Ajuste de pesos das classes;
- Amostragem controlada;
- Métodos de redução da classe majoritária;
- Métodos de aumento da classe minoritária;
- Otimização do limiar;
- Avaliação baseada em métricas específicas para a classe positiva.

Essas abordagens não devem ser consideradas implementadas no projeto atual sem confirmação nos scripts de treinamento.

## 9. Resultados comparativos disponíveis

A aplicação apresenta os seguintes resultados no conjunto de teste:

| Métrica | Regressão Logística | Random Forest |
|---|---:|---:|
| Acurácia | 69,24% | 77,56% |
| Precisão | 14,32% | 17,64% |
| Recall | 66,18% | 58,19% |
| F1-score | 23,55% | 27,08% |
| ROC-AUC | 0,7631 | 0,7462 |
| PR-AUC | 0,2244 | 0,1954 |

A Regressão Logística apresenta maior recall e PR-AUC, enquanto o Random Forest apresenta maior acurácia, precisão e F1-score.

Esses resultados demonstram que os algoritmos respondem de maneira diferente aos critérios de avaliação.

A interpretação detalhada das métricas, matrizes de confusão e impactos operacionais será apresentada no capítulo específico de avaliação estatística.

## 10. Critérios de seleção do modelo

A escolha do modelo deve considerar o objetivo operacional da seguradora.

Quando a prioridade é ampliar a identificação de fraudes, o recall possui relevância elevada.

Quando a capacidade de investigação é limitada, a precisão e o volume de alertas também se tornam importantes.

A seleção deverá considerar:

1. Capacidade de identificar fraudes.
2. Volume de falsos positivos.
3. Quantidade de falsos negativos.
4. Desempenho global.
5. Estabilidade temporal.
6. Custo operacional das investigações.
7. Exposição financeira potencial.
8. Interpretabilidade e governança.

Não existe uma métrica universalmente suficiente para selecionar um modelo de prevenção de fraudes.

## 11. Recomendações para evolução da modelagem

Para versões futuras, recomenda-se:

- Realizar validação temporal em múltiplos períodos.
- Investigar a calibração das probabilidades.
- Comparar diferentes limiares de classificação.
- Avaliar pesos de classe e estratégias de balanceamento.
- Realizar análise de importância e contribuição das variáveis.
- Avaliar estabilidade do desempenho ao longo do tempo.
- Comparar modelos adicionais de classificação.
- Construir uma função de custo para apoiar a seleção econômica.
- Registrar hiperparâmetros e métricas no MLflow.
- Preservar a rastreabilidade dos experimentos.

## 12. Considerações finais

A estratégia de modelagem combina duas abordagens complementares para o problema de classificação de fraudes em seguradoras.

A Regressão Logística oferece uma referência estatística com maior facilidade de interpretação dos coeficientes, enquanto o Random Forest amplia a capacidade de representar relações não lineares e interações entre variáveis.

Os resultados disponíveis demonstram que o melhor modelo depende do critério utilizado e das prioridades operacionais.

A decisão final deverá considerar conjuntamente desempenho estatístico, capacidade investigativa, custos dos erros, estabilidade temporal e governança.