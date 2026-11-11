# Validação Temporal, Monitoramento e Drift dos Modelos

## 1. Introdução

Modelos de Machine Learning aplicados à prevenção de fraudes precisam manter desempenho consistente ao longo do tempo.

Em uma seguradora, o comportamento dos segurados, os padrões de sinistros, os canais de contratação e as estratégias utilizadas por fraudadores podem sofrer alterações.

Essas mudanças podem comprometer a capacidade de generalização dos modelos desenvolvidos a partir de dados históricos.

Por essa razão, a avaliação de um modelo não deve terminar após a etapa de treinamento e teste.

É necessário estabelecer mecanismos de validação temporal, monitoramento estatístico, acompanhamento operacional e identificação de possíveis mudanças nos dados.

Este capítulo apresenta os fundamentos e as estratégias recomendadas para acompanhar a estabilidade dos modelos de prevenção de fraudes.

## 2. Importância da validação temporal

A validação temporal procura reproduzir uma condição mais próxima da utilização real do modelo.

Em aplicações tradicionais de classificação, uma divisão aleatória dos dados pode misturar observações de períodos diferentes entre treinamento e teste.

Em problemas relacionados a seguros, essa estratégia pode produzir uma avaliação excessivamente otimista caso existam padrões temporais, mudanças de comportamento ou informações relacionadas ao futuro.

A utilização de uma divisão temporal permite avaliar a capacidade de generalização para períodos posteriores aos utilizados no treinamento.

## 3. Estratégia temporal utilizada no projeto

A estratégia documentada considera:

| Finalidade | Período |
|---|---|
| Treinamento | 2023 e 2024 |
| Teste | 2025 |

Essa organização procura avaliar o desempenho dos modelos em registros posteriores ao período de treinamento.

O conjunto de teste contém:

- 6.649 registros;
- 476 fraudes;
- 6.173 registros não fraudulentos;
- Prevalência de fraude de 7,16%.

A utilização de 2025 como período de teste permite observar o desempenho em dados temporalmente posteriores aos utilizados no treinamento.

### 3.1 Vantagens da estratégia

A divisão temporal apresenta vantagens importantes:

1. Reduz o risco de mistura entre períodos de treinamento e teste.
2. Aproxima a avaliação do cenário de implantação.
3. Permite investigar mudanças de comportamento ao longo do tempo.
4. Oferece uma referência para futuras comparações.
5. Apoia a construção de mecanismos de monitoramento.

Entretanto, a validação temporal não elimina automaticamente todos os riscos de vazamento de informação.

É necessário verificar a origem e o momento de disponibilidade de cada variável.

## 4. Conceito de data leakage temporal

O vazamento de informação ocorre quando o modelo utiliza dados que não estariam disponíveis no momento em que uma previsão real precisaria ser realizada.

Em uma seguradora, isso pode acontecer quando uma variável é registrada depois da investigação, da regulação ou da conclusão do sinistro.

Exemplos de situações que exigem verificação:

- Informações inseridas após a confirmação de fraude;
- Resultados de investigação disponíveis somente posteriormente;
- Dados financeiros atualizados depois da indenização;
- Variáveis construídas utilizando informações futuras;
- Transformações calculadas com estatísticas de toda a base.

A validação deve verificar se cada variável representa informação efetivamente disponível no momento da decisão.

Esse cuidado é essencial para evitar que o desempenho observado no teste seja superior ao que seria possível obter em produção.

## 5. Conceito de Data Drift

Data Drift é a mudança na distribuição das variáveis de entrada ao longo do tempo.

Pode ocorrer quando o perfil dos registros analisados muda em relação ao período de treinamento.

Exemplos:

- Alteração da distribuição etária dos segurados;
- Mudança no valor médio dos sinistros;
- Crescimento da participação de determinados canais;
- Mudanças geográficas na distribuição das ocorrências;
- Alteração na frequência de determinados tipos de sinistro.

Uma forma de representar o conceito é:

\[
P_{treino}(X)\neq P_{produção}(X)
\]

Essa diferença não significa necessariamente que o modelo perdeu desempenho, mas indica que os dados passaram a apresentar características diferentes das observadas durante o treinamento.

## 6. Conceito de Concept Drift

Concept Drift ocorre quando a relação entre as variáveis de entrada e o resultado que se deseja prever muda ao longo do tempo.

Pode ser representado por:

\[
P_{treino}(Y|X)\neq P_{produção}(Y|X)
\]

Em prevenção de fraudes, isso pode ocorrer quando:

- Fraudadores modificam suas estratégias;
- Surgem novos padrões de fraude;
- Mudam as regras de subscrição;
- São introduzidos novos produtos;
- Mudam os procedimentos de regulação;
- Alterações econômicas afetam o comportamento dos sinistros.

O Concept Drift é particularmente importante porque um modelo pode continuar recebendo dados aparentemente semelhantes, mas perder capacidade de distinguir fraudes de ocorrências legítimas.

