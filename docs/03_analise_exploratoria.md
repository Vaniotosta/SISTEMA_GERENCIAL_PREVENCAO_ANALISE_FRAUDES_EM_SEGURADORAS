# Análise Exploratória de Dados (EDA)

## 1. Introdução

A Análise Exploratória de Dados (Exploratory Data Analysis — EDA) constitui uma etapa fundamental do processo de Ciência de Dados. Seu objetivo é compreender as características da base, identificar padrões, avaliar a qualidade das informações e investigar possíveis relações entre as variáveis explicativas e a variável-alvo.

No contexto da prevenção de fraudes em seguradoras, a EDA permite investigar a distribuição dos registros, a concentração de ocorrências fraudulentas, o comportamento das variáveis financeiras e contratuais e possíveis padrões temporais e geográficos.

A análise exploratória também orienta decisões relacionadas à preparação dos dados, seleção de atributos e escolha dos procedimentos estatísticos e computacionais.

Este capítulo apresenta os fundamentos e os resultados quantitativos já disponíveis no projeto, diferenciando evidências confirmadas de análises que ainda dependem da execução sobre a base original.

## 2. Objetivos da análise exploratória

A EDA possui os seguintes objetivos:

- Compreender a distribuição geral dos registros.
- Avaliar o equilíbrio entre as classes.
- Identificar características das variáveis numéricas e categóricas.
- Investigar valores ausentes e inconsistências.
- Identificar possíveis valores extremos.
- Investigar padrões temporais e geográficos.
- Examinar associações entre as variáveis explicativas e a ocorrência de fraude.
- Produzir evidências que orientem a preparação e a modelagem.

## 3. Análise da distribuição da variável-alvo

A base apresenta 20.000 registros, distribuídos entre duas classes.

| Classificação | Quantidade | Participação |
|---|---:|---:|
| Não fraude | 18.648 | 93,24% |
| Fraude | 1.352 | 6,76% |
| Total | 20.000 | 100% |

A distribuição evidencia um desbalanceamento significativo entre as classes.

A classe não fraude representa 93,24% dos registros, enquanto a classe fraude corresponde a 6,76%.

Essa diferença possui implicações diretas para a modelagem. Um classificador que simplesmente atribuísse a classe majoritária a todos os registros alcançaria 93,24% de acurácia na base completa, sem identificar nenhuma fraude.

Portanto, a avaliação do sistema precisa considerar métricas que representem adequadamente o desempenho na classe minoritária.

## 4. Distribuição do conjunto de teste

A avaliação temporal de 2025 apresenta a seguinte composição:

| Classificação | Quantidade | Participação |
|---|---:|---:|
| Não fraude | 6.173 | 92,84% |
| Fraude | 476 | 7,16% |
| Total | 6.649 | 100% |

A prevalência de fraude no conjunto de teste é de aproximadamente 7,16%.

Esse indicador representa a proporção de registros fraudulentos entre os registros avaliados.

A diferença entre a prevalência da base completa e a do conjunto de teste demonstra a importância de examinar separadamente as distribuições dos períodos de treinamento e teste.

A comparação temporal deve ser aprofundada para verificar estabilidade da população, alterações na frequência de fraudes e possíveis mudanças no comportamento dos registros.

## 5. Estatística descritiva das variáveis numéricas

As variáveis numéricas representam características cadastrais, financeiras, contratuais e temporais.

A análise descritiva deve contemplar medidas de tendência central, dispersão e posição.

### 5.1 Medidas de tendência central

**Média aritmética**

Representa o valor médio de uma variável e pode ser influenciada por observações extremas.

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

**Mediana**

Representa o valor central de uma distribuição ordenada. É particularmente útil quando existem assimetrias ou valores extremos.

### 5.2 Medidas de dispersão

**Desvio-padrão**

Representa a dispersão dos valores em torno da média.

\[
s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}
\]

**Amplitude**

Corresponde à diferença entre o maior e o menor valor observado.

**Intervalo interquartil**

É calculado pela diferença entre o terceiro e o primeiro quartis:

\[
IQR=Q_3-Q_1
\]

Essas medidas permitem avaliar a variabilidade das características e identificar distribuições que possam exigir atenção durante a preparação dos dados.

### 5.3 Variáveis prioritárias para análise

Recomenda-se examinar especialmente:

- `idade`;
- `tempo_cliente_anos`;
- `score_credito`;
- `renda_mensal`;
- `valor_segurado`;
- `franquia`;
- `premio_anual`;
- `alteracoes_apolice_90d`;
- `hora_sinistro`;
- `qtd_testemunhas`;
- `valor_sinistro_num`;
- `dias_ate_aviso`;
- `mes_sinistro`;
- `dia_semana_sinistro`.

A análise deve ser realizada tanto para a população completa quanto separadamente por classe, permitindo investigar diferenças entre registros fraudulentos e não fraudulentos.

Os valores efetivos de média, mediana, quartis e desvio-padrão ainda precisam ser calculados a partir da base original.

## 6. Análise das variáveis categóricas

As variáveis categóricas representam informações relacionadas ao perfil cadastral, às condições contratuais e às características do sinistro.

Entre elas estão:

- `estado_civil`;
- `tipo_cobertura`;
- `canal_venda`;
- `tipo_sinistro`;
- `uf`;
- `boletim_ocorrencia`;
- `houve_vitima`;
- `oficina_credenciada`.

A análise deve contemplar:

1. Frequência absoluta de cada categoria.
2. Frequência relativa em percentual.
3. Distribuição das categorias por classificação de fraude.
4. Categorias com baixa frequência.
5. Possíveis inconsistências de preenchimento.

