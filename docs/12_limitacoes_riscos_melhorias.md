# 12. Limitações, Riscos e Plano de Melhorias

## 1. Introdução

Este documento apresenta uma avaliação crítica das limitações técnicas, estatísticas, operacionais e gerenciais do Sistema de Prevenção e Análise de Fraudes em Seguradoras.

O objetivo é identificar os riscos associados à utilização dos modelos preditivos, estabelecer os cuidados necessários para interpretar os resultados e propor uma trajetória estruturada de evolução do projeto.

Uma solução de inteligência artificial aplicada à prevenção de fraudes não deve ser avaliada exclusivamente pela capacidade de classificação. Também é necessário considerar a qualidade dos dados, a estabilidade dos modelos, os custos operacionais, a explicabilidade das previsões e a participação humana no processo decisório.

As limitações aqui apresentadas devem ser entendidas como parte da avaliação científica e tecnológica da solução, e não como uma invalidação dos resultados obtidos.

## 2. Limitações relacionadas aos dados

### 2.1. Representatividade da base

A base utilizada no projeto possui 20.000 registros, dos quais 1.352 correspondem a fraudes identificadas, representando 6,76% das observações.

Embora esse volume permita desenvolver e avaliar modelos de classificação, não é possível afirmar que a distribuição observada represente integralmente o comportamento de todas as carteiras, produtos, regiões ou períodos de uma seguradora real.

A generalização dos resultados depende da representatividade da amostra e da semelhança entre os dados utilizados no desenvolvimento e aqueles encontrados em ambientes operacionais.

### 2.2. Desbalanceamento das classes

A variável-alvo apresenta distribuição desigual:

- Registros sem fraude: 18.648 (93,24%).
- Registros com fraude: 1.352 (6,76%).

Esse desbalanceamento exige atenção especial, pois um classificador pode apresentar elevada acurácia simplesmente favorecendo a classe majoritária.

Por esse motivo, o projeto utiliza métricas complementares, como precisão, recall, F1-score, ROC-AUC e PR-AUC.

### 2.3. Disponibilidade e qualidade das variáveis

A solução utiliza 22 variáveis de entrada relacionadas ao perfil do cliente, à apólice e às características do sinistro.

Entretanto, a presença dessas variáveis não garante, isoladamente, qualidade, consistência ou disponibilidade em um ambiente real.

É necessário avaliar:

- Percentual de valores ausentes por variável.
- Registros duplicados.
- Inconsistências cadastrais.
- Valores extremos.
- Categorias desconhecidas.
- Alterações nos padrões de preenchimento.
- Disponibilidade das informações no momento da análise.

A interface permite o preenchimento opcional de determinados campos. Isso não constitui, por si só, evidência de que tenha sido implementado um processo completo de tratamento de valores ausentes no treinamento dos modelos.

A documentação integral do pipeline original de preparação dos dados deve ser preservada para permitir reprodução e auditoria.

## 3. Limitações estatísticas dos modelos

### 3.1. Desempenho preditivo

Os modelos foram avaliados em uma base temporal de teste referente a 2025, com 6.649 registros, incluindo 476 fraudes.

Os resultados observados foram:

| Métrica | Regressão Logística | Random Forest |
|---|---:|---:|
| Acurácia | 69,24% | 77,56% |
| Precisão | 14,32% | 17,64% |
| Recall | 66,18% | 58,19% |
| F1-score | 23,55% | 27,08% |
| ROC-AUC | 0,7631 | 0,7462 |
| PR-AUC | 0,2244 | 0,1954 |

Os resultados demonstram que os modelos conseguem identificar parte dos registros fraudulentos, mas ainda apresentam limitações relevantes.

A precisão relativamente baixa indica que uma parcela expressiva dos registros classificados como suspeitos não corresponde a fraudes identificadas na base de avaliação.

Consequentemente, a implantação operacional exigiria um processo de investigação e validação humana dos alertas.

### 3.2. Diferença entre acurácia e capacidade de identificação de fraudes

A acurácia não deve ser utilizada isoladamente como critério de seleção.

Na base completa, 93,24% dos registros pertencem à classe sem fraude. Um classificador que sempre previsse ausência de fraude alcançaria essa acurácia, mas não identificaria nenhum caso fraudulento.

