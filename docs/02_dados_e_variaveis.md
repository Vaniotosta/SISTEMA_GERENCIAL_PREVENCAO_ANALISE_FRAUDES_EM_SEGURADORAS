# Dados e Caracterização das Variáveis

## 1. Introdução

A qualidade dos dados constitui um dos principais fatores que determinam a confiabilidade de sistemas de aprendizado de máquina. Em problemas de prevenção de fraudes, a análise das características dos registros permite compreender quais informações estão disponíveis para os modelos e como essas informações podem contribuir para a identificação de padrões associados a comportamentos suspeitos.

Este capítulo apresenta a caracterização estrutural da base utilizada no projeto, a variável-alvo e as 22 variáveis informadas como entradas dos modelos preditivos.

A descrição concentra-se na função analítica das variáveis. Não são atribuídas distribuições, correlações ou propriedades estatísticas específicas sem evidências produzidas pela análise efetiva dos dados.

## 2. Caracterização geral da base

A base utilizada no projeto apresenta a seguinte estrutura quantitativa:

| Indicador | Quantidade |
|---|---:|
| Registros totais | 20.000 |
| Variáveis inicialmente disponíveis | 33 |
| Variáveis utilizadas como entradas | 22 |
| Registros classificados como fraude | 1.352 |
| Registros classificados como não fraude | 18.648 |

A variável-alvo apresenta duas categorias: fraude e não fraude.

A distribuição das classes é:

| Classe | Quantidade | Participação |
|---|---:|---:|
| Fraude | 1.352 | 6,76% |
| Não fraude | 18.648 | 93,24% |
| Total | 20.000 | 100% |

A participação minoritária da classe fraude caracteriza um cenário de desbalanceamento, aspecto que influencia a seleção das métricas de avaliação e a interpretação dos resultados.

## 3. Variável-alvo

A variável-alvo representa a classificação histórica do registro quanto à ocorrência de fraude.

Sua finalidade é fornecer a referência utilizada no aprendizado supervisionado.

| Classe | Significado |
|---|---|
| 0 | Não fraude |
| 1 | Fraude |

O modelo aprende relações estatísticas entre as variáveis explicativas e a classificação observada nos dados de treinamento.

É importante distinguir a classificação histórica da previsão produzida pelo modelo. A primeira representa o rótulo utilizado como referência; a segunda representa uma estimativa probabilística que deve ser validada.

## 4. Variáveis utilizadas pelos modelos

Foram informadas 22 variáveis como entradas dos modelos. Elas podem ser organizadas em grupos analíticos para facilitar a interpretação.

### 4.1 Características cadastrais e do segurado

| Variável | Tipo informado | Função analítica |
|---|---|---|
| `idade` | Numérica | Representar a idade do segurado. |
| `tempo_cliente_anos` | Numérica | Representar o tempo de relacionamento com a seguradora. |
| `estado_civil` | Categórica | Representar a condição civil informada. |
| `renda_mensal` | Numérica | Representar a renda mensal informada. |

Essas variáveis permitem caracterizar aspectos cadastrais e do relacionamento do segurado com a organização.

Sua utilização deve observar critérios de qualidade, pertinência e governança, evitando interpretações determinísticas sobre o comportamento individual.

### 4.2 Características financeiras e contratuais

| Variável | Tipo informado | Função analítica |
|---|---|---|
| `score_credito` | Numérica | Representar a pontuação de crédito disponível. |
| `tipo_cobertura` | Categórica | Identificar a modalidade de cobertura contratada. |
| `valor_segurado` | Numérica | Representar o valor segurado. |
| `franquia` | Numérica | Representar o valor da franquia contratual. |
| `premio_anual` | Numérica | Representar o prêmio anual do seguro. |
| `canal_venda` | Categórica | Identificar o canal de comercialização. |
| `alteracoes_apolice_90d` | Numérica | Representar a quantidade de alterações na apólice em uma janela de 90 dias. |

Esse grupo reúne informações relacionadas à estrutura financeira e às condições contratuais.

A análise conjunta dessas características pode auxiliar na identificação de padrões estatísticos relacionados às condições do seguro e ao histórico recente de alterações contratuais.

Entretanto, nenhuma dessas características constitui, isoladamente, evidência de fraude.

### 4.3 Características do sinistro

| Variável | Tipo informado | Função analítica |
|---|---|---|
| `tipo_sinistro` | Categórica | Identificar a natureza do sinistro. |
| `hora_sinistro` | Numérica | Representar o horário de ocorrência. |
| `boletim_ocorrencia` | Categórica | Indicar a informação relativa ao boletim de ocorrência. |
| `qtd_testemunhas` | Numérica | Representar a quantidade de testemunhas informada. |
| `houve_vitima` | Categórica | Indicar a existência de vítimas. |
| `oficina_credenciada` | Categórica | Representar a informação sobre oficina credenciada. |
| `valor_sinistro_num` | Numérica | Representar o valor numérico do sinistro. |
| `dias_ate_aviso` | Numérica | Representar o intervalo entre a ocorrência e o aviso do sinistro. |

As variáveis desse grupo estão relacionadas às circunstâncias e às características do evento comunicado à seguradora.

Elas podem oferecer informações relevantes para a análise de consistência dos registros, desde que sejam consideradas em conjunto e interpretadas de acordo com o contexto operacional.

