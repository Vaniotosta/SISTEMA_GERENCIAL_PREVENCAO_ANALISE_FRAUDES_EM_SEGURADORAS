# Pré-processamento e Engenharia de Atributos

## 1. Introdução

O pré-processamento constitui uma etapa fundamental do desenvolvimento de modelos de aprendizado de máquina. Seu objetivo é transformar os dados originais em uma estrutura consistente, adequada aos requisitos dos algoritmos e compatível com o processo de treinamento e inferência.

Em sistemas de prevenção de fraudes em seguradoras, essa etapa exige atenção especial à qualidade das informações cadastrais, financeiras, contratuais e relacionadas aos sinistros.

Problemas como valores ausentes, inconsistências, diferentes escalas de mensuração, categorias não padronizadas e informações temporais podem comprometer a qualidade das previsões.

Este capítulo apresenta os fundamentos metodológicos do pré-processamento e da engenharia de atributos aplicáveis ao projeto, distinguindo os procedimentos recomendados daqueles cuja execução original ainda precisa ser comprovada.

## 2. Objetivos do pré-processamento

O pré-processamento busca:

- Melhorar a consistência dos dados utilizados pelos modelos.
- Identificar e tratar problemas de qualidade.
- Preparar variáveis numéricas e categóricas.
- Evitar incompatibilidades entre treinamento e inferência.
- Reduzir riscos de vazamento de informações.
- Garantir reprodutibilidade das transformações.
- Preservar a correspondência entre as variáveis utilizadas no treinamento e na aplicação.

Uma preparação adequada também contribui para a estabilidade dos modelos quando novos registros são submetidos à análise.

## 3. Tipologia das variáveis

As 22 variáveis informadas como entradas dos modelos apresentam diferentes naturezas.

**Variáveis numéricas:**

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

**Variáveis categóricas:**

- `estado_civil`;
- `tipo_cobertura`;
- `canal_venda`;
- `tipo_sinistro`;
- `uf`;
- `boletim_ocorrencia`;
- `houve_vitima`;
- `oficina_credenciada`.

A identificação da natureza de cada variável é importante para determinar os procedimentos de transformação adequados.

## 4. Tratamento de valores ausentes

Valores ausentes podem surgir por falhas de preenchimento, indisponibilidade de informações ou características próprias dos processos de negócio.

Sua presença deve ser investigada antes da definição de qualquer estratégia de tratamento.

Entre as abordagens metodológicas possíveis estão:

**Imputação pela mediana**

Pode ser utilizada em variáveis numéricas quando a mediana representa adequadamente a distribuição e oferece maior robustez diante de valores extremos.

**Imputação pela média**

Pode ser considerada em distribuições sem assimetria acentuada e sem influência excessiva de observações extremas.

**Categoria explícita para ausência**

Em determinadas variáveis categóricas, pode ser relevante preservar a informação de ausência por meio de uma categoria específica.

**Indicador de ausência**

Uma variável adicional pode registrar se determinado campo estava ausente, quando essa informação tiver significado analítico.

A escolha deve considerar a distribuição, o contexto operacional e o comportamento dos dados.

No projeto, os campos `score_credito`, `renda_mensal`, `qtd_testemunhas` e `oficina_credenciada` aparecem como opcionais na interface. Isso não comprova a existência de valores ausentes na base original nem identifica o método de tratamento utilizado no treinamento.

A estratégia efetivamente aplicada deverá ser confirmada no pipeline original.

## 5. Codificação de variáveis categóricas

Algoritmos de aprendizado de máquina geralmente exigem que as variáveis categóricas sejam representadas numericamente.

Uma abordagem possível é o One-Hot Encoding, que transforma categorias em variáveis indicadoras.

Por exemplo, uma variável hipotética de tipo de cobertura pode ser representada por diferentes colunas binárias.

Outra possibilidade é utilizar codificação ordinal, desde que exista uma relação de ordem legítima entre as categorias.

A escolha deve considerar o algoritmo utilizado e a natureza da variável.

Na Regressão Logística, a codificação adequada é especialmente importante, pois a representação numérica influencia diretamente a interpretação da relação entre as características e a probabilidade estimada.

No Random Forest, as transformações também precisam respeitar os requisitos de entrada do pipeline utilizado.

Não há evidência suficiente, até o momento, para afirmar qual técnica de codificação foi aplicada originalmente no projeto.

## 6. Padronização e escalonamento de variáveis numéricas

Variáveis numéricas podem apresentar escalas bastante diferentes.

Por exemplo, idade, quantidade de alterações contratuais e valor segurado podem possuir magnitudes distintas.

Uma técnica frequentemente utilizada é a padronização pelo escore Z:

\[
z=\frac{x-\mu}{\sigma}
\]

Em que:

- \(x\) representa o valor original;
- \(\mu\) representa a média da variável;
- \(\sigma\) representa o desvio-padrão;
- \(z\) representa o valor padronizado.

A padronização pode ser relevante para a Regressão Logística, especialmente em procedimentos de regularização e otimização numérica.

O Random Forest, por ser baseado em divisões realizadas por árvores de decisão, geralmente apresenta menor dependência da escala das variáveis numéricas.

Entretanto, a decisão sobre escalonamento deve ser documentada a partir do pipeline efetivamente utilizado.

Quando houver padronização ou outra transformação, os parâmetros devem ser ajustados exclusivamente com os dados de treinamento e posteriormente aplicados ao conjunto de teste e aos novos registros.

## 7. Engenharia de atributos