Na base temporal de teste, a proporção de registros sem fraude é de aproximadamente 92,84%.

Portanto, a avaliação deve considerar a capacidade de identificar fraudes, a quantidade de falsos alertas e o custo associado aos erros.

### 3.3. Diferença entre os limiares de classificação

A aplicação utiliza os seguintes limiares:

- Regressão Logística: 0,50.
- Random Forest: 0,25.

Esses valores representam os pontos de corte utilizados para transformar as probabilidades estimadas em classificações.

Como os limiares são diferentes, as matrizes de confusão não representam uma comparação realizada sob o mesmo critério operacional.

A comparação deve considerar tanto as métricas calculadas nos limiares atuais quanto análises adicionais com limiares equivalentes e curvas de desempenho.

A definição de um limiar adequado deve considerar a capacidade operacional da equipe de investigação e os custos dos falsos positivos e falsos negativos.

### 3.4. Necessidade de calibração das probabilidades

Uma probabilidade estimada de 0,80 não significa necessariamente que 80% dos registros com essa previsão serão efetivamente fraudulentos.

Para utilizar as probabilidades como estimativas de risco, recomenda-se avaliar a calibração dos modelos.

Entre as técnicas possíveis estão:

- Curvas de calibração.
- Brier Score.
- Calibração isotônica.
- Regressão logística de calibração.

A calibração deve ser realizada sem utilizar informações da base de teste para ajustar o modelo.

## 4. Riscos metodológicos

### 4.1. Vazamento de dados

O vazamento de dados ocorre quando informações que não estariam disponíveis no momento da previsão são utilizadas durante o treinamento ou a avaliação.

Em sistemas de prevenção de fraudes, esse risco é particularmente importante.

Por exemplo, informações decorrentes de uma investigação concluída não devem ser utilizadas como variáveis de entrada se a previsão for realizada antes da investigação.

Recomenda-se verificar:

- A disponibilidade temporal de cada variável.
- A separação entre treinamento e teste.
- O ajuste dos transformadores exclusivamente com dados de treinamento.
- A inexistência de informações derivadas diretamente do resultado da investigação.
- A reprodução do processo completo de treinamento.

A divisão temporal entre 2023–2024 para treinamento e 2025 para teste é uma estratégia adequada para investigar a generalização temporal, mas não elimina automaticamente todos os riscos de vazamento.

### 4.2. Reprodutibilidade

A reprodução integral dos resultados depende da preservação dos seguintes elementos:

- Base de dados utilizada.
- Dicionário de variáveis.
- Código de preparação dos dados.
- Código de treinamento.
- Parâmetros dos modelos.
- Versões das bibliotecas.
- Critérios de divisão dos dados.
- Métricas e limiares utilizados.
- Artefatos dos modelos.

O repositório atual contém artefatos de modelos e uma aplicação de inferência, mas a presença desses elementos não comprova que todo o processo original de treinamento esteja documentado e reproduzível.

A recuperação e organização do pipeline completo constituem uma melhoria prioritária.

## 5. Riscos operacionais e gerenciais

### 5.1. Falsos positivos

Um falso positivo ocorre quando um registro legítimo é classificado como suspeito.

Esse erro pode gerar:

- Investigações desnecessárias.
- Aumento do tempo de análise.
- Sobrecarga das equipes.
- Atrasos no atendimento ao segurado.
- Custos operacionais adicionais.
- Risco de decisões injustas quando não existe revisão humana.

A precisão dos modelos demonstra que esse risco precisa ser considerado antes de qualquer implantação operacional.

### 5.2. Falsos negativos

Um falso negativo ocorre quando um registro fraudulento é classificado como não fraudulento.

Esse tipo de erro pode permitir que casos suspeitos não sejam encaminhados para investigação.

A redução dos falsos negativos é relevante para a prevenção de perdas, mas não deve ser buscada sem considerar o aumento potencial de falsos positivos.

### 5.3. Capacidade de investigação

Um modelo pode identificar muitos registros suspeitos, mas a organização precisa possuir capacidade operacional para analisar os alertas.