A análise percentual por classe é especialmente importante. Uma categoria com grande número de fraudes pode simplesmente apresentar grande volume de registros totais. Por isso, é necessário avaliar também a proporção de fraude dentro de cada categoria.

Não se deve interpretar uma associação observada como evidência de causalidade.

## 7. Investigação de valores ausentes

A presença de valores ausentes pode comprometer a qualidade das análises e a capacidade de generalização dos modelos.

A investigação deve identificar:

- Quantidade de valores ausentes por variável.
- Percentual de ausência em relação ao total.
- Diferenças de ausência entre os períodos.
- Possíveis relações entre ausência e classificação de fraude.

Quatro variáveis aparecem como opcionais na interface:

- `score_credito`;
- `renda_mensal`;
- `qtd_testemunhas`;
- `oficina_credenciada`.

Essa característica da interface não comprova que existam valores ausentes na base original.

A confirmação depende da análise direta dos dados utilizados no treinamento.

## 8. Investigação de valores extremos

Valores extremos podem influenciar medidas estatísticas e o comportamento dos algoritmos.

No contexto de seguros, variáveis como valor segurado, prêmio anual e valor do sinistro merecem atenção especial.

Uma técnica exploratória possível é a utilização do intervalo interquartil.

Considerando:

\[
IQR=Q_3-Q_1
\]

Podem ser sinalizados como potenciais valores extremos os registros que estejam abaixo de:

\[
Q_1-1,5(IQR)
\]

ou acima de:

\[
Q_3+1,5(IQR)
\]

Esse procedimento é uma ferramenta de investigação, não uma regra automática para excluir registros.

Valores elevados podem representar sinistros legítimos de grande porte e, portanto, precisam ser avaliados considerando o contexto do negócio.

## 9. Análise de correlação e associação

A investigação das relações entre variáveis pode contribuir para identificar redundâncias, padrões e possíveis relações com a variável-alvo.

Para variáveis numéricas, uma medida possível é a correlação de Pearson:

\[
r_{xy}=
\frac{\operatorname{Cov}(X,Y)}
{\sigma_X\sigma_Y}
\]

Essa medida avalia relações lineares entre duas variáveis numéricas.

Entretanto, a correlação de Pearson não identifica adequadamente todas as relações não lineares e não deve ser interpretada como evidência causal.

Para variáveis categóricas, podem ser utilizadas tabelas de contingência e medidas de associação apropriadas.

A escolha das medidas deve considerar a natureza das variáveis e as características das distribuições observadas.

## 10. Análise temporal

O projeto utiliza uma separação temporal entre treinamento e teste:

- Treinamento: 2023 e 2024.
- Teste: 2025.

Essa estrutura permite investigar a capacidade de generalização em um período posterior.

A análise temporal deve considerar:

- Frequência mensal dos sinistros.
- Participação mensal de fraudes.
- Variação da prevalência ao longo dos períodos.
- Possíveis padrões por dia da semana.
- Distribuição dos horários de ocorrência.
- Alterações no comportamento das variáveis entre treinamento e teste.

Uma alteração expressiva na distribuição dos dados ao longo do tempo pode indicar mudança de perfil da população ou possível *data drift*.

A existência e a intensidade dessas alterações precisam ser verificadas empiricamente.

## 11. Análise geográfica

A variável `uf` permite investigar a distribuição dos registros por unidade federativa.

Entre as análises recomendadas estão:

- Volume de sinistros por unidade federativa.
- Participação de fraudes por unidade federativa.
- Taxa de fraude dentro de cada região.
- Comparação da distribuição entre treinamento e teste.

A interpretação deve considerar o volume de registros de cada região. Comparar apenas quantidades absolutas pode produzir conclusões equivocadas quando as populações possuem tamanhos diferentes.

Também é importante avaliar a estabilidade das estimativas em regiões com poucos registros.

## 12. Relação entre EDA e modelagem

A análise exploratória fundamenta diversas decisões posteriores:

| Evidência investigada | Implicação metodológica |
|---|---|
| Desbalanceamento entre classes | Avaliar recall, precision e PR-AUC. |
| Valores ausentes | Definir estratégia de tratamento. |
| Valores extremos | Investigar consistência e impacto nos modelos. |
| Variáveis categóricas | Avaliar codificação apropriada. |
| Diferentes escalas numéricas | Avaliar necessidade de padronização. |
| Associação entre variáveis | Investigar redundância e contribuição preditiva. |
| Variação temporal | Avaliar estabilidade e generalização. |

As decisões efetivamente adotadas devem ser confirmadas nos scripts ou pipelines originais de preparação dos dados.

## 13. Limitações da análise disponível

Os resultados quantitativos confirmados neste capítulo são a distribuição geral das classes e a composição do conjunto de teste.

Ainda não estão documentados, com evidências da base original:

- Médias e medianas das variáveis;
- Desvios-padrão e quartis;
- Distribuições categóricas;
- Percentuais de valores ausentes;
- Análise de valores extremos;
- Correlações;
- Associações estatísticas;
- Distribuições geográficas;
- Evolução temporal detalhada.

Essas análises não devem ser substituídas por valores estimados ou exemplos fictícios.

A documentação deverá ser atualizada quando os dados originais ou os artefatos de exploração estiverem disponíveis.

## 14. Considerações finais

A EDA estabelece a base para compreender o comportamento dos registros e avaliar a adequação dos dados à construção dos modelos preditivos.

A distribuição desbalanceada da variável-alvo constitui uma evidência relevante já identificada e justifica a utilização de métricas específicas para a classe fraudulenta.

A continuidade da análise deve priorizar estatística descritiva, investigação de valores ausentes, análise de associações e avaliação da estabilidade temporal.

Essas etapas permitirão fortalecer a rastreabilidade das decisões metodológicas e a confiabilidade das futuras versões do sistema.