A engenharia de atributos consiste na criação, transformação ou reorganização de variáveis com o objetivo de representar melhor o fenômeno investigado.

No contexto de seguros, algumas possibilidades de investigação incluem:

**Características temporais**

- Período entre ocorrência e comunicação do sinistro;
- Mês e dia da semana;
- Faixas de horário;
- Comportamento temporal dos registros.

**Características contratuais**

- Histórico de alterações da apólice;
- Relações entre prêmio anual e valor segurado;
- Indicadores associados à franquia;
- Tempo de relacionamento com a seguradora.

**Características financeiras**

- Relação entre valor do sinistro e valor segurado;
- Relação entre prêmio e valor segurado;
- Indicadores de magnitude financeira do evento.

Essas possibilidades representam oportunidades de evolução metodológica. Não devem ser interpretadas como atributos comprovadamente criados ou utilizados no treinamento atual.

A inclusão de novas características deverá ser acompanhada de avaliação de relevância, consistência, disponibilidade temporal e contribuição efetiva para o desempenho dos modelos.

## 8. Controle de vazamento de dados

O vazamento de dados (*data leakage*) ocorre quando informações que não estariam disponíveis no momento da previsão influenciam o treinamento ou a avaliação do modelo.

Em prevenção de fraudes, esse problema merece atenção especial.

Por exemplo, informações produzidas após uma investigação, confirmação de irregularidade ou conclusão do processo de regulação não devem ser utilizadas como variáveis preditoras quando o objetivo é identificar suspeitas antes dessas etapas.

A prevenção de vazamento exige:

1. Definir o momento exato em que a previsão será realizada.
2. Identificar quais informações estavam disponíveis nesse momento.
3. Excluir atributos derivados da decisão final ou de etapas posteriores.
4. Ajustar transformações exclusivamente com dados de treinamento.
5. Preservar a separação temporal entre treinamento e teste.

A utilização de dados de 2023 e 2024 para treinamento e 2025 para teste constitui uma estratégia temporal relevante, mas não comprova isoladamente a ausência de vazamento.

É necessário verificar também a origem temporal de cada variável.

## 9. Consistência entre treinamento e inferência

Um requisito essencial é que os dados apresentados à aplicação sigam a mesma estrutura e as mesmas transformações utilizadas durante o treinamento.

Isso inclui:

- Nomes e ordem das variáveis;
- Tipos de dados;
- Codificação das categorias;
- Tratamento de valores ausentes;
- Transformações numéricas;
- Estrutura de entrada dos modelos.

A aplicação atual carrega os modelos por meio de `mlflow.sklearn.load_model`.

A existência dos artefatos serializados permite carregar os modelos, mas é necessário verificar se todas as transformações utilizadas no treinamento estão incorporadas aos pipelines registrados.

Caso estejam separadas do modelo, será necessário garantir sua reprodução na aplicação.

Essa verificação é importante para evitar diferenças entre o ambiente de desenvolvimento e o ambiente de produção.

## 10. Reprodutibilidade do processo

Um processo de preparação de dados deve ser reproduzível.

Para isso, recomenda-se registrar:

- Versão da base utilizada;
- Relação das variáveis selecionadas;
- Procedimentos de limpeza;
- Métodos de imputação;
- Codificação das variáveis;
- Transformações numéricas;
- Parâmetros dos pipelines;
- Versões das bibliotecas;
- Data e identificação dos experimentos.

O MLflow pode contribuir para a rastreabilidade de parâmetros, métricas, artefatos e versões dos modelos.

A evolução da arquitetura com Databricks poderá ampliar a organização dos dados e a reprodução das etapas de preparação.

## 11. Procedimentos que precisam ser confirmados

Para completar a documentação do pré-processamento original, será necessário inspecionar os códigos ou artefatos de treinamento e confirmar:

| Procedimento | Situação documental |
|---|---|
| Seleção das 22 variáveis | Quantidade e nomes conhecidos |
| Tratamento de valores ausentes | Pendente de confirmação |
| Codificação categórica | Pendente de confirmação |
| Padronização numérica | Pendente de confirmação |
| Tratamento de valores extremos | Pendente de confirmação |
| Engenharia de atributos | Pendente de confirmação |
| Exclusão de variáveis com vazamento | Pendente de auditoria |
| Incorporação das transformações aos modelos | Pendente de inspeção |

Essa distinção evita atribuir ao projeto procedimentos que não foram comprovados.

## 12. Recomendações para evolução

Para as próximas versões, recomenda-se:

1. Construir um pipeline integrado de preparação e modelagem.
2. Automatizar a validação dos tipos e da estrutura dos dados.
3. Implementar verificações de valores ausentes e inconsistências.
4. Registrar todas as transformações utilizadas.
5. Garantir a separação temporal dos dados.
6. Implementar testes para verificar a compatibilidade entre treinamento e inferência.
7. Avaliar a contribuição de novos atributos por meio de experimentos controlados.
8. Registrar versões dos dados e dos modelos no ambiente de experimentação.

## 13. Considerações finais

O pré-processamento e a engenharia de atributos são componentes fundamentais para a confiabilidade de sistemas de classificação de fraudes.

A qualidade das previsões depende não apenas da escolha do algoritmo, mas também da consistência das informações, da adequação das transformações e da ausência de vazamento de dados.

A documentação do projeto estabelece os fundamentos necessários para auditar o processo original e orientar sua evolução para uma arquitetura mais rastreável, reproduzível e adequada ao ambiente operacional de uma seguradora.