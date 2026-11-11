# Governança de Dados, LGPD, Segurança e Inteligência Artificial Responsável

## 1. Introdução

A utilização de Machine Learning na prevenção de fraudes em seguradoras exige uma estrutura de governança capaz de assegurar a qualidade, a segurança, a rastreabilidade e o uso responsável das informações.

Os dados utilizados em operações de seguros podem envolver informações cadastrais, financeiras, contratuais e relacionadas a sinistros. Por isso, seu tratamento deve observar requisitos legais, regulatórios, éticos e organizacionais.

Além da qualidade preditiva, uma solução de prevenção de fraudes precisa considerar:

- Proteção de dados pessoais;
- Controle de acesso;
- Segurança da informação;
- Transparência metodológica;
- Explicabilidade dos resultados;
- Supervisão humana;
- Prevenção de vieses;
- Rastreabilidade das decisões;
- Responsabilização dos processos.

Este capítulo apresenta os princípios que devem orientar a governança da solução.

## 2. Governança de dados

Governança de dados corresponde ao conjunto de políticas, responsabilidades, processos e controles utilizados para garantir que os dados sejam tratados de maneira adequada durante seu ciclo de vida.

Em uma seguradora, a governança deve abranger desde a coleta das informações até seu armazenamento, processamento, utilização analítica, compartilhamento e descarte.

### 2.1 Objetivos da governança

Os principais objetivos são:

1. Assegurar qualidade e consistência dos dados.
2. Definir responsabilidades sobre as informações.
3. Garantir rastreabilidade das transformações.
4. Controlar acessos e permissões.
5. Reduzir riscos de utilização inadequada.
6. Preservar a integridade dos registros.
7. Apoiar auditorias e processos de conformidade.
8. Estabelecer critérios de retenção e descarte.

### 2.2 Dimensões da qualidade dos dados

A qualidade deve ser avaliada considerando diferentes dimensões.

| Dimensão | Significado | Exemplo no projeto |
|---|---|---|
| Completude | Presença das informações necessárias | Campos cadastrais preenchidos |
| Consistência | Compatibilidade entre informações | Valores e categorias coerentes |
| Validade | Conformidade com regras definidas | Idade dentro de intervalos admissíveis |
| Unicidade | Ausência de duplicações indevidas | Identificação única dos sinistros |
| Atualidade | Disponibilidade no momento adequado | Dados atualizados antes da previsão |
| Precisão | Correspondência com a realidade | Valores financeiros corretos |

A qualidade dos dados influencia diretamente a confiabilidade dos modelos.

Um algoritmo sofisticado não consegue compensar integralmente informações incorretas, inconsistentes ou inadequadas.

## 3. Lei Geral de Proteção de Dados Pessoais (LGPD)

A Lei nº 13.709/2018, conhecida como Lei Geral de Proteção de Dados Pessoais, estabelece regras para o tratamento de dados pessoais no Brasil.

O projeto deve considerar a LGPD em todas as etapas que envolvam informações de pessoas naturais identificadas ou identificáveis.

Entre os princípios relevantes estão:

- Finalidade;
- Adequação;
- Necessidade;
- Livre acesso;
- Qualidade dos dados;
- Transparência;
- Segurança;
- Prevenção;
- Não discriminação;
- Responsabilização e prestação de contas.

### 3.1 Finalidade

Os dados devem ser tratados para finalidades legítimas, específicas e informadas.

No contexto da solução, a finalidade analítica é apoiar a identificação de padrões associados a possíveis fraudes em sinistros.

A utilização de informações para outras finalidades exige avaliação de compatibilidade e fundamento jurídico adequado.

### 3.2 Adequação

O tratamento deve ser compatível com a finalidade informada.

As variáveis utilizadas precisam possuir relação justificável com o problema analítico.

A inclusão de uma variável deve considerar sua relevância, necessidade e possíveis consequências para os titulares.

### 3.3 Necessidade

O princípio da necessidade orienta a utilização do mínimo de dados pessoais necessário para alcançar a finalidade pretendida.

Isso significa que não se deve incluir informações pessoais apenas porque estão disponíveis.

A seleção de variáveis precisa ser justificada tecnicamente e avaliada sob a perspectiva de proteção de dados.

### 3.4 Qualidade dos dados

As informações devem ser exatas, claras, relevantes e atualizadas conforme a necessidade e a finalidade do tratamento.

Dados desatualizados ou incorretos podem produzir classificações inadequadas.