## 7. Estratégias para identificar mudanças nos dados

O monitoramento deve acompanhar variáveis numéricas e categóricas.

### 7.1 Variáveis numéricas

Para variáveis numéricas, recomenda-se comparar:

- Média;
- Mediana;
- Desvio-padrão;
- Quartis;
- Valores extremos;
- Distribuição de frequências.

Exemplos de variáveis do projeto:

- Idade;
- Renda mensal;
- Valor segurado;
- Prêmio anual;
- Valor do sinistro;
- Dias até o aviso.

A comparação deve utilizar períodos de referência claramente definidos.

### 7.2 Variáveis categóricas

Para variáveis categóricas, recomenda-se acompanhar:

- Frequência absoluta;
- Frequência relativa;
- Categorias novas;
- Categorias ausentes;
- Mudanças na participação de cada categoria.

Exemplos:

- Estado civil;
- Tipo de cobertura;
- Canal de venda;
- Tipo de sinistro;
- Unidade federativa;
- Boletim de ocorrência.

A identificação de novas categorias pode indicar mudanças operacionais ou problemas de integração dos dados.

## 8. Métodos estatísticos para monitoramento de drift

Existem diferentes métodos para identificar alterações nas distribuições.

### 8.1 Population Stability Index (PSI)

O PSI é utilizado para comparar distribuições entre uma população de referência e uma população atual.

Sua formulação é:

\[
PSI=\sum_{i=1}^{n}(A_i-E_i)
\ln\left(\frac{A_i}{E_i}\right)
\]

Em que:

- \(A_i\): proporção observada na população atual;
- \(E_i\): proporção observada na população de referência;
- \(n\): quantidade de faixas ou categorias.

O PSI pode ser utilizado para acompanhar mudanças na distribuição das variáveis e dos escores de risco.

Limiares como 0,10 e 0,25 são utilizados em algumas práticas como referências indicativas, mas não devem ser tratados como regras universais.

A interpretação depende da variável, do tamanho da amostra e do contexto operacional.

### 8.2 Kolmogorov-Smirnov

O teste de Kolmogorov-Smirnov pode ser utilizado para comparar distribuições empíricas de variáveis numéricas.

A estatística considera a maior diferença absoluta entre as funções de distribuição acumulada.

\[
D=\sup_x|F_1(x)-F_2(x)|
\]

O resultado pode indicar diferenças entre as distribuições de referência e as observadas.

A interpretação deve considerar o tamanho da amostra e a relevância prática da diferença.

### 8.3 Teste Qui-quadrado

O teste Qui-quadrado pode ser utilizado para avaliar diferenças entre distribuições categóricas.

Sua estatística é:

\[
\chi^2=\sum_{i=1}^{n}
\frac{(O_i-E_i)^2}{E_i}
\]

Em que:

- \(O_i\): frequência observada;
- \(E_i\): frequência esperada.

O método exige atenção às frequências esperadas e às condições de aplicação do teste.

### 8.4 Divergência de Jensen-Shannon

A divergência de Jensen-Shannon pode ser utilizada para comparar distribuições probabilísticas.

É uma alternativa simétrica baseada na divergência de Kullback-Leibler e pode ser útil para acompanhar alterações na distribuição de variáveis ou escores.

A escolha do método deve considerar o tipo de variável, o volume de dados e a finalidade do monitoramento.

## 9. Monitoramento do desempenho preditivo

O monitoramento não deve se limitar às características dos dados.

Também é necessário acompanhar as métricas dos modelos quando os resultados reais estiverem disponíveis.

Recomenda-se acompanhar:

- Recall;
- Precisão;
- F1-score;
- ROC-AUC;
- PR-AUC;
- Taxa de falsos positivos;
- Taxa de falsos negativos;
- Quantidade de alertas;
- Taxa de confirmação das investigações.

A análise deve ser realizada por período e, quando possível, por segmento de negócio.

### 9.1 Defasagem na disponibilidade dos rótulos

Em prevenção de fraudes, a confirmação de uma ocorrência pode acontecer semanas ou meses após a abertura do sinistro.

Isso significa que as métricas reais de desempenho podem não estar disponíveis imediatamente.

O monitoramento precisa distinguir:

1. Indicadores calculados com previsões recentes;
2. Indicadores calculados com resultados de investigação já concluídos;
3. Indicadores provisórios ainda sujeitos à confirmação.

Não se deve interpretar a ausência de fraude confirmada como prova de que um alerta era falso positivo quando a investigação ainda está pendente.

## 10. Monitoramento dos limiares de decisão

Os limiares influenciam diretamente o volume de alertas e a capacidade de detecção.

No projeto, os valores utilizados são:

| Modelo | Limiar |
|---|---:|
| Regressão Logística | 0,50 |
| Random Forest | 0,25 |