### 4.4 Características geográficas e temporais

| Variável | Tipo informado | Função analítica |
|---|---|---|
| `uf` | Categórica | Identificar a unidade federativa associada ao registro. |
| `mes_sinistro` | Numérica | Representar o mês de ocorrência. |
| `dia_semana_sinistro` | Numérica | Representar o dia da semana da ocorrência. |

Essas variáveis permitem representar dimensões geográficas e temporais dos registros.

Em aplicações de prevenção de fraudes, características temporais podem auxiliar na identificação de padrões de concentração de ocorrências e possíveis mudanças de comportamento ao longo do tempo.

A análise dessas dimensões exige atenção a sazonalidade, distribuição dos registros e possíveis diferenças entre períodos.

## 5. Organização das variáveis por natureza

Considerando os tipos informados, as variáveis podem ser agrupadas em:

- Numéricas: idade, tempo de relacionamento, indicadores financeiros, quantidades e medidas temporais.
- Categóricas: estado civil, cobertura, canal de venda, tipo de sinistro, informações de ocorrência e unidade federativa.

A distinção é metodologicamente relevante porque variáveis numéricas e categóricas podem exigir tratamentos diferentes durante a preparação dos dados.

Por exemplo, variáveis categóricas podem necessitar de codificação para utilização em determinados algoritmos. Variáveis numéricas podem exigir avaliação de escala, valores extremos e consistência.

Este documento registra a necessidade dessas verificações, mas não afirma quais procedimentos específicos foram aplicados no treinamento original, pois isso depende da inspeção dos artefatos e dos códigos de preparação.

## 6. Variáveis com indicação de opcionalidade

Na estrutura de entrada da aplicação, quatro campos aparecem identificados como opcionais:

- `score_credito`;
- `renda_mensal`;
- `qtd_testemunhas`;
- `oficina_credenciada`.

A indicação de opcionalidade na interface significa que esses campos podem não ser obrigatórios no preenchimento de uma consulta individual.

Isso não comprova, por si só, a existência de valores ausentes na base original nem permite concluir qual estratégia de tratamento de dados faltantes foi utilizada durante o treinamento.

Para uma documentação metodológica completa, será necessário verificar o pipeline original de preparação e transformação dos dados.

## 7. Relevância analítica dos grupos de variáveis

A organização das variáveis em grupos permite estruturar futuras investigações sobre a contribuição das características para o desempenho preditivo.

Algumas linhas de análise que podem ser desenvolvidas são:

1. Avaliar a relação entre características contratuais e a classificação histórica de fraude.
2. Investigar padrões temporais de ocorrência dos sinistros.
3. Examinar a influência de características financeiras sobre as probabilidades estimadas.
4. Verificar a importância relativa das variáveis nos modelos.
5. Avaliar possíveis diferenças de desempenho entre grupos e regiões.
6. Identificar variáveis redundantes, inconsistentes ou com baixa contribuição preditiva.

Essas análises deverão ser realizadas com os dados disponíveis e documentadas com seus respectivos resultados.

## 8. Cuidados metodológicos e de governança

A utilização de dados cadastrais, financeiros, geográficos e relacionados a sinistros exige atenção a aspectos de qualidade e governança.

Entre os principais cuidados estão:

**Qualidade dos dados:** verificar consistência dos valores, duplicidades, dados ausentes e registros incompatíveis.

**Temporalidade:** assegurar que as variáveis utilizadas na previsão correspondam a informações disponíveis no momento em que a decisão seria tomada.

**Vazamento de dados:** evitar a utilização de informações que revelem direta ou indiretamente a classificação final do sinistro.

**Representatividade:** avaliar se os registros utilizados representam adequadamente os diferentes períodos e contextos de operação.

**Privacidade:** restringir o acesso às informações pessoais e financeiras e observar os princípios aplicáveis da Lei Geral de Proteção de Dados Pessoais (LGPD).

**Justiça algorítmica:** avaliar se o sistema produz diferenças injustificadas de desempenho entre grupos e se as variáveis utilizadas são adequadas ao objetivo analítico.

## 9. Limitações da caracterização disponível

A caracterização apresentada neste documento está baseada nas quantidades e nos nomes das variáveis identificados no projeto.

Ainda precisam ser comprovados por meio da base original ou dos artefatos de análise:

- Distribuições estatísticas das variáveis;
- Média, mediana, desvio-padrão e quartis;
- Frequências das categorias;
- Percentuais efetivos de valores ausentes;
- Presença e tratamento de valores extremos;
- Correlações e associações entre variáveis;
- Procedimentos de codificação e transformação;
- Critérios de seleção das 22 variáveis.

Esses elementos serão incorporados à documentação de análise exploratória e preparação dos dados após a obtenção das evidências correspondentes.

## 10. Considerações finais

A base do projeto reúne informações cadastrais, contratuais, financeiras, geográficas e relacionadas aos sinistros, permitindo estruturar um problema de classificação supervisionada.

A organização das 22 variáveis em grupos analíticos facilita a interpretação do problema e estabelece uma referência para as próximas etapas da documentação.

A caracterização estrutural constitui o ponto de partida para a análise exploratória, a avaliação da qualidade dos dados e a compreensão das relações entre as variáveis e a ocorrência histórica de fraudes.