A quantidade de alertas deve ser compatível com:

- Número de analistas disponíveis.
- Tempo médio de investigação.
- Complexidade dos casos.
- Prioridade financeira.
- Critérios de encaminhamento.
- Procedimentos de auditoria.

O desempenho de um sistema antifraude depende tanto da qualidade preditiva quanto da capacidade de transformar alertas em investigações eficientes.

## 6. Limitações da análise econômico-financeira

A aplicação apresenta valores estimados de exposição financeira associados aos modelos:

- Regressão Logística: R$ 2.935.123,43.
- Random Forest: R$ 3.951.496,83.
- Diferença apresentada: R$ 1.016.373,40.

Esses valores são informações exibidas pela aplicação. A metodologia detalhada de cálculo e sua correspondência com perdas efetivamente verificadas ainda precisam ser validadas.

Portanto, não devem ser interpretados automaticamente como:

- Prejuízo financeiro efetivamente ocorrido.
- Economia realizada pela seguradora.
- Valor recuperado.
- Retorno sobre investimento.
- Prova de superioridade econômica de um modelo.

Para consolidar essa análise, recomenda-se documentar a origem dos valores, a regra de cálculo, a relação entre previsões e valores dos sinistros e os custos de investigação.

Uma avaliação econômica robusta deverá considerar:

1. Custo médio de investigação.
2. Valor financeiro associado aos casos confirmados.
3. Taxa de conversão de alertas em fraudes confirmadas.
4. Custo dos falsos positivos.
5. Perdas associadas aos falsos negativos.
6. Custos de implantação e manutenção.
7. Benefícios financeiros efetivamente mensurados.

Somente após essa validação será possível estimar retorno financeiro com maior confiabilidade.

## 7. Riscos de implantação em produção

A aplicação atual demonstra uma solução funcional de análise e inferência, mas sua existência não significa que todos os requisitos de um ambiente corporativo de produção estejam implementados.

Antes da implantação em uma seguradora, devem ser avaliados:

- Integração com sistemas de apólices e sinistros.
- Autenticação e autorização de usuários.
- Controle de acesso por perfil.
- Proteção de informações pessoais.
- Registro de operações.
- Monitoramento de disponibilidade.
- Monitoramento de desempenho preditivo.
- Versionamento de modelos.
- Estratégia de recuperação em caso de falha.
- Processo de atualização e validação dos modelos.

O uso de Databricks, Delta Lake e arquitetura Medallion pode ser considerado em uma evolução futura da infraestrutura de dados. Essas tecnologias não devem ser apresentadas como funcionalidades já implantadas na solução atual.

## 8. Riscos de viés e uso inadequado da inteligência artificial

Modelos preditivos podem reproduzir padrões históricos inadequados presentes nos dados.

No contexto de seguros, isso pode gerar diferenças injustificadas na identificação de registros suspeitos entre grupos de clientes ou regiões.

Recomenda-se:

- Avaliar o desempenho por grupos relevantes.
- Verificar possíveis diferenças nas taxas de falsos positivos e falsos negativos.
- Investigar variáveis que possam funcionar como proxies de características sensíveis.
- Documentar os critérios de utilização das previsões.
- Manter revisão humana.
- Evitar decisões exclusivamente automatizadas sem avaliação jurídica e regulatória apropriada.

O modelo deve funcionar como ferramenta de apoio à análise, e não como prova definitiva de fraude.

## 9. Plano de melhorias priorizado

As melhorias propostas foram organizadas considerando impacto esperado e dependências técnicas.

| Prioridade | Melhoria | Impacto esperado |
|---|---|---|
| Alta | Recuperar e documentar o pipeline completo de treinamento | Reprodutibilidade |
| Alta | Validar a origem e o cálculo da exposição financeira | Confiabilidade econômica |
| Alta | Revisar vazamento de dados e disponibilidade temporal das variáveis | Validade estatística |
| Alta | Avaliar diferentes limiares de classificação | Eficiência operacional |
| Alta | Implementar avaliação de calibração | Confiabilidade das probabilidades |
| Média | Avaliar desempenho por segmentos | Identificação de vieses |
| Média | Implementar monitoramento de dados e desempenho | Estabilidade |
| Média | Registrar versões e experimentos de forma padronizada | Governança |
| Média | Avaliar técnicas de tratamento do desbalanceamento | Desempenho na classe minoritária |
| Média | Aprimorar explicabilidade das previsões | Apoio à investigação |
| Futura | Integrar fontes corporativas de dados | Escalabilidade |
| Futura | Evoluir a infraestrutura para ambiente corporativo | Operação em produção |

