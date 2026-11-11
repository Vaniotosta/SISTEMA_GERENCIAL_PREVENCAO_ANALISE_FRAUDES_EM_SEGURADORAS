# Análise Econômico-Financeira da Prevenção de Fraudes

## 1. Introdução

A aplicação de modelos preditivos à prevenção de fraudes em seguradoras deve ser avaliada não apenas pela capacidade estatística de classificação, mas também pelo potencial de contribuição para os resultados financeiros e operacionais da organização.

Uma solução de detecção de fraudes pode contribuir para:

- Identificar ocorrências suspeitas antes da conclusão do processo de indenização;
- Priorizar sinistros para investigação;
- Reduzir a exposição a pagamentos indevidos;
- Melhorar a alocação dos recursos das equipes antifraude;
- Apoiar decisões fundamentadas em dados;
- Aumentar a eficiência dos processos de regulação de sinistros.

Entretanto, a identificação estatística de uma ocorrência suspeita não representa, por si só, uma economia financeira efetiva.

Para demonstrar retorno econômico, é necessário relacionar os resultados preditivos a decisões operacionais, investigações concluídas, fraudes efetivamente confirmadas e valores financeiros que deixaram de ser pagos indevidamente.

Este capítulo apresenta a estrutura de avaliação econômico-financeira, os indicadores reportados pela aplicação e as condições necessárias para mensurar o retorno efetivo da solução.

## 2. Relação entre desempenho preditivo e resultado financeiro

O desempenho de um modelo antifraude pode produzir consequências financeiras diferentes.

A matriz de confusão permite identificar quatro situações:

| Resultado | Consequência operacional | Possível consequência financeira |
|---|---|---|
| Verdadeiro positivo | Fraude identificada | Possibilidade de evitar pagamento indevido |
| Falso positivo | Sinistro legítimo sinalizado | Custo adicional de investigação |
| Verdadeiro negativo | Sinistro legítimo corretamente classificado | Processamento sem alerta adicional |
| Falso negativo | Fraude não identificada | Possibilidade de pagamento indevido não evitado |

A principal distinção é que o modelo produz classificações e escores de risco, enquanto o resultado financeiro depende das decisões posteriores.

Um verdadeiro positivo somente se converte em benefício econômico quando a investigação confirma a fraude e uma medida operacional impede ou recupera um pagamento indevido.

Da mesma forma, um falso positivo pode gerar custos de investigação, atrasos e impactos na experiência do segurado.

Portanto, a avaliação econômica precisa considerar tanto os benefícios potenciais quanto os custos decorrentes da operação do sistema.

## 3. Indicadores de exposição financeira apresentados pela aplicação

A aplicação apresenta os seguintes valores associados aos modelos:

| Modelo | Exposição apresentada |
|---|---:|
| Regressão Logística | R$ 2.935.123,43 |
| Random Forest | R$ 3.951.496,83 |
| Diferença | R$ 1.016.373,40 |

A diferença entre os valores é calculada por:

\[
\Delta E=E_{RF}-E_{LR}
\]

\[
\Delta E=3.951.496,83-2.935.123,43
\]

\[
\Delta E=R\$\,1.016.373,40
\]

O valor representa aproximadamente R$ 1,02 milhão de diferença entre as exposições financeiras exibidas para os dois modelos.

### 3.1 Ressalva metodológica sobre os valores

Os valores acima correspondem aos indicadores financeiros apresentados na interface da aplicação.

A implementação consultada apresenta valores fixos de R$ 2,94 milhões e R$ 3,95 milhões na construção do gráfico de exposição.

A origem analítica desses valores, sua composição e sua vinculação aos registros individuais ainda precisam ser verificadas no processo original de cálculo.

Por essa razão, não devem ser interpretados como:

- Perdas financeiras efetivamente realizadas;
- Pagamentos indevidos comprovados;
- Valores recuperados pela seguradora;
- Economia efetivamente obtida;
- Retorno financeiro comprovado dos modelos.

A diferença de R$ 1.016.373,40 também não deve ser interpretada como economia produzida pelo Random Forest ou como evidência de superioridade financeira desse algoritmo.

Para validar economicamente esses indicadores, será necessário reconstruir o cálculo a partir dos registros de sinistros, das classificações dos modelos e dos valores financeiros correspondentes.

## 4. Custos associados aos erros de classificação

A análise econômica deve considerar os custos dos falsos positivos e dos falsos negativos.

### 4.1 Custo dos falsos positivos

Um falso positivo ocorre quando um sinistro não fraudulento é sinalizado pelo modelo como suspeito.

As principais consequências potenciais incluem:

- Necessidade de investigação adicional;
- Aumento do tempo de análise;
- Consumo de recursos da equipe antifraude;
- Possíveis atrasos na regulação;
- Impacto negativo na experiência do segurado;
- Aumento do custo operacional.

Uma aproximação inicial do custo pode ser calculada por:

\[
C_{FP}=N_{FP}\times C_I
\]

Em que:

- \(N_{FP}\): quantidade de falsos positivos;
- \(C_I\): custo médio de investigação de um alerta.

O custo médio deve ser obtido a partir dos dados operacionais da seguradora.

### 4.2 Custo dos falsos negativos

Um falso negativo ocorre quando uma fraude existente não é identificada pelo modelo.

As consequências potenciais incluem:

- Pagamento de indenização indevida;
- Perda financeira não evitada;
- Despesas administrativas relacionadas ao sinistro;
- Custos adicionais de recuperação;
- Impactos sobre a rentabilidade da carteira.