### 3.5 Segurança e prevenção

Devem ser adotadas medidas técnicas e administrativas para proteger os dados contra acessos não autorizados, perda, alteração, divulgação ou tratamento inadequado.

A segurança precisa ser considerada desde a concepção da arquitetura.

## 4. Bases legais para o tratamento

A LGPD estabelece hipóteses legais que autorizam o tratamento de dados pessoais.

A definição da base legal aplicável deve ser realizada pelo controlador, com apoio das áreas jurídica, de privacidade e de governança.

No contexto de seguros, a análise pode considerar, conforme as circunstâncias concretas:

- Cumprimento de obrigação legal ou regulatória;
- Execução de contrato ou procedimentos preliminares relacionados a contrato;
- Exercício regular de direitos;
- Legítimo interesse, quando aplicável e após avaliação dos requisitos legais;
- Outras hipóteses legais pertinentes.

Não se deve presumir que uma única base legal autorize indistintamente todos os tratamentos realizados pela seguradora.

A finalidade, a natureza dos dados, a operação executada e a relação com o titular precisam ser avaliadas individualmente.

## 5. Dados pessoais e dados pessoais sensíveis

A classificação dos dados é fundamental para definir os controles de proteção.

Dados pessoais são informações relacionadas a pessoa natural identificada ou identificável.

Dados pessoais sensíveis incluem categorias específicas previstas na LGPD, como informações sobre saúde, origem racial ou étnica, convicção religiosa e outros elementos definidos legalmente.

A presença de informações financeiras ou contratuais não significa, por si só, que elas sejam classificadas como dados pessoais sensíveis pela definição legal.

Entretanto, esses dados podem apresentar elevado risco de exposição e devem receber proteção adequada.

### 5.1 Aplicação ao projeto

As variáveis documentadas incluem informações como:

- Idade;
- Renda mensal;
- Score de crédito;
- Estado civil;
- Unidade federativa;
- Valor segurado;
- Prêmio anual;
- Tipo de sinistro;
- Valor do sinistro.

A classificação jurídica e operacional de cada variável deverá ser formalizada pela organização responsável pelos dados.

Também será necessário verificar se existem identificadores diretos ou indiretos nos dados originais.

## 6. Anonimização, pseudonimização e minimização

Esses conceitos possuem funções diferentes.

### 6.1 Anonimização

Consiste na utilização de meios técnicos razoáveis e disponíveis para impedir que um dado seja associado a um indivíduo, considerando os critérios legais aplicáveis.

Dados efetivamente anonimizados deixam de ser considerados dados pessoais nos termos da LGPD, ressalvadas as situações previstas na legislação.

### 6.2 Pseudonimização

Consiste na substituição de identificadores diretos por códigos ou identificadores alternativos.

A possibilidade de associação com o titular permanece quando existem informações adicionais que permitem a reversão ou reidentificação.

Por isso, dados pseudonimizados continuam exigindo proteção.

### 6.3 Minimização

Consiste em limitar a coleta e o tratamento às informações necessárias para a finalidade.

No projeto, essa prática deve orientar a seleção das variáveis e a disponibilização dos dados para as equipes técnicas.

## 7. Segurança da informação

A arquitetura deve implementar controles que preservem a confidencialidade, a integridade e a disponibilidade das informações.

### 7.1 Confidencialidade

Garante que as informações sejam acessadas somente por pessoas e sistemas autorizados.

Medidas recomendadas:

- Controle de acesso por perfil;
- Autenticação;
- Gestão de permissões;
- Criptografia;
- Proteção de credenciais;
- Segregação de ambientes.

### 7.2 Integridade

Busca assegurar que os dados não sejam modificados de maneira indevida.

Medidas recomendadas:

- Controle de versões;
- Registro de alterações;
- Validação de integridade;
- Logs de operações;
- Controle de acesso a arquivos;
- Rastreabilidade de transformações.

### 7.3 Disponibilidade

Busca garantir que os sistemas e dados estejam acessíveis quando necessários.

Medidas recomendadas:

- Rotinas de backup;
- Monitoramento de serviços;
- Procedimentos de recuperação;
- Gestão de incidentes;
- Planejamento de continuidade.

## 8. Controle de acesso e segregação de responsabilidades

Uma arquitetura corporativa deve estabelecer diferentes níveis de acesso.

Exemplo de organização:

| Perfil | Responsabilidade |
|---|---|
| Administrador de dados | Gerenciar permissões e estruturas de dados |
| Engenheiro de dados | Construir e manter pipelines |
| Cientista de dados | Desenvolver e avaliar modelos |
| Analista antifraude | Investigar alertas autorizados |
| Gestor | Acompanhar indicadores gerenciais |
| Auditor | Verificar registros e controles autorizados |

O acesso deve seguir o princípio do menor privilégio.

Cada usuário deve possuir somente as permissões necessárias para desempenhar suas atividades.

A segregação de responsabilidades reduz o risco de alterações não autorizadas e facilita a auditoria.

## 9. Explicabilidade dos modelos

A explicabilidade busca tornar os resultados dos modelos compreensíveis para os usuários responsáveis pela análise e pela tomada de decisão.

Em uma operação antifraude, é importante que um alerta não seja tratado como uma conclusão definitiva de fraude.

O resultado do algoritmo deve ser interpretado como uma indicação de risco que necessita de avaliação contextual.

### 9.1 Regressão Logística

A Regressão Logística possui uma estrutura matemática que permite analisar os coeficientes associados às variáveis.

A interpretação pode considerar:

- Sinal dos coeficientes;
- Magnitude;
- Odds ratios;
- Incerteza estatística, quando estimada;
- Relação entre variáveis.

A interpretação precisa considerar a codificação utilizada e a escala das variáveis.

Não é possível afirmar quais fatores mais influenciam as previsões deste projeto sem examinar os coeficientes e o processamento efetivamente aplicado.

### 9.2 Random Forest

O Random Forest pode ser interpretado por meio de técnicas de importância de variáveis e métodos de explicação local.

Entre as alternativas estão:

- Permutation Importance;
- SHAP;
- Análise de dependência parcial;
- Comparação de previsões sob diferentes condições.

A importância de uma variável não representa necessariamente causalidade.

Da mesma forma, uma explicação local representa uma interpretação da previsão em relação ao modelo, e não uma comprovação de fraude.

### 9.3 Explicabilidade local e global

A explicabilidade global procura compreender o comportamento geral do modelo.

A explicabilidade local procura esclarecer quais características contribuíram para uma previsão específica.

As duas perspectivas são complementares.

A implementação futura deverá permitir que analistas autorizados compreendam os fatores associados aos alertas, respeitando os limites técnicos das explicações e a proteção das informações pessoais.

## 10. Vieses algorítmicos e não discriminação

Modelos preditivos podem reproduzir ou ampliar padrões discriminatórios presentes nos dados históricos.

Esse risco merece atenção especial em seguros, pois classificações inadequadas podem afetar pessoas e grupos de maneira desigual.

A análise deve considerar:

- Representatividade da base;
- Qualidade dos rótulos;
- Variáveis utilizadas;
- Correlações entre atributos;
- Diferenças de desempenho entre grupos;
- Taxas de falsos positivos;
- Taxas de falsos negativos;
- Consequências das decisões apoiadas pelo modelo.

A simples remoção de uma variável sensível não garante ausência de discriminação, pois outras variáveis podem funcionar como proxies.

### 10.1 Avaliação de desempenho por grupos

Quando juridicamente adequado e tecnicamente viável, recomenda-se avaliar o desempenho em segmentos relevantes.

Podem ser acompanhados:

- Recall por segmento;
- Precisão por segmento;
- Taxa de falsos positivos;
- Taxa de falsos negativos;
- Quantidade de registros por grupo.

A comparação deve considerar o tamanho das amostras, a incerteza estatística e as limitações dos dados.

O objetivo é identificar diferenças injustificadas e estabelecer mecanismos de mitigação.

## 11. Supervisão humana e decisão assistida

A aplicação deve ser utilizada como instrumento de apoio à decisão.

Um escore de risco não constitui prova de fraude.

A confirmação deve depender de procedimentos adequados de investigação, análise documental e avaliação por profissionais autorizados.

Recomenda-se que:

1. Os alertas sejam encaminhados para análise.
2. A equipe registre a conclusão da investigação.
3. As decisões sejam justificáveis e rastreáveis.
4. Os casos inconclusivos permaneçam identificados como pendentes.
5. Os resultados das investigações sejam utilizados para avaliar a qualidade do sistema.
6. Casos de impacto relevante possuam mecanismos de revisão.

A supervisão humana deve ser efetiva e não apenas uma etapa formal de aprovação automática.