## 10. Proposta de experimentos futuros

Para orientar a evolução científica do projeto, recomenda-se executar experimentos controlados.

### Experimento 1 — Otimização do limiar

Avaliar diferentes pontos de corte para cada modelo.

Objetivo: identificar combinações entre precisão, recall e volume de alertas que sejam compatíveis com a capacidade de investigação.

Critérios de avaliação:

- Recall.
- Precisão.
- F1-score.
- Falsos positivos.
- Falsos negativos.
- Quantidade de alertas.

### Experimento 2 — Tratamento do desbalanceamento

Investigar estratégias como:

- Pesos de classe.
- Subamostragem da classe majoritária.
- Sobreamostragem da classe minoritária.
- SMOTE, quando metodologicamente adequado.

As técnicas devem ser aplicadas exclusivamente nos dados de treinamento de cada partição, evitando contaminação da validação e do teste.

### Experimento 3 — Calibração

Avaliar se as probabilidades estimadas correspondem às frequências observadas de fraude.

Critérios:

- Brier Score.
- Curvas de calibração.
- Comparação antes e depois da calibração.

### Experimento 4 — Explicabilidade

Investigar a contribuição das variáveis para as previsões.

Técnicas possíveis:

- Coeficientes da Regressão Logística.
- Importância de variáveis.
- Permutation Importance.
- SHAP.

As explicações devem ser interpretadas considerando as limitações de cada técnica e a possível correlação entre variáveis.

### Experimento 5 — Validação temporal ampliada

Avaliar o comportamento dos modelos em períodos adicionais, quando houver dados disponíveis.

Objetivo: investigar a estabilidade dos resultados e a capacidade de generalização diante de mudanças no comportamento das fraudes.

## 11. Critérios de aceitação para evolução

A evolução do sistema deve ser conduzida por critérios mensuráveis.

Antes de considerar uma nova versão adequada para uso operacional, recomenda-se exigir:

1. Pipeline de treinamento documentado e reproduzível.
2. Ausência de vazamento de dados identificado.
3. Avaliação temporal independente.
4. Métricas de classificação documentadas.
5. Limiares justificados por critérios operacionais.
6. Probabilidades avaliadas quanto à calibração, quando utilizadas como estimativas de risco.
7. Análise de falsos positivos e falsos negativos.
8. Metodologia financeira validada.
9. Controles de acesso e segurança avaliados.
10. Processo de revisão humana e auditoria definido.

Os critérios e valores mínimos de desempenho deverão ser definidos com a seguradora conforme seu apetite de risco, capacidade de investigação e objetivos de negócio.

## 12. Conclusão

O Sistema de Prevenção e Análise de Fraudes em Seguradoras apresenta uma aplicação prática de aprendizado de máquina para apoiar a identificação de registros potencialmente fraudulentos.

Os resultados demonstram que a Regressão Logística e o Random Forest oferecem perspectivas diferentes de desempenho. O Random Forest apresenta maior acurácia, precisão e F1-score nos limiares utilizados, enquanto a Regressão Logística apresenta maior recall, ROC-AUC e PR-AUC.

Entretanto, a precisão limitada, a necessidade de validação econômica, a documentação incompleta do pipeline original e os requisitos de governança demonstram que ainda existem etapas importantes antes de uma utilização corporativa em produção.

A evolução da solução deverá priorizar reprodutibilidade, validação estatística, explicabilidade, eficiência operacional, segurança e mensuração financeira.

A principal contribuição do projeto está na construção de uma estrutura analítica que transforma dados de sinistros em informações úteis para apoiar a investigação e a tomada de decisão.

A inteligência artificial deve atuar como instrumento de apoio especializado, preservando a responsabilidade humana, a transparência e a qualidade dos processos decisórios.