Esses valores devem ser acompanhados ao longo do tempo.

Uma mudança na distribuição dos escores pode alterar a quantidade de registros classificados como suspeitos.

Recomenda-se monitorar:

- Quantidade de alertas por período;
- Percentual de alertas em relação ao total;
- Fraudes identificadas;
- Taxa de confirmação;
- Capacidade da equipe de investigação;
- Mudanças na distribuição dos escores.

A alteração de um limiar deve ser documentada e validada antes de sua adoção operacional.

## 11. Estratégia de retreinamento

O retreinamento consiste em atualizar o modelo utilizando dados mais recentes.

Não deve ser realizado automaticamente apenas porque uma variável apresentou alteração estatística.

A decisão precisa considerar:

- Evidências de degradação do desempenho;
- Mudanças relevantes nos dados;
- Disponibilidade de novos rótulos confiáveis;
- Qualidade dos dados recentes;
- Resultado da avaliação temporal;
- Comparação entre a versão atual e a nova versão.

Uma estratégia recomendada é manter uma janela histórica de treinamento e avaliar diferentes períodos de atualização.

O novo modelo somente deve substituir o modelo vigente após passar pelos critérios de validação definidos pela organização.

## 12. Monitoramento e governança com MLflow

O MLflow pode apoiar o acompanhamento do ciclo de vida dos modelos.

Entre as informações que podem ser registradas estão:

- Identificador da execução;
- Algoritmo utilizado;
- Parâmetros;
- Métricas;
- Versão do modelo;
- Data de treinamento;
- Período dos dados;
- Artefatos;
- Resultados de validação.

O registro estruturado permite comparar diferentes versões e reconstruir as condições de treinamento.

No contexto da evolução da arquitetura, recomenda-se utilizar o MLflow como componente de rastreabilidade e gestão do ciclo de vida dos modelos.

A integração com uma plataforma de dados, como Databricks, poderá ampliar a automação dos processos de treinamento, avaliação e monitoramento.

Essa integração constitui uma direção de evolução arquitetural e não deve ser confundida com funcionalidades já comprovadamente implantadas.

## 13. Arquitetura recomendada de monitoramento

A arquitetura futura pode ser organizada em cinco etapas:

1. Ingestão periódica de novos sinistros;
2. Validação e preparação dos dados;
3. Geração de previsões e escores de risco;
4. Monitoramento de distribuição e desempenho;
5. Avaliação da necessidade de intervenção ou retreinamento.

O Streamlit pode continuar sendo utilizado como interface gerencial para apresentação dos indicadores.

A camada de processamento e armazenamento poderá evoluir para uma arquitetura integrada ao Databricks, mantendo o MLflow como componente de rastreabilidade dos experimentos e modelos.

## 14. Indicadores recomendados para um painel de monitoramento

| Indicador | Objetivo |
|---|---|
| PSI por variável | Identificar alterações nas distribuições |
| Distribuição dos escores | Acompanhar mudanças no comportamento das previsões |
| Volume de alertas | Monitorar a demanda operacional |
| Recall por período | Acompanhar a capacidade de detecção |
| Precisão por período | Acompanhar a qualidade dos alertas |
| PR-AUC por período | Monitorar a discriminação da classe positiva |
| Taxa de confirmação | Avaliar os resultados das investigações |
| Tempo de investigação | Acompanhar a eficiência operacional |
| Versão do modelo | Garantir rastreabilidade |
| Data do último treinamento | Acompanhar a atualização dos modelos |

Esses indicadores devem possuir periodicidade, responsáveis e critérios de intervenção definidos.

## 15. Limitações atuais

O repositório atual contém modelos serializados e uma aplicação de inferência, mas não documenta um sistema completo de monitoramento contínuo em produção.

Também não estão demonstrados:

- Cálculo periódico de PSI;
- Testes automatizados de drift;
- Monitoramento contínuo de métricas;
- Alertas automáticos de degradação;
- Política implementada de retreinamento;
- Histórico de desempenho em produção.

Esses itens devem ser tratados como requisitos de evolução, não como funcionalidades já implementadas.

## 16. Conclusão

A estabilidade temporal é um requisito fundamental para a utilização responsável de modelos preditivos na prevenção de fraudes.

A divisão temporal entre treinamento e teste oferece uma primeira avaliação da capacidade de generalização, mas não substitui o acompanhamento contínuo após a implantação.

O monitoramento de Data Drift, Concept Drift, métricas de desempenho e indicadores operacionais permite identificar mudanças que podem comprometer a qualidade das previsões.

A evolução da solução deverá incorporar mecanismos de monitoramento, rastreabilidade, validação periódica e governança do ciclo de vida dos modelos.

Dessa forma, a aplicação poderá evoluir para uma plataforma analítica mais robusta, capaz de acompanhar mudanças no comportamento dos dados e preservar a confiabilidade das decisões apoiadas por Machine Learning.