## 12. Rastreabilidade e auditoria

A rastreabilidade permite reconstruir as condições em que uma previsão foi produzida.

Recomenda-se registrar:

- Identificador do sinistro;
- Data e horário da previsão;
- Versão do modelo;
- Algoritmo utilizado;
- Variáveis disponibilizadas;
- Escore produzido;
- Limiar aplicado;
- Resultado da classificação;
- Responsável pela investigação;
- Resultado da análise;
- Alterações posteriores.

Esses registros devem respeitar critérios de minimização, retenção e controle de acesso.

O objetivo é permitir auditorias técnicas e operacionais sem criar exposição desnecessária de informações pessoais.

## 13. Governança dos modelos

A governança de modelos deve estabelecer critérios formais para desenvolvimento, avaliação, aprovação, implantação e descontinuação.

Uma estrutura recomendada contempla:

### Desenvolvimento

- Documentação da finalidade;
- Descrição dos dados;
- Registro das variáveis;
- Justificativa da escolha do algoritmo.

### Validação

- Avaliação temporal;
- Métricas estatísticas;
- Análise de erros;
- Avaliação de vieses;
- Verificação de estabilidade.

### Aprovação

- Revisão técnica;
- Revisão de riscos;
- Avaliação de segurança;
- Aprovação pelas áreas responsáveis.

### Implantação

- Controle de versão;
- Registro da configuração;
- Testes de integração;
- Plano de contingência.

### Monitoramento

- Acompanhamento de métricas;
- Monitoramento de drift;
- Revisões periódicas;
- Registro de incidentes.

### Descontinuação

- Registro da decisão;
- Preservação dos históricos necessários;
- Revogação de acessos;
- Plano de substituição ou encerramento.

## 14. Relação com o Databricks e o MLflow

Na arquitetura futura, o Databricks poderá concentrar as atividades de armazenamento, processamento e análise de dados.

O MLflow poderá apoiar a rastreabilidade dos experimentos e das versões dos modelos.

Essa integração poderá fortalecer:

- Registro de experimentos;
- Controle de versões;
- Histórico de parâmetros;
- Comparação de métricas;
- Reprodutibilidade;
- Gestão de artefatos;
- Auditoria do ciclo de vida dos modelos.

A plataforma tecnológica não substitui a definição de políticas de governança.

A organização precisa estabelecer responsáveis, regras de acesso, critérios de aprovação e processos de auditoria independentemente da ferramenta utilizada.

## 15. Gestão de incidentes e resposta a riscos

A operação deve possuir procedimentos para identificar, avaliar e responder a incidentes de segurança.

Exemplos de situações que exigem atenção:

- Acesso não autorizado;
- Exposição de informações pessoais;
- Vazamento de credenciais;
- Alteração indevida de dados;
- Manipulação de previsões;
- Indisponibilidade de serviços;
- Uso inadequado de informações.

Os procedimentos devem definir responsáveis, canais de comunicação, medidas de contenção, investigação e documentação.

Quando aplicável, a organização deverá observar as obrigações legais e regulatórias relativas à comunicação de incidentes.

## 16. Limitações atuais e requisitos de evolução

A documentação e o código disponíveis não comprovam a implementação integral de uma estrutura corporativa de governança.

Os seguintes elementos devem ser tratados como requisitos de evolução:

- Política formal de classificação de dados;
- Matriz de responsabilidades;
- Avaliação documentada das bases legais;
- Controle de acesso por perfil;
- Gestão centralizada de credenciais;
- Política de retenção e descarte;
- Auditoria de previsões;
- Análise de explicabilidade;
- Avaliação de vieses;
- Processo formal de aprovação de modelos;
- Plano de resposta a incidentes.

A implementação desses controles depende da organização responsável pelo tratamento dos dados e da infraestrutura utilizada.

## 17. Conclusão

A governança de dados, a segurança da informação e o uso responsável de inteligência artificial são componentes essenciais de uma solução de prevenção de fraudes em seguradoras.

A qualidade estatística dos modelos precisa estar acompanhada de transparência, proteção dos titulares, rastreabilidade e supervisão humana.

A adoção dos princípios da LGPD e das boas práticas de governança contribui para reduzir riscos e fortalecer a confiabilidade da solução.

A evolução arquitetural deverá incorporar controles técnicos e organizacionais que permitam utilizar Machine Learning de maneira segura, auditável e compatível com as responsabilidades da seguradora.