Uma estimativa simplificada seria:

\[
C_{FN}=\sum_{i=1}^{N_{FN}}V_i
\]

Em que:

- \(N_{FN}\): quantidade de falsos negativos;
- \(V_i\): valor financeiro associado ao sinistro fraudulento não identificado.

Esse cálculo depende da disponibilidade dos valores individuais dos sinistros e da confirmação de que os registros classificados como fraude representam efetivamente fraudes segundo a referência utilizada.

O valor do sinistro não deve ser automaticamente tratado como perda evitável. É necessário considerar o valor que seria efetivamente pago, eventuais franquias, recuperações, cobertura contratual e outras condições de indenização.

## 5. Comparação operacional com impacto econômico potencial

Com base nas matrizes de confusão do conjunto de teste:

| Indicador | Regressão Logística | Random Forest |
|---|---:|---:|
| Verdadeiros positivos | 315 | 277 |
| Falsos positivos | 1.884 | 1.293 |
| Falsos negativos | 161 | 199 |
| Total de alertas | 2.199 | 1.570 |

A Regressão Logística identificou 38 fraudes adicionais em comparação ao Random Forest.

Por outro lado, gerou 591 falsos positivos adicionais.

O volume total de alertas foi 629 registros maior.

Essas diferenças permitem construir uma análise de capacidade operacional.

A Regressão Logística pode ser mais interessante quando a prioridade é ampliar a identificação de fraudes, desde que a seguradora disponha de capacidade para investigar os alertas adicionais.

O Random Forest pode ser interessante quando existe restrição operacional e a prioridade é reduzir a quantidade de investigações, aceitando uma quantidade maior de fraudes não identificadas.

A decisão financeira depende dos custos relativos de cada situação.

## 6. Modelo de custo esperado

Uma estrutura de avaliação pode combinar os custos dos erros de classificação.

Uma formulação simplificada é:

\[
C_{Total}=C_{FP}+C_{FN}
\]

Expandindo:

\[
C_{Total}=(N_{FP}\times C_I)+
\sum_{i=1}^{N_{FN}}V_i
\]

Em que:

- \(N_{FP}\): quantidade de falsos positivos;
- \(C_I\): custo médio de investigação;
- \(N_{FN}\): quantidade de falsos negativos;
- \(V_i\): valor financeiro associado a cada falso negativo.

Essa formulação representa uma estrutura inicial de custo esperado.

Em uma aplicação real, o modelo deve ser ampliado para contemplar:

- Taxa de confirmação de fraudes após investigação;
- Probabilidade de impedir o pagamento;
- Valor efetivamente indenizável;
- Percentual de recuperação financeira;
- Custo de tecnologia;
- Custo de manutenção dos modelos;
- Custo de integração e operação;
- Custos jurídicos e administrativos;
- Impactos sobre o tempo de regulação.

## 7. Benefício financeiro efetivamente comprovado

O benefício financeiro não deve ser calculado simplesmente pela soma dos valores de sinistros classificados como suspeitos.

É necessário identificar quais casos foram investigados, confirmados e efetivamente impediram pagamentos indevidos.

Uma formulação conceitual para o benefício bruto é:

\[
B_{Bruto}=\sum_{i=1}^{n}P_i
\]

Em que \(P_i\) representa o pagamento indevido que foi efetivamente evitado em cada fraude confirmada.

O benefício líquido pode ser estimado por:

\[
B_{Liquido}=B_{Bruto}-C_{Operacional}
\]

O custo operacional deve incluir as despesas incrementais necessárias para manter a solução em funcionamento.

Para calcular o retorno sobre o investimento:

\[
ROI=\frac{B_{Liquido}}{C_{Investimento}}\times100
\]

A análise deve utilizar um período definido, uma linha de base comparável e critérios consistentes de atribuição do benefício à solução.

## 8. Simulação econômica e análise de sensibilidade

Antes de implantar a solução em escala, recomenda-se construir cenários econômicos.

Os cenários podem variar conforme:

- Custo médio de investigação;
- Percentual de alertas confirmados;
- Valor médio dos pagamentos indevidos;
- Capacidade diária de investigação;
- Percentual de fraudes efetivamente evitadas;
- Custo de operação da infraestrutura.

A análise de sensibilidade permite verificar como a rentabilidade potencial muda diante de diferentes premissas.

Uma simulação deve deixar explícito que seus resultados são hipotéticos até que os parâmetros sejam substituídos por dados operacionais validados.

Não se deve utilizar valores simulados como evidência de economia efetivamente alcançada.

## 9. Indicadores gerenciais recomendados

Para transformar a solução em instrumento de gestão, recomenda-se acompanhar os seguintes indicadores:

| Indicador | Finalidade |
|---|---|
| Valor de sinistros suspeitos | Mensurar o valor financeiro associado aos alertas |
| Valor de fraudes confirmadas | Identificar a exposição validada pela investigação |
| Pagamentos efetivamente evitados | Mensurar benefício financeiro comprovado |
| Taxa de confirmação dos alertas | Avaliar a efetividade das investigações |
| Custo por investigação | Medir eficiência operacional |
| Custo por fraude identificada | Avaliar o esforço necessário para detectar fraudes |
| Taxa de falsos positivos | Monitorar alertas improdutivos |
| Taxa de falsos negativos | Acompanhar fraudes não identificadas |
| Tempo médio de investigação | Avaliar eficiência do processo |
| ROI da solução | Avaliar retorno financeiro |

Esses indicadores devem ser acompanhados ao longo do tempo e