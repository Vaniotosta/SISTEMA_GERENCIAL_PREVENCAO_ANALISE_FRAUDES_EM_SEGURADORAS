# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# dependencies = [
#   "seaborn",
#   "shap",
# ]
# ///
# Exploracao da base de sinistros 
# ETAPA 1 — LEITURA E EXPLORAÇÃO DA BASE

from pathlib import Path
import pandas as pd

# Caminho da base no Databricks
caminho = Path(
    "/Workspace/Users/vbtosta@gmail.com/"
    "PREVENCAO-DE-FRAUDE-EM-SINISTROS/data/raw/sinistros_raw.csv"
)

# Verificar existência
if not caminho.exists():
    raise FileNotFoundError(f"Base não encontrada: {caminho}")

# Leitura
df = pd.read_csv(caminho, low_memory=False)

# 1. Dimensões
print("DIMENSÕES DA BASE")
print(f"Linhas: {df.shape[0]:,}")
print(f"Colunas: {df.shape[1]}")

# 2. Primeiros registros
print("\nAMOSTRA DOS DADOS")
display(df.head(10))

# 3. Tipos de dados
print("\nTIPOS DE DADOS")
display(df.dtypes.astype(str).to_frame("tipo"))

# 4. Valores ausentes
print("\nVALORES AUSENTES")
ausentes = pd.DataFrame({
    "quantidade": df.isna().sum(),
    "percentual": (df.isna().mean() * 100).round(2)
})
display(ausentes.sort_values("quantidade", ascending=False))

# 5. Duplicidades
print("\nDUPLICIDADES")
print("Linhas duplicadas:", df.duplicated().sum())
print("IDs duplicados:", df["id_sinistro"].duplicated().sum())

# 6. Distribuição da variável-alvo
print("\nDISTRIBUIÇÃO DE FRAUDES")
display(
    df["fraude"].value_counts()
      .rename_axis("fraude")
      .to_frame("quantidade")
)

# 7. Estatísticas descritivas
print("\nESTATÍSTICAS DESCRITIVAS")
display(df.describe(include="all").T)

# 8. Identificação de possíveis vazamentos
print("\nCOLUNAS QUE NÃO DEVEM SER PREDITIVAS")
print(["status_investigacao", "valor_recuperado"])

print("\nExploração inicial concluída.")

# COMMAND ----------

# TAXA DE FRAUDE POR TIPO DE SINISTRO

analise_tipo = (
    df.groupby("tipo_sinistro")["fraude"]
      .agg(["count", "sum", "mean"])
      .rename(columns={
          "count": "total_sinistros",
          "sum": "total_fraudes",
          "mean": "taxa_fraude"
      })
      .sort_values("taxa_fraude", ascending=False)
)

analise_tipo["taxa_fraude"] *= 100

display(analise_tipo.round(2))

# COMMAND ----------

display(analise_tipo.reset_index())


# COMMAND ----------

print("Linhas da base:", len(df))
print("Total na tabela agrupada:", analise_tipo["total_sinistros"].sum())
print("Total de fraudes na base:", df["fraude"].sum())
print("Total de fraudes na tabela:", analise_tipo["total_fraudes"].sum())


# COMMAND ----------

# PADRONIZAÇÃO DA CATEGORIA TIPO_SINISTRO

df["tipo_sinistro"] = (
    df["tipo_sinistro"]
    .str.strip()
    .str.casefold()
    .replace({
        "colisao": "colisão"
    })
)

# Conferir categorias padronizadas
display(df["tipo_sinistro"].value_counts())

# COMMAND ----------

# TAXA DE FRAUDE POR CATEGORIA PADRONIZADA

analise_tipo = (
    df.groupby("tipo_sinistro")["fraude"]
      .agg(
          total_sinistros="count",
          total_fraudes="sum",
          taxa_fraude="mean"
      )
      .sort_values("taxa_fraude", ascending=False)
)

analise_tipo["taxa_fraude"] *= 100

display(analise_tipo.round(2))

# COMMAND ----------

print(df[["valor_sinistro", "fraude"]].dtypes)
display(df[["valor_sinistro", "fraude"]].head(10))

# COMMAND ----------

import pandas as pd

def converter_valor(valor):
    if pd.isna(valor):
        return None

    if isinstance(valor, (int, float)):
        return float(valor)

    valor = str(valor).strip()
    valor = valor.replace("R$", "").replace(" ", "")
    valor = valor.replace(".", "").replace(",", ".")

    return pd.to_numeric(valor, errors="coerce")


df["valor_sinistro_num"] = df["valor_sinistro"].apply(converter_valor)

# Conferir os resultados
display(
    df[["valor_sinistro", "valor_sinistro_num"]].head(15)
)

# COMMAND ----------

import pandas as pd

def converter_valor(valor):
    if pd.isna(valor):
        return None

    if isinstance(valor, (int, float)):
        return float(valor)

    valor = str(valor).strip()
    valor = valor.replace("R$", "").replace(" ", "")

    # Formato brasileiro: 15.013,87
    if "," in valor:
        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

    # Formato decimal: 64031.04
    return pd.to_numeric(valor, errors="coerce")


df["valor_sinistro_num"] = df["valor_sinistro"].apply(converter_valor)

display(
    df[["valor_sinistro", "valor_sinistro_num"]].head(15)
)

# COMMAND ----------

# VALIDAÇÃO DA CONVERSÃO

print("Total de registros:", len(df))
print("Valores ausentes na coluna original:", df["valor_sinistro"].isna().sum())
print("Valores ausentes após conversão:", df["valor_sinistro_num"].isna().sum())
print("Valores inválidos:", df["valor_sinistro_num"].isna().sum() - df["valor_sinistro"].isna().sum())

display(df["valor_sinistro_num"].describe())

# COMMAND ----------

# ANÁLISE DA TAXA DE FRAUDE POR FAIXA DE VALOR

df["faixa_valor"] = pd.qcut(
    df["valor_sinistro_num"],
    q=5,
    duplicates="drop"
)

analise_valor = (
    df.groupby("faixa_valor", observed=True)["fraude"]
      .agg(
          total_sinistros="count",
          total_fraudes="sum",
          taxa_fraude="mean"
      )
)

analise_valor["taxa_fraude"] *= 100

display(analise_valor.round(2))

# COMMAND ----------


import os
import matplotlib.pyplot as plt
import pandas as pd

# ==================================================
# 1. CONFIGURAÇÃO DA PASTA
# ==================================================

pasta_graficos = "/Workspace/Users/vbtosta@gmail.com/PREVENCAO-DE-FRAUDE-EM-SINISTROS/reports/graficos"

os.makedirs(pasta_graficos, exist_ok=True)

# ==================================================
# 2. GRÁFICO: TAXA DE FRAUDE POR TIPO DE SINISTRO
# ==================================================

dados_tipo = (
    df.groupby("tipo_sinistro")["fraude"]
      .mean()
      .mul(100)
      .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
ax = dados_tipo.plot(kind="bar")

plt.title("Taxa de Fraude por Tipo de Sinistro")
plt.xlabel("Tipo de Sinistro")
plt.ylabel("Taxa de Fraude (%)")
plt.xticks(rotation=35, ha="right")

for i, valor in enumerate(dados_tipo):
    ax.text(i, valor + 0.15, f"{valor:.2f}%", ha="center")

plt.tight_layout()
plt.savefig(
    os.path.join(pasta_graficos, "taxa_fraude_tipo_sinistro.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# ==================================================
# 3. GRÁFICO: TAXA DE FRAUDE POR FAIXA DE VALOR
# ==================================================

dados_valor = analise_valor["taxa_fraude"]

plt.figure(figsize=(10, 6))
ax = dados_valor.plot(kind="bar")

plt.title("Taxa de Fraude por Faixa de Valor do Sinistro")
plt.xlabel("Faixa de Valor")
plt.ylabel("Taxa de Fraude (%)")
plt.xticks(rotation=25, ha="right")

for i, valor in enumerate(dados_valor):
    ax.text(i, valor + 0.15, f"{valor:.2f}%", ha="center")

plt.tight_layout()
plt.savefig(
    os.path.join(pasta_graficos, "taxa_fraude_faixa_valor.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# ==================================================
# 4. GRÁFICO: DISTRIBUIÇÃO DAS FRAUDES
# ==================================================

distribuicao = df["fraude"].value_counts().sort_index()

plt.figure(figsize=(8, 6))
plt.pie(
    distribuicao.values,
    labels=["Sem fraude", "Fraude"],
    autopct="%1.2f%%",
    startangle=90
)

plt.title("Distribuição de Fraudes na Base")
plt.tight_layout()
plt.savefig(
    os.path.join(pasta_graficos, "distribuicao_fraudes.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# ==================================================
# 5. CONFIRMAÇÃO DOS ARQUIVOS
# ==================================================

print("Gráficos gerados com sucesso!")
print("Pasta:", pasta_graficos)

for arquivo in os.listdir(pasta_graficos):
    print(arquivo)


# COMMAND ----------


# LISTAR AS COLUNAS DA BASE

for coluna in df.columns:
    print(coluna)


# COMMAND ----------


import os
import matplotlib.pyplot as plt

# 1. TABELA: TAXA DE FRAUDE POR HISTÓRICO RECENTE

analise_historico = (
    df.groupby("qtd_sinistros_12m")["fraude"]
      .agg(
          total_sinistros="count",
          total_fraudes="sum",
          taxa_fraude="mean"
      )
      .sort_index()
)

analise_historico["taxa_fraude"] *= 100

display(analise_historico.round(2))

# 2. GRÁFICO

plt.figure(figsize=(10, 6))

barras = plt.bar(
    analise_historico.index.astype(str),
    analise_historico["taxa_fraude"]
)

plt.title("Taxa de Fraude por Histórico de Sinistros (12 meses)")
plt.xlabel("Quantidade de Sinistros nos Últimos 12 Meses")
plt.ylabel("Taxa de Fraude (%)")

for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.15,
        f"{altura:.2f}%",
        ha="center"
    )

plt.tight_layout()

# 3. SALVAR

pasta_graficos = (
    "/Workspace/Users/vbtosta@gmail.com/"
    "PREVENCAO-DE-FRAUDE-EM-SINISTROS/reports/graficos"
)

os.makedirs(pasta_graficos, exist_ok=True)

plt.savefig(
    os.path.join(
        pasta_graficos,
        "taxa_fraude_historico_12m.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# COMMAND ----------


import os
import matplotlib.pyplot as plt

# 1. TABELA: TAXA DE FRAUDE POR HISTÓRICO TOTAL

analise_historico_total = (
    df.groupby("qtd_sinistros_total")["fraude"]
      .agg(
          total_sinistros="count",
          total_fraudes="sum",
          taxa_fraude="mean"
      )
      .sort_index()
)

analise_historico_total["taxa_fraude"] *= 100

display(analise_historico_total.round(2))

# 2. GRÁFICO

plt.figure(figsize=(10, 6))

barras = plt.bar(
    analise_historico_total.index.astype(str),
    analise_historico_total["taxa_fraude"]
)

plt.title("Taxa de Fraude por Histórico Total de Sinistros")
plt.xlabel("Quantidade Total de Sinistros Anteriores")
plt.ylabel("Taxa de Fraude (%)")

for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.15,
        f"{altura:.2f}%",
        ha="center"
    )

plt.tight_layout()

# 3. SALVAR O GRÁFICO

pasta_graficos = (
    "/Workspace/Users/vbtosta@gmail.com/"
    "PREVENCAO-DE-FRAUDE-EM-SINISTROS/reports/graficos"
)

os.makedirs(pasta_graficos, exist_ok=True)

plt.savefig(
    os.path.join(
        pasta_graficos,
        "taxa_fraude_historico_total.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# COMMAND ----------

# Estatísticas descritivas do score de crédito
display(df["score_credito"].describe())

# Verificar valores ausentes
print("Valores ausentes:", df["score_credito"].isna().sum())

# Verificar valores distintos
print("Quantidade de valores distintos:", df["score_credito"].nunique())

# COMMAND ----------


import pandas as pd
import matplotlib.pyplot as plt

# Criar uma cópia da variável para não alterar o score original
score_faixa = pd.qcut(
    df["score_credito"],
    q=5,
    duplicates="drop"
).astype("object")

# Identificar registros sem score
score_faixa[df["score_credito"].isna()] = "Não informado"

# Criar tabela de análise
analise_score = (
    pd.DataFrame({
        "faixa_score": score_faixa,
        "fraude": df["fraude"]
    })
    .groupby("faixa_score", observed=True)["fraude"]
    .agg(
        total_registros="count",
        total_fraudes="sum",
        taxa_fraude="mean"
    )
)

analise_score["taxa_fraude"] *= 100

display(analise_score.round(2))

# Gráfico da taxa de fraude
plt.figure(figsize=(12, 6))

plt.bar(
    analise_score.index.astype(str),
    analise_score["taxa_fraude"]
)

plt.title("Taxa de Fraude por Faixa de Score de Crédito")
plt.xlabel("Faixa de Score")
plt.ylabel("Taxa de Fraude (%)")
plt.xticks(rotation=25, ha="right")

plt.tight_layout()
plt.show()
plt.close()


# COMMAND ----------

display(df["alteracoes_apolice_90d"].value_counts().sort_index())

display(df["alteracoes_apolice_90d"].describe())

# COMMAND ----------


import matplotlib.pyplot as plt

# Agrupar os registros pela quantidade de alterações
analise_alteracoes = (
    df.groupby("alteracoes_apolice_90d")["fraude"]
      .agg(
          total_registros="count",
          total_fraudes="sum",
          taxa_fraude="mean"
      )
      .sort_index()
)

analise_alteracoes["taxa_fraude"] *= 100

# Exibir tabela
display(analise_alteracoes.round(2))

# Gerar gráfico
plt.figure(figsize=(10, 6))

barras = plt.bar(
    analise_alteracoes.index.astype(str),
    analise_alteracoes["taxa_fraude"]
)

plt.title("Taxa de Fraude por Alterações na Apólice")
plt.xlabel("Quantidade de Alterações nos Últimos 90 Dias")
plt.ylabel("Taxa de Fraude (%)")

for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.15,
        f"{altura:.2f}%",
        ha="center"
    )

plt.tight_layout()
plt.show()
plt.close()


# COMMAND ----------

display(
    df["qtd_testemunhas"]
    .value_counts(dropna=False)
    .sort_index()
)

# COMMAND ----------


import pandas as pd
import matplotlib.pyplot as plt

# Criar categorias, preservando os valores ausentes
faixa_testemunhas = df["qtd_testemunhas"].apply(
    lambda x: "Não informado" if pd.isna(x) else str(int(x))
)

# Agrupar e calcular as taxas
analise_testemunhas = (
    pd.DataFrame({
        "faixa_testemunhas": faixa_testemunhas,
        "fraude": df["fraude"]
    })
    .groupby("faixa_testemunhas")["fraude"]
    .agg(
        total_registros="count",
        total_fraudes="sum",
        taxa_fraude="mean"
    )
)

analise_testemunhas["taxa_fraude"] *= 100

# Organizar as categorias
ordem = [str(i) for i in range(8)] + ["Não informado"]
analise_testemunhas = analise_testemunhas.reindex(ordem)

# Exibir tabela
display(analise_testemunhas.round(2))

# Gerar gráfico
plt.figure(figsize=(11, 6))

plt.bar(
    analise_testemunhas.index,
    analise_testemunhas["taxa_fraude"]
)

plt.title("Taxa de Fraude por Quantidade de Testemunhas")
plt.xlabel("Quantidade de Testemunhas")
plt.ylabel("Taxa de Fraude (%)")
plt.xticks(rotation=25)

plt.tight_layout()
plt.show()
plt.close()


# COMMAND ----------

display(df["uf"].value_counts(dropna=False))

# COMMAND ----------


import pandas as pd
import matplotlib.pyplot as plt

# Padronizar espaços e letras maiúsculas
uf_normalizada = df["uf"].astype("string").str.strip().str.upper()

# Unificar nomes completos e siglas
mapa_ufs = {
    "SÃO PAULO": "SP",
    "BAHIA": "BA"
}

df["uf_normalizada"] = uf_normalizada.replace(mapa_ufs)

# Conferir a padronização
print("Distribuição após padronização:")
display(df["uf_normalizada"].value_counts(dropna=False))

# Calcular indicadores de fraude por estado
analise_uf = (
    df.groupby("uf_normalizada", dropna=False)["fraude"]
      .agg(
          total_registros="count",
          total_fraudes="sum",
          taxa_fraude="mean"
      )
      .sort_values("taxa_fraude", ascending=False)
)

analise_uf["taxa_fraude"] *= 100

# Exibir tabela
display(analise_uf.round(2))

# Criar gráfico
plt.figure(figsize=(10, 6))

barras = plt.bar(
    analise_uf.index.astype(str),
    analise_uf["taxa_fraude"]
)

plt.title("Taxa de Fraude por Estado")
plt.xlabel("Estado")
plt.ylabel("Taxa de Fraude (%)")

for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.1,
        f"{altura:.2f}%",
        ha="center"
    )

plt.tight_layout()
plt.show()
plt.close()


# COMMAND ----------

display(df["canal_venda"].value_counts(dropna=False))

# COMMAND ----------


import os
import pandas as pd
import matplotlib.pyplot as plt

# Preservar os registros sem informação
canal = df["canal_venda"].fillna("Não informado")

# Calcular indicadores
analise_canal = (
    pd.DataFrame({
        "canal_venda": canal,
        "fraude": df["fraude"]
    })
    .groupby("canal_venda")["fraude"]
    .agg(
        total_registros="count",
        total_fraudes="sum",
        taxa_fraude="mean"
    )
)

analise_canal["taxa_fraude"] *= 100

# Ordenar pela taxa de fraude
analise_canal = analise_canal.sort_values(
    "taxa_fraude",
    ascending=False
)

display(analise_canal.round(2))

# Gerar gráfico
plt.figure(figsize=(10, 6))

barras = plt.bar(
    analise_canal.index,
    analise_canal["taxa_fraude"]
)

plt.title("Taxa de Fraude por Canal de Venda")
plt.xlabel("Canal de Venda")
plt.ylabel("Taxa de Fraude (%)")

for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.1,
        f"{altura:.2f}%",
        ha="center"
    )

plt.tight_layout()

# Salvar gráfico
pasta_graficos = (
    "/Workspace/Users/vbtosta@gmail.com/"
    "PREVENCAO-DE-FRAUDE-EM-SINISTROS/reports/graficos"
)

os.makedirs(pasta_graficos, exist_ok=True)

plt.savefig(
    os.path.join(pasta_graficos, "taxa_fraude_canal_venda.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# COMMAND ----------


import os
import matplotlib.pyplot as plt
import pandas as pd

# Variáveis categóricas que ainda precisamos investigar
variaveis = [
    "tipo_cobertura",
    "estado_civil",
    "oficina_credenciada",
    "houve_vitima",
    "boletim_ocorrencia"
]

# Pasta para salvar os gráficos
pasta_graficos = (
    "/Workspace/Users/vbtosta@gmail.com/"
    "PREVENCAO-DE-FRAUDE-EM-SINISTROS/reports/graficos"
)

os.makedirs(pasta_graficos, exist_ok=True)

# Dicionário para armazenar os resultados
resultados_eda = {}

for coluna in variaveis:

    # Preservar os valores ausentes
    categoria = df[coluna].astype("object").fillna("Não informado")

    # Calcular indicadores
    tabela = (
        pd.DataFrame({
            "categoria": categoria,
            "fraude": df["fraude"]
        })
        .groupby("categoria", dropna=False)["fraude"]
        .agg(
            total_registros="count",
            total_fraudes="sum",
            taxa_fraude="mean"
        )
    )

    tabela["taxa_fraude"] *= 100
    tabela["participacao"] = (
        tabela["total_registros"] / len(df) * 100
    )

    tabela = tabela.sort_values(
        "taxa_fraude",
        ascending=False
    )

    resultados_eda[coluna] = tabela

    print(f"\n========== {coluna.upper()} ==========")
    display(tabela.round(2))

    # Gráfico
    plt.figure(figsize=(10, 5))

    plt.bar(
        tabela.index.astype(str),
        tabela["taxa_fraude"]
    )

    plt.title(f"Taxa de Fraude por {coluna}")
    plt.xlabel("Categoria")
    plt.ylabel("Taxa de Fraude (%)")
    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()

    nome_arquivo = f"taxa_fraude_{coluna}.png"

    plt.savefig(
        os.path.join(pasta_graficos, nome_arquivo),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

print("\nAnálises concluídas.")
print("Gráficos salvos em:", pasta_graficos)


# COMMAND ----------

# MAGIC %md
# MAGIC # Relatório de Análise Exploratória de Dados (EDA)
# MAGIC ## Projeto: Prevenção de Fraudes em Sinistros de Seguros
# MAGIC
# MAGIC **Ambiente:** Databricks Free Edition  
# MAGIC **Linguagem:** Python  
# MAGIC **Objetivo:** Identificar padrões associados à ocorrência de fraudes em sinistros e levantar evidências para orientar o desenvolvimento de modelos preditivos de classificação.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 1. Objetivo da análise
# MAGIC
# MAGIC Esta análise exploratória teve como objetivo compreender o comportamento dos dados de sinistros, avaliar sua qualidade, identificar possíveis associações entre características dos segurados, apólices e ocorrências e levantar variáveis potencialmente relevantes para a construção de um modelo de detecção de fraudes.
# MAGIC
# MAGIC A investigação foi conduzida considerando aspectos como:
# MAGIC
# MAGIC - Distribuição dos registros e da variável-alvo;
# MAGIC - Qualidade e consistência dos dados;
# MAGIC - Valores ausentes e duplicidades;
# MAGIC - Distribuição de variáveis numéricas e categóricas;
# MAGIC - Taxas de fraude por grupos e categorias;
# MAGIC - Identificação de possíveis variáveis preditoras;
# MAGIC - Riscos de vazamento de informação (*data leakage*).
# MAGIC
# MAGIC Os resultados apresentados são exploratórios e representam associações observadas na base, não relações causais.
# MAGIC
# MAGIC ## 2. Caracterização da base de dados
# MAGIC
# MAGIC A base analisada possui **20.300 registros e 30 variáveis originais**, além de duas colunas criadas durante a exploração: `valor_sinistro_num` e `faixa_valor`.
# MAGIC
# MAGIC A variável-alvo é `fraude`, que identifica se determinado sinistro foi classificado como fraudulento.
# MAGIC
# MAGIC Distribuição da variável-alvo:
# MAGIC
# MAGIC | Classificação | Registros | Participação |
# MAGIC |---|---:|---:|
# MAGIC | Não fraude (0) | 18.931 | 93,26% |
# MAGIC | Fraude (1) | 1.369 | 6,74% |
# MAGIC | **Total** | **20.300** | **100%** |
# MAGIC
# MAGIC A base apresenta desbalanceamento entre as classes, com aproximadamente 6,74% de registros fraudulentos.
# MAGIC
# MAGIC Esse aspecto deverá ser considerado durante a modelagem, pois modelos treinados sem estratégias adequadas podem apresentar alta acurácia e, ainda assim, baixa capacidade de identificar fraudes.
# MAGIC
# MAGIC ## 3. Qualidade e consistência dos dados
# MAGIC
# MAGIC Durante a exploração foram identificados problemas que precisam ser tratados antes do treinamento dos modelos.
# MAGIC
# MAGIC ### 3.1 Registros duplicados
# MAGIC
# MAGIC Foram identificados:
# MAGIC
# MAGIC - 300 linhas duplicadas;
# MAGIC - 300 identificadores `id_sinistro` duplicados.
# MAGIC
# MAGIC Isso representa aproximadamente 1,48% da base.
# MAGIC
# MAGIC Antes da remoção, será necessário verificar se os registros com o mesmo identificador possuem informações idênticas ou conflitantes. Caso sejam duplicações exatas, deverão ser tratados em uma base de trabalho separada, preservando os dados originais.
# MAGIC
# MAGIC As taxas de fraude calculadas nesta etapa ainda consideram essas duplicidades.
# MAGIC
# MAGIC ### 3.2 Valores ausentes
# MAGIC
# MAGIC | Variável | Valores ausentes | Participação |
# MAGIC |---|---:|---:|
# MAGIC | `qtd_testemunhas` | 2.454 | 12,09% |
# MAGIC | `renda_mensal` | 1.959 | 9,65% |
# MAGIC | `score_credito` | 1.644 | 8,10% |
# MAGIC | `oficina_credenciada` | 1.205 | 5,94% |
# MAGIC | `estado_civil` | 600 | 2,96% |
# MAGIC | `canal_venda` | 383 | 1,89% |
# MAGIC
# MAGIC A ausência de informações deverá ser investigada antes da imputação. Em algumas variáveis, como score de crédito e canal de venda, os registros sem informação apresentaram taxas de fraude diferentes das observadas em determinadas categorias preenchidas.
# MAGIC
# MAGIC Portanto, a ausência de informação poderá ser representada por uma categoria própria ou por indicadores de ausência, conforme o tipo de variável e o desempenho observado na validação.
# MAGIC
# MAGIC ### 3.3 Valores inconsistentes
# MAGIC
# MAGIC Foram identificados valores suspeitos nas variáveis numéricas:
# MAGIC
# MAGIC - `idade`: mínimo de -1 e máximo de 999;
# MAGIC - `tempo_cliente_anos`: mínimo de -1;
# MAGIC - `renda_mensal` e `valor_segurado`: apresentam valores extremos que precisam ser investigados.
# MAGIC
# MAGIC Esses valores não devem ser removidos automaticamente. Será necessário verificar sua origem e definir regras de tratamento.
# MAGIC
# MAGIC ### 3.4 Padronização de categorias
# MAGIC
# MAGIC A variável `tipo_sinistro` apresentava inconsistências de escrita, como diferenças de letras maiúsculas, minúsculas e espaços.
# MAGIC
# MAGIC Foi realizada uma normalização para unificar categorias equivalentes.
# MAGIC
# MAGIC A variável `uf` também apresentava categorias fragmentadas, como `SP`, `sp` e `São Paulo`. Foi criada a coluna `uf_normalizada`, que consolidou os estados em oito categorias.
# MAGIC
# MAGIC A coluna original foi preservada.
# MAGIC
# MAGIC ### 3.5 Conversão de valores monetários
# MAGIC
# MAGIC A variável `valor_sinistro` apresentava formatos numéricos e monetários brasileiros misturados.
# MAGIC
# MAGIC Foi criada a coluna `valor_sinistro_num`, convertendo os valores para formato numérico.
# MAGIC
# MAGIC A validação identificou:
# MAGIC
# MAGIC - 20.300 registros;
# MAGIC - Nenhum valor ausente após a conversão;
# MAGIC - Nenhum valor inválido após a conversão.
# MAGIC
# MAGIC Estatísticas do valor do sinistro:
# MAGIC
# MAGIC | Estatística | Valor |
# MAGIC |---|---:|
# MAGIC | Média | R$ 20.004,47 |
# MAGIC | Mediana | R$ 16.325,84 |
# MAGIC | Desvio-padrão | R$ 15.343,98 |
# MAGIC | Mínimo | R$ 752,17 |
# MAGIC | Máximo | R$ 163.935,40 |
# MAGIC
# MAGIC A média superior à mediana sugere assimetria à direita, possivelmente influenciada por sinistros de valores elevados.
# MAGIC
# MAGIC Os valores extremos deverão ser investigados, sem exclusão automática.
# MAGIC
# MAGIC ## 4. Análise das variáveis e principais descobertas
# MAGIC
# MAGIC ### 4.1 Tipo de sinistro
# MAGIC
# MAGIC Após a normalização, foram identificadas cinco categorias:
# MAGIC
# MAGIC | Tipo de sinistro | Registros | Fraudes | Taxa de fraude |
# MAGIC |---|---:|---:|---:|
# MAGIC | Incêndio | 990 | 100 | 10,10% |
# MAGIC | Furto | 2.409 | 235 | 9,76% |
# MAGIC | Roubo | 3.113 | 299 | 9,60% |
# MAGIC | Danos naturais | 2.645 | 148 | 5,60% |
# MAGIC | Colisão | 11.143 | 587 | 5,27% |
# MAGIC
# MAGIC **Insight:** incêndio apresentou a maior taxa proporcional de fraude, enquanto colisão concentrou o maior número absoluto de fraudes.
# MAGIC
# MAGIC **Evidência para modelagem:** `tipo_sinistro` é uma variável categórica candidata à modelagem, pois apresenta diferenças nas taxas de fraude entre as categorias.
# MAGIC
# MAGIC ### 4.2 Valor do sinistro
# MAGIC
# MAGIC A variável `valor_sinistro_num` apresentou aumento progressivo da taxa de fraude entre os cinco grupos de valores.
# MAGIC
# MAGIC | Faixa de valor | Registros | Fraudes | Taxa de fraude |
# MAGIC |---|---:|---:|---:|
# MAGIC | 1º quintil | 4.060 | 129 | 3,18% |
# MAGIC | 2º quintil | 4.060 | 191 | 4,70% |
# MAGIC | 3º quintil | 4.060 | 268 | 6,60% |
# MAGIC | 4º quintil | 4.060 | 360 | 8,87% |
# MAGIC | 5º quintil | 4.060 | 421 | 10,37% |
# MAGIC
# MAGIC **Insight:** o grupo de maior valor apresentou taxa de fraude aproximadamente 3,26 vezes superior à do grupo de menor valor.
# MAGIC
# MAGIC **Evidência para modelagem:** `valor_sinistro_num` é uma variável prioritária para avaliação preditiva. Sua relação com a fraude deverá ser testada também como variável contínua, sem depender exclusivamente das faixas criadas para a EDA.
# MAGIC
# MAGIC ### 4.3 Histórico de sinistros nos últimos 12 meses
# MAGIC
# MAGIC | Sinistros anteriores | Registros | Fraudes | Taxa de fraude |
# MAGIC |---:|---:|---:|---:|
# MAGIC | 0 | 14.295 | 773 | 5,41% |
# MAGIC | 1 | 5.051 | 459 | 9,09% |
# MAGIC | 2 | 858 | 117 | 13,64% |
# MAGIC | 3 | 91 | 20 | 21,98% |
# MAGIC | 4 | 5 | 0 | 0,00% |
# MAGIC
# MAGIC **Insight:** a taxa de fraude aumentou de 5,41% para 21,98% entre os registros com zero e três sinistros anteriores nos últimos 12 meses.
# MAGIC
# MAGIC A categoria com quatro sinistros possui somente cinco registros, não permitindo uma conclusão confiável.
# MAGIC
# MAGIC **Evidência para modelagem:** `qtd_sinistros_12m` é uma variável candidata importante, especialmente por apresentar um padrão crescente nas categorias com maior volume de observações.
# MAGIC
# MAGIC ### 4.4 Histórico total de sinistros
# MAGIC
# MAGIC | Sinistros anteriores | Registros | Fraudes | Taxa de fraude |
# MAGIC |---:|---:|---:|---:|
# MAGIC | 0 | 6.410 | 348 | 5,43% |
# MAGIC | 1 | 7.459 | 500 | 6,70% |
# MAGIC | 2 | 4.270 | 334 | 7,82% |
# MAGIC | 3 | 1.597 | 137 | 8,58% |
# MAGIC | 4 | 443 | 35 | 7,90% |
# MAGIC | 5 | 102 | 13 | 12,75% |
# MAGIC | 6 | 16 | 2 | 12,50% |
# MAGIC | 7 | 3 | 0 | 0,00% |
# MAGIC
# MAGIC **Insight:** foi observada uma tendência de aumento da taxa de fraude conforme cresce o histórico acumulado de sinistros, embora o comportamento não seja perfeitamente linear.
# MAGIC
# MAGIC **Evidência para modelagem:** `qtd_sinistros_total` é uma variável candidata relevante. Deve ser avaliada juntamente com `qtd_sinistros_12m`, verificando possível redundância e correlação entre as duas.
# MAGIC
# MAGIC ### 4.5 Score de crédito
# MAGIC
# MAGIC A variável `score_credito` apresentou:
# MAGIC
# MAGIC | Estatística | Valor |
# MAGIC |---|---:|
# MAGIC | Registros com score | 18.656 |
# MAGIC | Registros sem score | 1.644 |
# MAGIC | Média | 649,66 |
# MAGIC | Mediana | 649 |
# MAGIC | Desvio-padrão | 119,35 |
# MAGIC | Mínimo | 250 |
# MAGIC | Máximo | 950 |
# MAGIC
# MAGIC A taxa de fraude por quintil foi:
# MAGIC
# MAGIC | Grupo de score | Registros | Fraudes | Taxa de fraude |
# MAGIC |---|---:|---:|---:|
# MAGIC | Menor score | 3.763 | 380 | 10,10% |
# MAGIC | 2º grupo | 3.752 | 295 | 7,86% |
# MAGIC | 3º grupo | 3.758 | 242 | 6,44% |
# MAGIC | 4º grupo | 3.668 | 207 | 5,64% |
# MAGIC | Maior score | 3.715 | 115 | 3,10% |
# MAGIC | Não informado | 1.644 | 130 | 7,91% |
# MAGIC
# MAGIC **Insight:** foi observada uma relação inversa entre score de crédito e taxa de fraude. O grupo com menor score apresentou taxa de 10,10%, enquanto o grupo com maior score apresentou 3,10%.
# MAGIC
# MAGIC Os registros sem score apresentaram taxa de 7,91%, acima da taxa geral da base.
# MAGIC
# MAGIC **Evidência para modelagem:** `score_credito` é uma das variáveis candidatas prioritárias. A ausência de score também deverá ser investigada e tratada.
# MAGIC
# MAGIC ### 4.6 Alterações na apólice nos últimos 90 dias
# MAGIC
# MAGIC | Alterações | Registros | Fraudes | Taxa de fraude |
# MAGIC |---:|---:|---:|---:|
# MAGIC | 0 | 13.481 | 767 | 5,69% |
# MAGIC | 1 | 5.517 | 440 | 7,98% |
# MAGIC | 2 | 1.123 | 134 | 11,93% |
# MAGIC | 3 | 163 | 27 | 16,56% |
# MAGIC | 4 | 16 | 1 | 6,25% |
# MAGIC
# MAGIC **Insight:** a taxa de fraude aumentou de 5,69% para 16,56% entre zero e três alterações recentes.
# MAGIC
# MAGIC A categoria com quatro alterações apresenta somente 16 registros, exigindo cautela.
# MAGIC
# MAGIC **Evidência para modelagem:** `alteracoes_apolice_90d` é uma variável candidata relevante, com associação observada entre alterações recentes e ocorrência de fraude.
# MAGIC
# MAGIC ### 4.7 Quantidade de testemunhas
# MAGIC
# MAGIC | Testemunhas | Registros | Fraudes | Taxa de fraude |
# MAGIC |---:|---:|---:|---:|
# MAGIC | 0 | 5.475 | 490 | 8,95% |
# MAGIC | 1 | 6.440 | 363 | 5,64% |
# MAGIC | 2 | 3.880 | 231 | 5,95% |
# MAGIC | 3 | 1.474 | 86 | 5,83% |
# MAGIC | 4 | 456 | 29 | 6,36% |
# MAGIC | 5 | 107 | 7 | 6,54% |
# MAGIC | 6 | 13 | 1 | 7,69% |
# MAGIC | 7 | 1 | 0 | 0,00% |
# MAGIC | Não informado | 2.454 | 162 | 6,60% |
# MAGIC
# MAGIC **Insight:** os registros sem testemunhas apresentaram taxa de fraude de 8,95%, superior à observada nos registros com uma ou mais testemunhas em categorias com volume representativo.
# MAGIC
# MAGIC Não foi identificada uma relação linear entre quantidade de testemunhas e fraude.
# MAGIC
# MAGIC **Evidência para modelagem:** `qtd_testemunhas` pode ser útil, principalmente para distinguir a ausência de testemunhas das demais situações. Os valores ausentes e categorias raras precisam de tratamento adequado.
# MAGIC
# MAGIC ### 4.8 Estado do sinistro
# MAGIC
# MAGIC Após padronização, foram identificados oito estados:
# MAGIC
# MAGIC | Estado | Registros | Fraudes | Taxa de fraude |
# MAGIC |---|---:|---:|---:|
# MAGIC | BA | 1.981 | 154 | 7,77% |
# MAGIC | PR | 1.875 | 140 | 7,47% |
# MAGIC | PE | 1.602 | 112 | 6,99% |
# MAGIC | RS | 1.575 | 106 | 6,73% |
# MAGIC | SP | 6.107 | 405 | 6,63% |
# MAGIC | RJ | 3.136 | 204 | 6,51% |
# MAGIC | MG | 2.423 | 153 | 6,31% |
# MAGIC | SC | 1.601 | 95 | 5,93% |
# MAGIC
# MAGIC **Insight:** foram observadas diferenças regionais na taxa de fraude. A Bahia apresentou a maior taxa, enquanto Santa Catarina apresentou a menor.
# MAGIC
# MAGIC São Paulo concentrou o maior número absoluto de fraudes, com 405 ocorrências, mas não apresentou a maior taxa proporcional.
# MAGIC
# MAGIC **Evidência para modelagem:** `uf_normalizada` é uma variável candidata à modelagem. Sua contribuição deverá ser avaliada sem presumir que diferenças regionais observadas na base sintética representem padrões reais.
# MAGIC
# MAGIC ### 4.9 Canal de venda
# MAGIC
# MAGIC | Canal | Registros | Fraudes | Taxa de fraude |
# MAGIC |---|---:|---:|---:|
# MAGIC | Não informado | 383 | 41 | 10,70% |
# MAGIC | Telefone | 1.970 | 149 | 7,56% |
# MAGIC | Corretor | 9.908 | 661 | 6,67% |
# MAGIC | Online | 5.022 | 332 | 6,61% |
# MAGIC | Agência | 3.017 | 186 | 6,17% |
# MAGIC
# MAGIC **Insight:** os registros sem informação sobre o canal apresentaram a maior taxa de fraude, de 10,70%. Entre os canais identificados, Telefone apresentou a maior taxa, de 7,56%.
# MAGIC
# MAGIC **Evidência para modelagem:** `canal_venda` é uma variável candidata. A ausência de informação deve ser preservada e avaliada como possível indicador.
# MAGIC
# MAGIC ## 5. Perguntas de negócio e evidências encontradas
# MAGIC
# MAGIC A análise exploratória foi orientada por perguntas que poderiam apoiar uma operação de prevenção a fraudes.
# MAGIC
# MAGIC | Pergunta de negócio | Evidência encontrada | Implicação para o modelo |
# MAGIC |---|---|---|
# MAGIC | Sinistros de maior valor apresentam maior risco de fraude? | A taxa aumentou de 3,18% para 10,37% entre os quintis de valor. | Avaliar `valor_sinistro_num` como variável preditora. |
# MAGIC | O histórico de sinistros está associado à fraude? | A taxa aumentou com o histórico recente e total, principalmente nas categorias com volume suficiente. | Avaliar `qtd_sinistros_12m` e `qtd_sinistros_total`. |
# MAGIC | O score de crédito diferencia perfis de fraude? | A taxa caiu de 10,10% no menor quintil para 3,10% no maior. | Priorizar a avaliação de `score_credito`. |
# MAGIC | Alterações recentes na apólice estão associadas à fraude? | A taxa subiu de 5,69% para 16,56% entre zero e três alterações. | Avaliar `alteracoes_apolice_90d`. |
# MAGIC | A ausência de testemunhas apresenta comportamento diferente? | A categoria zero testemunhas apresentou taxa de 8,95%. | Avaliar `qtd_testemunhas` e sua ausência. |
# MAGIC | Existem diferenças regionais? | As taxas variaram de 5,93% a 7,77% entre os estados. | Testar `uf_normalizada`. |
# MAGIC | O canal de venda apresenta diferenças? | Telefone apresentou 7,56%; registros sem informação, 10,70%. | Avaliar `canal_venda` e valores ausentes. |
# MAGIC | O tipo de ocorrência influencia a distribuição de fraude? | Incêndio apresentou 10,10%, contra 5,27% em colisão. | Avaliar `tipo_sinistro`. |
# MAGIC
# MAGIC Essas perguntas transformam os resultados exploratórios em hipóteses que poderão ser testadas durante a modelagem.
# MAGIC
# MAGIC ## 6. Variáveis prioritárias para modelagem preditiva
# MAGIC
# MAGIC Com base nas associações observadas, as seguintes variáveis devem receber prioridade na primeira versão do modelo:
# MAGIC
# MAGIC | Prioridade exploratória | Variável | Evidência principal | Tratamento previsto |
# MAGIC |---|---|---|---|
# MAGIC | Alta | `valor_sinistro_num` | Crescimento da taxa entre os quintis de valor. | Numérica; avaliar assimetria e valores extremos. |
# MAGIC | Alta | `score_credito` | Relação inversa entre score e fraude. | Numérica; tratar valores ausentes. |
# MAGIC | Alta | `qtd_sinistros_12m` | Aumento da taxa conforme o histórico recente. | Numérica discreta; avaliar categorias raras. |
# MAGIC | Alta | `alteracoes_apolice_90d` | Aumento da taxa com alterações recentes. | Numérica discreta; avaliar categorias raras. |
# MAGIC | Alta | `qtd_sinistros_total` | Associação entre histórico acumulado e fraude. | Numérica discreta; avaliar redundância com histórico de 12 meses. |
# MAGIC | Média | `tipo_sinistro` | Diferenças relevantes entre tipos de ocorrência. | Categórica; normalizar e codificar. |
# MAGIC | Média | `uf_normalizada` | Diferenças entre estados. | Categórica; codificar. |
# MAGIC | Média | `canal_venda` | Diferenças entre canais e ausência de informação. | Categórica; preservar ausência. |
# MAGIC | Média | `qtd_testemunhas` | Maior taxa na categoria sem testemunhas. | Numérica discreta; tratar ausências e raridades. |
# MAGIC
# MAGIC **Importante:** essa classificação é uma priorização exploratória, não uma medida definitiva de importância preditiva. A importância real das variáveis será verificada por validação cruzada, métricas de desempenho e técnicas de explicabilidade, como SHAP.
# MAGIC
# MAGIC ## 7. Variáveis que exigem atenção por possível vazamento de informação
# MAGIC
# MAGIC Algumas colunas não devem ser utilizadas automaticamente como preditoras.
# MAGIC
# MAGIC | Variável | Risco metodológico |
# MAGIC |---|---|
# MAGIC | `status_investigacao` | Pode representar uma informação conhecida somente após a investigação. |
# MAGIC | `valor_recuperado` | Pode ser conhecido somente depois da ocorrência e do processo de recuperação. |
# MAGIC | `id_sinistro` | Identificador, sem justificativa para uso preditivo direto. |
# MAGIC | `id_segurado` | Identificador; pode permitir memorização de clientes e vazamento entre conjuntos. |
# MAGIC | `pais` | Apresenta apenas uma categoria, não oferecendo discriminação na base atual. |
# MAGIC
# MAGIC As datas também precisam ser avaliadas conforme o momento em que a previsão seria realizada. Por exemplo, `data_aviso` pode ser utilizável se a previsão ocorrer após o aviso do sinistro, mas não necessariamente em um momento anterior.
# MAGIC
# MAGIC Será necessário definir formalmente o momento da previsão e garantir que todas as variáveis estejam disponíveis naquele instante.
# MAGIC
# MAGIC ## 8. Principais evidências para a construção do modelo
# MAGIC
# MAGIC A EDA fornece evidências de que existem padrões potencialmente úteis para diferenciar sinistros fraudulentos e não fraudulentos.
# MAGIC
# MAGIC Os resultados mais expressivos foram:
# MAGIC
# MAGIC 1. **Valor do sinistro:** taxa de 10,37% no quintil de maior valor, contra 3,18% no menor.
# MAGIC 2. **Score de crédito:** taxa de 10,10% no quintil de menor score, contra 3,10% no maior.
# MAGIC 3. **Histórico recente:** taxa de 21,98% na categoria de três sinistros anteriores, embora com apenas 91 registros.
# MAGIC 4. **Alterações recentes na apólice:** taxa de 16,56% na categoria de três alterações, com 163 registros.
# MAGIC 5. **Tipo de sinistro:** incêndio apresentou taxa de 10,10%.
# MAGIC 6. **Ausência de testemunhas:** taxa de 8,95%.
# MAGIC 7. **Canal de venda:** registros sem informação apresentaram taxa de 10,70%.
# MAGIC
# MAGIC Essas evidências justificam testar as variáveis em modelos preditivos, mas não garantem que todas contribuirão para melhorar a capacidade de classificação.
# MAGIC
# MAGIC ## 9. Limitações da análise
# MAGIC
# MAGIC Os resultados devem ser interpretados considerando as seguintes limitações:
# MAGIC
# MAGIC - A base é sintética, gerada programaticamente para simular uma operação de seguros.
# MAGIC - Foram identificados 300 registros duplicados, ainda não tratados.
# MAGIC - As taxas apresentadas foram calculadas antes da deduplicação.
# MAGIC - Algumas categorias possuem poucos registros, tornando suas taxas instáveis.
# MAGIC - A análise exploratória identifica associações, não causalidade.
# MAGIC - Ainda não foi realizada validação estatística formal da contribuição individual das variáveis.
# MAGIC - Os resultados não representam impacto comercial comprovado nem desempenho de um sistema real em produção.
# MAGIC
# MAGIC As taxas deverão ser recalculadas após a limpeza da base.
# MAGIC
# MAGIC ## 10. Próximas etapas do projeto
# MAGIC
# MAGIC A partir das evidências encontradas, recomenda-se seguir a seguinte sequência:
# MAGIC
# MAGIC **Etapa 1 — Limpeza e qualidade dos dados**
# MAGIC - Investigar os 300 registros duplicados.
# MAGIC - Verificar identificadores repetidos e possíveis conflitos.
# MAGIC - Tratar valores inválidos de idade e tempo de relacionamento.
# MAGIC - Investigar valores extremos.
# MAGIC - Definir estratégias para valores ausentes.
# MAGIC - Consolidar as regras de padronização.
# MAGIC
# MAGIC **Etapa 2 — Engenharia de atributos**
# MAGIC - Converter e tratar variáveis numéricas.
# MAGIC - Codificar variáveis categóricas.
# MAGIC - Criar atributos derivados quando houver justificativa de negócio.
# MAGIC - Excluir identificadores e variáveis com vazamento de informação.
# MAGIC - Avaliar correlação e redundância entre variáveis.
# MAGIC
# MAGIC **Etapa 3 — Modelagem preditiva**
# MAGIC - Criar conjunto de treino e teste.
# MAGIC - Estabelecer um modelo de referência (*baseline*).
# MAGIC - Treinar modelos de classificação.
# MAGIC - Comparar Random Forest, Regressão Logística e Gradient Boosting, conforme a compatibilidade do ambiente.
# MAGIC - Realizar validação cruzada.
# MAGIC - Considerar o desbalanceamento da variável-alvo.
# MAGIC
# MAGIC **Etapa 4 — Avaliação e explicabilidade**
# MAGIC - Avaliar Precision, Recall, F1-score, ROC-AUC e PR-AUC.
# MAGIC - Analisar matriz de confusão.
# MAGIC - Avaliar calibração das probabilidades.
# MAGIC - Investigar importância das variáveis com SHAP.
# MAGIC - Estimar custos de falsos positivos e falsos negativos.
# MAGIC - Comparar o modelo inicial com a versão aprimorada.
# MAGIC
# MAGIC ## 11. Conclusão
# MAGIC
# MAGIC A análise exploratória identificou padrões relevantes em variáveis relacionadas ao valor do sinistro, histórico de ocorrências, score de crédito, alterações recentes na apólice, tipo de sinistro, quantidade de testemunhas, estado e canal de venda.
# MAGIC
# MAGIC Entre elas, `valor_sinistro_num`, `score_credito`, `qtd_sinistros_12m`, `qtd_sinistros_total` e `alteracoes_apolice_90d` apresentam evidências exploratórias particularmente interessantes para a modelagem.
# MAGIC
# MAGIC A próxima etapa será realizar a limpeza e preparação dos dados, preservando a rastreabilidade das transformações. Em seguida, será possível avaliar quais dessas variáveis realmente contribuem para a identificação de fraudes em modelos de Machine Learning.
# MAGIC
# MAGIC O objetivo não será apenas maximizar a acurácia, mas desenvolver um modelo capaz de identificar uma parcela relevante das fraudes, controlar falsos alertas e produzir probabilidades úteis para apoiar a priorização de sinistros.
# MAGIC
# MAGIC **Observação final:** por se tratar de uma base sintética, os resultados devem ser apresentados como experimentais e técnicos, sem extrapolação direta para o comportamento de uma seguradora real.

# COMMAND ----------


# Verificar duplicidades por identificador do sinistro

duplicados_id = df[
    df["id_sinistro"].duplicated(keep=False)
].sort_values("id_sinistro")

print("Registros envolvidos em IDs repetidos:", len(duplicados_id))

print(
    "Quantidade de IDs de sinistro repetidos:",
    duplicados_id["id_sinistro"].nunique()
)

# Verificar se os registros com o mesmo ID são exatamente iguais
print(
    "Linhas integralmente duplicadas:",
    df.duplicated().sum()
)

# Verificar quantos IDs repetidos apresentam informações conflitantes
colunas_comparacao = [
    coluna for coluna in df.columns
    if coluna not in ["valor_sinistro_num", "faixa_valor", "uf_normalizada"]
]

conflitos = (
    duplicados_id.groupby("id_sinistro")[colunas_comparacao]
    .nunique(dropna=False)
    .gt(1)
    .any(axis=1)
)

print(
    "IDs repetidos com informações conflitantes:",
    conflitos.sum()
)


# COMMAND ----------


# Criar uma cópia sem duplicações de ID
df_limpo = df.drop_duplicates(
    subset="id_sinistro",
    keep="first"
).copy()

# Validar o resultado
print("Registros originais:", len(df))
print("Registros após deduplicação:", len(df_limpo))
print(
    "IDs duplicados restantes:",
    df_limpo["id_sinistro"].duplicated().sum()
)

print(
    "Dimensões da nova base:",
    df_limpo.shape
)

# Verificar distribuição da variável-alvo após limpeza
display(
    df_limpo["fraude"]
    .value_counts()
    .to_frame("quantidade")
)


# COMMAND ----------

for coluna in ["idade", "tempo_cliente_anos"]:
    print(f"\n===== {coluna} =====")

    print("Quantidade de valores negativos:",
          (df_limpo[coluna] < 0).sum())

    print("Quantidade de valores nulos:",
          df_limpo[coluna].isna().sum())

    print("Menores valores:")
    display(
        df_limpo[coluna]
        .value_counts()
        .sort_index()
        .head(10)
    )

    print("Maiores valores:")
    display(
        df_limpo[coluna]
        .value_counts()
        .sort_index()
        .tail(10)
    )

# COMMAND ----------

print("===== IDADE =====")

print("Idades abaixo de 18:")
print((df_limpo["idade"] < 18).sum())

print("Idades acima de 100:")
print((df_limpo["idade"] > 100).sum())

print("\n===== TEMPO DE CLIENTE =====")

print("Valores abaixo de zero:")
print((df_limpo["tempo_cliente_anos"] < 0).sum())

print("Valores acima de 30:")
print((df_limpo["tempo_cliente_anos"] > 30).sum())

print("\nDistribuição das idades:")
display(
    df_limpo["idade"]
    .value_counts()
    .sort_index()
    .to_frame("quantidade")
)


# COMMAND ----------

# Criar cópia de trabalho para o tratamento
df_limpo = df_limpo.copy()

# Substituir idades fora do intervalo válido por valores ausentes
df_limpo.loc[
    (df_limpo["idade"] < 18) | (df_limpo["idade"] > 100),
    "idade"
] = float("nan")

# Substituir tempo de relacionamento negativo por valor ausente
df_limpo.loc[
    df_limpo["tempo_cliente_anos"] < 0,
    "tempo_cliente_anos"
] = float("nan")

# Conferir o resultado
display(
    df_limpo[["idade", "tempo_cliente_anos"]]
    .isna()
    .sum()
    .to_frame("valores ausentes após tratamento")
)

print("Total de registros preservados:", len(df_limpo))

# COMMAND ----------

import pandas as pd
import matplotlib.pyplot as plt

# Calcular quantidade e percentual de valores ausentes
resumo_ausentes = pd.DataFrame({
    "quantidade": df_limpo.isna().sum(),
    "percentual": (df_limpo.isna().mean() * 100).round(2)
})

# Manter apenas colunas com valores ausentes
resumo_ausentes = (
    resumo_ausentes[resumo_ausentes["quantidade"] > 0]
    .sort_values("quantidade", ascending=False)
)

print("Diagnóstico de valores ausentes:")
display(resumo_ausentes)

# Gráfico da quantidade de valores ausentes
plt.figure(figsize=(10, 6))

resumo_ausentes["quantidade"].sort_values().plot(
    kind="barh"
)

plt.title("Quantidade de valores ausentes por variável")
plt.xlabel("Quantidade de registros")
plt.ylabel("Variáveis")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# COMMAND ----------

print("===== TIPOS DAS COLUNAS =====")

display(
    pd.DataFrame({
        "coluna": df_limpo.columns,
        "tipo": df_limpo.dtypes.astype(str).values,
        "valores_unicos": [
            df_limpo[col].nunique()
            for col in df_limpo.columns
        ],
        "ausentes": df_limpo.isna().sum().values
    })
)

# COMMAND ----------

colunas_categoricas = [
    "estado_civil",
    "tipo_cobertura",
    "canal_venda",
    "tipo_sinistro",
    "uf",
    "boletim_ocorrencia",
    "houve_vitima",
    "oficina_credenciada"
]

for coluna in colunas_categoricas:
    print(f"\n===== {coluna} =====")

    display(
        df_limpo[coluna]
        .value_counts(dropna=False)
        .to_frame("quantidade")
    )

# COMMAND ----------

for coluna in colunas_categoricas:
    print(f"\n===== {coluna} =====")
    print(df_limpo[coluna].value_counts(dropna=False).to_string())

# COMMAND ----------

# Padronizar tipo de cobertura
df_limpo["tipo_cobertura"] = (
    df_limpo["tipo_cobertura"]
    .astype("string")
    .str.strip()
    .str.casefold()
    .replace({
        "colisao": "colisão"
    })
)

# Padronizar boletim de ocorrência
df_limpo["boletim_ocorrencia"] = (
    df_limpo["boletim_ocorrencia"]
    .astype("string")
    .str.strip()
    .str.casefold()
    .replace({
        "sim": "Sim",
        "s": "Sim",
        "não": "Não",
        "n": "Não"
    })
)

# Padronizar UF
df_limpo["uf"] = (
    df_limpo["uf"]
    .astype("string")
    .str.strip()
    .str.upper()
    .replace({
        "SÃO PAULO": "SP",
        "BAHIA": "BA"
    })
)

# Conferir as categorias após a padronização
for coluna in [
    "tipo_cobertura",
    "boletim_ocorrencia",
    "uf"
]:
    print(f"\n===== {coluna} =====")
    print(
        df_limpo[coluna]
        .value_counts(dropna=False)
        .to_string()
    )

# COMMAND ----------

print("DataFrame original df:", "df" in globals())
print("DataFrame tratado df_limpo:", "df_limpo" in globals())

# COMMAND ----------

colunas_numericas = [
    "renda_mensal",
    "valor_segurado",
    "franquia",
    "premio_anual",
    "valor_sinistro_num"
]

resumo_numerico = df_limpo[colunas_numericas].describe().T

display(
    resumo_numerico[
        ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    ].round(2)
)

# COMMAND ----------

colunas_numericas = [
    "renda_mensal",
    "valor_segurado",
    "franquia",
    "premio_anual",
    "valor_sinistro_num"
]

resultados_iqr = []

for coluna in colunas_numericas:
    dados = df_limpo[coluna].dropna()

    q1 = dados.quantile(0.25)
    q3 = dados.quantile(0.75)
    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    outliers = (
        (dados < limite_inferior) |
        (dados > limite_superior)
    )

    resultados_iqr.append({
        "variavel": coluna,
        "limite_inferior": round(limite_inferior, 2),
        "limite_superior": round(limite_superior, 2),
        "quantidade_outliers": int(outliers.sum()),
        "percentual_outliers": round(outliers.mean() * 100, 2)
    })

display(pd.DataFrame(resultados_iqr))

# COMMAND ----------

import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 2, figsize=(14, 12))

for ax, coluna in zip(axes.flatten(), colunas_numericas):
    ax.boxplot(
        df_limpo[coluna].dropna(),
        vert=False
    )
    ax.set_title(coluna)
    ax.set_xlabel("Valor")

axes.flatten()[-1].axis("off")

plt.suptitle(
    "Distribuição e valores extremos das variáveis financeiras",
    fontsize=14
)

plt.tight_layout()
plt.show()

# COMMAND ----------

# Selecionar as variáveis financeiras que estamos investigando
colunas_numericas = [
    "renda_mensal",
    "valor_segurado",
    "franquia",
    "premio_anual",
    "valor_sinistro_num"
]

# Calcular a assimetria de cada variável
resumo_assimetria = pd.DataFrame({
    "variavel": colunas_numericas,
    "assimetria": [
        df_limpo[coluna].skew()
        for coluna in colunas_numericas
    ]
})

# Ordenar da maior para a menor assimetria
resumo_assimetria = resumo_assimetria.sort_values(
    by="assimetria",
    ascending=False
)

# Exibir os resultados
display(resumo_assimetria.round(3))

# COMMAND ----------

import numpy as np
import matplotlib.pyplot as plt

# Selecionar as duas variáveis com maior assimetria
variaveis_teste = [
    "renda_mensal",
    "valor_segurado"
]

# Criar gráficos para comparar os dados originais e transformados
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

for linha, coluna in enumerate(variaveis_teste):

    # Remover valores ausentes apenas para construir os gráficos
    dados = df_limpo[coluna].dropna()

    # Gerar a distribuição dos valores originais
    axes[linha, 0].hist(dados, bins=40)
    axes[linha, 0].set_title(f"{coluna} - Original")
    axes[linha, 0].set_xlabel("Valor")
    axes[linha, 0].set_ylabel("Frequência")

    # Aplicar log1p para comprimir valores elevados
    dados_log = np.log1p(dados)

    # Gerar a distribuição dos valores transformados
    axes[linha, 1].hist(dados_log, bins=40)
    axes[linha, 1].set_title(f"{coluna} - Transformação log1p")
    axes[linha, 1].set_xlabel("log(1 + valor)")
    axes[linha, 1].set_ylabel("Frequência")

# Ajustar o espaçamento dos gráficos
plt.tight_layout()
plt.show()

# COMMAND ----------

# Comparar a assimetria original com a assimetria após log1p

import numpy as np
import pandas as pd

# Definir as variáveis que apresentaram maior assimetria
variaveis_teste = [
    "renda_mensal",
    "valor_segurado"
]

# Criar uma lista para armazenar os resultados
resultados = []

# Calcular a assimetria de cada variável
for coluna in variaveis_teste:

    # Selecionar os valores não ausentes
    dados_originais = df_limpo[coluna].dropna()

    # Aplicar a transformação logarítmica sem alterar o DataFrame original
    dados_transformados = np.log1p(dados_originais)

    # Registrar a assimetria antes e depois da transformação
    resultados.append({
        "Variável": coluna,
        "Assimetria original": dados_originais.skew(),
        "Assimetria após log1p": dados_transformados.skew()
    })

# Exibir os resultados em uma tabela
tabela_assimetria = pd.DataFrame(resultados)

display(tabela_assimetria.round(3))

# COMMAND ----------

# Comparar a assimetria original e transformada das demais variáveis financeiras

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Selecionar as variáveis financeiras ainda não avaliadas
variaveis_teste = [
    "franquia",
    "premio_anual",
    "valor_sinistro_num"
]

# Criar uma lista para armazenar os resultados
resultados = []

# Calcular a assimetria original e após log1p
for coluna in variaveis_teste:

    # Selecionar os valores não ausentes
    dados_originais = df_limpo[coluna].dropna()

    # Aplicar log1p sem modificar o DataFrame original
    dados_log = np.log1p(dados_originais)

    # Armazenar as métricas calculadas
    resultados.append({
        "Variável": coluna,
        "Assimetria original": dados_originais.skew(),
        "Assimetria após log1p": dados_log.skew()
    })

# Organizar os resultados em uma tabela
tabela_comparacao = pd.DataFrame(resultados)

# Exibir a tabela com três casas decimais
display(tabela_comparacao.round(3))

# Criar gráficos para visualizar as distribuições transformadas
fig, axes = plt.subplots(1, 3, figsize=(16, 4))

for eixo, coluna in zip(axes, variaveis_teste):

    # Aplicar log1p aos valores válidos
    dados_log = np.log1p(df_limpo[coluna].dropna())

    # Construir o histograma da variável transformada
    eixo.hist(dados_log, bins=35)

    # Identificar o gráfico
    eixo.set_title(f"{coluna} após log1p")
    eixo.set_xlabel("log(1 + valor)")
    eixo.set_ylabel("Frequência")

# Ajustar o espaçamento dos gráficos
plt.tight_layout()
plt.show()

# COMMAND ----------

# DBTITLE 1,Instalar seaborn
# MAGIC %pip install seaborn

# COMMAND ----------

# Comparar o valor dos sinistros entre casos fraudulentos e não fraudulentos
# Comparar os valores dos sinistros entre casos fraudulentos e não fraudulentos

import pandas as pd
import matplotlib.pyplot as plt

# Criar uma cópia temporária com as colunas necessárias
dados_analise = df_limpo[["valor_sinistro_num", "fraude"]].copy()

# Remover registros com valores ausentes nas colunas analisadas
dados_analise = dados_analise.dropna()

# Calcular estatísticas descritivas por classe de fraude
tabela_sinistros = (
    dados_analise
    .groupby("fraude")["valor_sinistro_num"]
    .agg(
        quantidade="count",
        media="mean",
        mediana="median",
        minimo="min",
        maximo="max"
    )
    .round(2)
)

# Exibir a tabela comparativa
display(tabela_sinistros)

# Separar os valores dos sinistros por classe
valores_sem_fraude = dados_analise.loc[
    dados_analise["fraude"] == 0, "valor_sinistro_num"
]

valores_com_fraude = dados_analise.loc[
    dados_analise["fraude"] == 1, "valor_sinistro_num"
]

# Criar o gráfico de caixas usando matplotlib
plt.figure(figsize=(10, 5))

plt.boxplot(
    [valores_sem_fraude, valores_com_fraude],
    tick_labels=["Não fraudulento (0)", "Fraudulento (1)"],
    showfliers=False
)

# Adicionar título e identificação dos eixos
plt.title("Valor do sinistro por ocorrência de fraude")
plt.xlabel("Classificação do sinistro")
plt.ylabel("Valor do sinistro (R$)")

# Ajustar o layout e exibir o gráfico
plt.tight_layout()
plt.show()

# COMMAND ----------

# Analisar a taxa de fraude em cinco faixas de valor do sinistro

import pandas as pd
import matplotlib.pyplot as plt

# Criar uma cópia temporária das colunas necessárias
dados_faixas = df_limpo[
    ["valor_sinistro_num", "fraude"]
].copy()

# Remover registros com valores ausentes
dados_faixas = dados_faixas.dropna()

# Dividir os sinistros em cinco grupos de tamanho semelhante
dados_faixas["faixa_quintil"] = pd.qcut(
    dados_faixas["valor_sinistro_num"],
    q=5,
    labels=["Q1 - Menores", "Q2", "Q3", "Q4", "Q5 - Maiores"]
)

# Calcular quantidade de registros, fraudes e taxa de fraude por grupo
tabela_quintis = (
    dados_faixas
    .groupby("faixa_quintil", observed=False)
    .agg(
        quantidade=("fraude", "count"),
        total_fraudes=("fraude", "sum"),
        taxa_fraude=("fraude", "mean")
    )
    .reset_index()
)

# Converter a taxa de fraude para percentual
tabela_quintis["taxa_fraude"] = (
    tabela_quintis["taxa_fraude"] * 100
)

# Exibir a tabela de resultados
display(tabela_quintis.round(2))

# Criar gráfico da taxa de fraude por quintil
plt.figure(figsize=(10, 5))

plt.bar(
    tabela_quintis["faixa_quintil"].astype(str),
    tabela_quintis["taxa_fraude"]
)

# Identificar título e eixos
plt.title("Taxa de fraude por faixa de valor do sinistro")
plt.xlabel("Faixa de valor do sinistro")
plt.ylabel("Taxa de fraude (%)")

# Exibir os percentuais sobre as barras
for indice, valor in enumerate(tabela_quintis["taxa_fraude"]):
    plt.text(indice, valor, f"{valor:.2f}%", ha="center", va="bottom")

# Ajustar e exibir o gráfico
plt.tight_layout()
plt.show()

# COMMAND ----------

# Analisar a taxa de fraude conforme a quantidade de sinistros nos últimos 12 meses

import pandas as pd
import matplotlib.pyplot as plt

# Criar uma cópia temporária das variáveis necessárias
dados_frequencia = df_limpo[
    ["qtd_sinistros_12m", "fraude"]
].copy()

# Remover registros com valores ausentes
dados_frequencia = dados_frequencia.dropna()

# Agrupar os registros pela quantidade de sinistros recentes
tabela_frequencia = (
    dados_frequencia
    .groupby("qtd_sinistros_12m")
    .agg(
        quantidade=("fraude", "count"),
        total_fraudes=("fraude", "sum"),
        taxa_fraude=("fraude", "mean")
    )
    .reset_index()
)

# Converter a taxa de fraude para percentual
tabela_frequencia["taxa_fraude"] = (
    tabela_frequencia["taxa_fraude"] * 100
)

# Exibir a tabela de resultados
display(tabela_frequencia.round(2))

# Criar gráfico da taxa de fraude por quantidade de sinistros
plt.figure(figsize=(9, 5))

plt.bar(
    tabela_frequencia["qtd_sinistros_12m"].astype(str),
    tabela_frequencia["taxa_fraude"]
)

# Identificar título e eixos
plt.title("Taxa de fraude por quantidade de sinistros nos últimos 12 meses")
plt.xlabel("Quantidade de sinistros")
plt.ylabel("Taxa de fraude (%)")

# Exibir os percentuais sobre as barras
for indice, valor in enumerate(tabela_frequencia["taxa_fraude"]):
    plt.text(indice, valor, f"{valor:.2f}%", ha="center", va="bottom")

# Ajustar e exibir o gráfico
plt.tight_layout()
plt.show()

# COMMAND ----------

# Analisar a taxa de fraude conforme as alterações recentes na apólice

import pandas as pd
import matplotlib.pyplot as plt

# Criar uma cópia temporária das colunas necessárias
dados_alteracoes = df_limpo[
    ["alteracoes_apolice_90d", "fraude"]
].copy()

# Remover registros com valores ausentes
dados_alteracoes = dados_alteracoes.dropna()

# Agrupar os registros pela quantidade de alterações na apólice
tabela_alteracoes = (
    dados_alteracoes
    .groupby("alteracoes_apolice_90d")
    .agg(
        quantidade=("fraude", "count"),
        total_fraudes=("fraude", "sum"),
        taxa_fraude=("fraude", "mean")
    )
    .reset_index()
)

# Converter a taxa de fraude para percentual
tabela_alteracoes["taxa_fraude"] = (
    tabela_alteracoes["taxa_fraude"] * 100
)

# Exibir a tabela de resultados
display(tabela_alteracoes.round(2))

# Criar gráfico da taxa de fraude por quantidade de alterações
plt.figure(figsize=(9, 5))

plt.bar(
    tabela_alteracoes["alteracoes_apolice_90d"].astype(str),
    tabela_alteracoes["taxa_fraude"]
)

# Identificar título e eixos
plt.title("Taxa de fraude por alterações na apólice nos últimos 90 dias")
plt.xlabel("Quantidade de alterações")
plt.ylabel("Taxa de fraude (%)")

# Exibir os percentuais sobre as barras
for indice, valor in enumerate(tabela_alteracoes["taxa_fraude"]):
    plt.text(indice, valor, f"{valor:.2f}%", ha="center", va="bottom")

# Ajustar o layout e exibir o gráfico
plt.tight_layout()
plt.show()

# COMMAND ----------

# Analisar a taxa de fraude por faixa de score de crédito

import pandas as pd
import matplotlib.pyplot as plt

# Criar uma cópia temporária das colunas necessárias
dados_score = df_limpo[
    ["score_credito", "fraude"]
].copy()

# Remover registros sem score para analisar somente os valores disponíveis
dados_score = dados_score.dropna(subset=["score_credito"])

# Dividir os scores em cinco grupos com quantidades semelhantes
dados_score["faixa_score"] = pd.qcut(
    dados_score["score_credito"],
    q=5,
    labels=[
        "Q1 - Menores scores",
        "Q2",
        "Q3",
        "Q4",
        "Q5 - Maiores scores"
    ]
)

# Calcular quantidade de registros, fraudes e taxa de fraude
tabela_score = (
    dados_score
    .groupby("faixa_score", observed=False)
    .agg(
        quantidade=("fraude", "count"),
        total_fraudes=("fraude", "sum"),
        taxa_fraude=("fraude", "mean")
    )
    .reset_index()
)

# Converter a taxa de fraude para percentual
tabela_score["taxa_fraude"] = (
    tabela_score["taxa_fraude"] * 100
)

# Exibir a tabela comparativa
display(tabela_score.round(2))

# Criar gráfico da taxa de fraude por faixa de score
plt.figure(figsize=(11, 5))

plt.bar(
    tabela_score["faixa_score"].astype(str),
    tabela_score["taxa_fraude"]
)

# Identificar título e eixos
plt.title("Taxa de fraude por faixa de score de crédito")
plt.xlabel("Faixa de score")
plt.ylabel("Taxa de fraude (%)")

# Exibir os percentuais sobre as barras
for indice, valor in enumerate(tabela_score["taxa_fraude"]):
    plt.text(indice, valor, f"{valor:.2f}%", ha="center", va="bottom")

# Ajustar o layout e exibir o gráfico
plt.tight_layout()
plt.show()

# COMMAND ----------

# Avaliar a taxa de fraude em registros com e sem score de crédito

import pandas as pd
import matplotlib.pyplot as plt

# Criar uma cópia temporária das colunas necessárias
dados_ausencia_score = df_limpo[
    ["score_credito", "fraude"]
].copy()

# Criar uma classificação para identificar a presença ou ausência do score
dados_ausencia_score["situacao_score"] = (
    dados_ausencia_score["score_credito"]
    .isna()
    .map({
        True: "Score ausente",
        False: "Score informado"
    })
)

# Calcular quantidade de registros, fraudes e taxa de fraude
tabela_ausencia_score = (
    dados_ausencia_score
    .groupby("situacao_score")
    .agg(
        quantidade=("fraude", "count"),
        total_fraudes=("fraude", "sum"),
        taxa_fraude=("fraude", "mean")
    )
    .reset_index()
)

# Converter a taxa de fraude para percentual
tabela_ausencia_score["taxa_fraude"] = (
    tabela_ausencia_score["taxa_fraude"] * 100
)

# Exibir a tabela comparativa
display(tabela_ausencia_score.round(2))

# Criar gráfico da taxa de fraude por situação do score
plt.figure(figsize=(8, 5))

plt.bar(
    tabela_ausencia_score["situacao_score"],
    tabela_ausencia_score["taxa_fraude"]
)

# Identificar título e eixos
plt.title("Taxa de fraude conforme disponibilidade do score")
plt.xlabel("Situação do score de crédito")
plt.ylabel("Taxa de fraude (%)")

# Exibir os percentuais sobre as barras
for indice, valor in enumerate(tabela_ausencia_score["taxa_fraude"]):
    plt.text(indice, valor, f"{valor:.2f}%", ha="center", va="bottom")

# Ajustar o layout e exibir o gráfico
plt.tight_layout()
plt.show()

# COMMAND ----------

# Avaliar a taxa de fraude conforme a ausência de informações
# nas variáveis renda_mensal e qtd_testemunhas

import pandas as pd
import matplotlib.pyplot as plt

# Definir as variáveis que serão analisadas
variaveis_ausentes = [
    "renda_mensal",
    "qtd_testemunhas"
]

# Criar uma lista para armazenar os resultados
resultados_ausencia = []

# Analisar cada variável separadamente
for coluna in variaveis_ausentes:

    # Criar uma cópia temporária com a variável e o alvo
    dados = df_limpo[[coluna, "fraude"]].copy()

    # Identificar se a informação está ausente ou preenchida
    dados["situacao"] = dados[coluna].isna().map({
        True: "Ausente",
        False: "Informado"
    })

    # Agrupar os registros pela situação da informação
    resumo = (
        dados
        .groupby("situacao")
        .agg(
            quantidade=("fraude", "count"),
            total_fraudes=("fraude", "sum"),
            taxa_fraude=("fraude", "mean")
        )
        .reset_index()
    )

    # Adicionar o nome da variável aos resultados
    resumo["variavel"] = coluna

    # Armazenar os resultados
    resultados_ausencia.append(resumo)

# Consolidar os resultados em uma única tabela
tabela_ausencia = pd.concat(
    resultados_ausencia,
    ignore_index=True
)

# Converter a taxa de fraude para percentual
tabela_ausencia["taxa_fraude"] *= 100

# Exibir a tabela comparativa
display(
    tabela_ausencia[
        ["variavel", "situacao", "quantidade",
         "total_fraudes", "taxa_fraude"]
    ].round(2)
)

# Criar gráficos separados para cada variável
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for eixo, coluna in zip(axes, variaveis_ausentes):

    # Selecionar os resultados da variável atual
    dados_grafico = tabela_ausencia[
        tabela_ausencia["variavel"] == coluna
    ]

    # Construir o gráfico de barras
    eixo.bar(
        dados_grafico["situacao"],
        dados_grafico["taxa_fraude"]
    )

    # Identificar título e eixos
    eixo.set_title(f"Taxa de fraude: {coluna}")
    eixo.set_xlabel("Disponibilidade da informação")
    eixo.set_ylabel("Taxa de fraude (%)")

    # Exibir os percentuais sobre as barras
    for indice, valor in enumerate(dados_grafico["taxa_fraude"]):
        eixo.text(
            indice,
            valor,
            f"{valor:.2f}%",
            ha="center",
            va="bottom"
        )

# Ajustar o espaçamento dos gráficos
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Relatório de Análise Exploratória de Dados (EDA)
# MAGIC ## Projeto: Prevenção de Fraudes em Sinistros de Seguros
# MAGIC
# MAGIC **Ambiente:** Databricks Free Edition  
# MAGIC **Base analisada:** `sinistros_raw.csv`  
# MAGIC **Data de referência:** novembro de 2026  
# MAGIC **Etapa:** Análise Exploratória de Dados — concluída
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 1. Objetivo da análise
# MAGIC
# MAGIC A Análise Exploratória de Dados teve como objetivo compreender a estrutura, a qualidade e o comportamento das informações presentes na base de sinistros, identificando padrões associados à ocorrência de fraudes.
# MAGIC
# MAGIC Foram investigados:
# MAGIC
# MAGIC - Integridade e duplicidade dos registros;
# MAGIC - Valores ausentes e inconsistências;
# MAGIC - Padronização de variáveis categóricas;
# MAGIC - Distribuição das variáveis numéricas;
# MAGIC - Identificação de valores extremos;
# MAGIC - Assimetria das distribuições;
# MAGIC - Relações entre as variáveis explicativas e a variável-alvo `fraude`.
# MAGIC
# MAGIC O objetivo foi produzir uma base mais consistente e reunir evidências que orientem a preparação dos dados e a construção dos modelos de Machine Learning.
# MAGIC
# MAGIC ## 2. Caracterização da base
# MAGIC
# MAGIC A base original apresentava:
# MAGIC
# MAGIC | Indicador | Resultado |
# MAGIC |---|---:|
# MAGIC | Registros originais | 20.300 |
# MAGIC | Colunas originais | 30 |
# MAGIC | Registros duplicados identificados | 300 |
# MAGIC | Registros após deduplicação | 20.000 |
# MAGIC | Colunas no DataFrame de trabalho após análises derivadas | 33 |
# MAGIC
# MAGIC Os 300 registros duplicados foram identificados considerando o identificador `id_sinistro`. Não foram observadas informações conflitantes entre os registros duplicados analisados.
# MAGIC
# MAGIC Após a deduplicação, a base de trabalho passou a conter 20.000 registros.
# MAGIC
# MAGIC ### 2.1 Distribuição da variável-alvo
# MAGIC
# MAGIC | Classificação | Quantidade | Percentual |
# MAGIC |---|---:|---:|
# MAGIC | Não fraudulento (0) | 18.648 | 93,24% |
# MAGIC | Fraudulento (1) | 1.352 | 6,76% |
# MAGIC | **Total** | **20.000** | **100%** |
# MAGIC
# MAGIC A base apresenta desequilíbrio entre as classes, com aproximadamente 6,76% de registros fraudulentos.
# MAGIC
# MAGIC Essa característica deverá ser considerada na modelagem, especialmente na escolha das métricas de avaliação e das estratégias de classificação.
# MAGIC
# MAGIC ## 3. Limpeza e tratamento dos dados
# MAGIC
# MAGIC ### 3.1 Remoção de duplicidades
# MAGIC
# MAGIC Foram removidos 300 registros duplicados, utilizando `id_sinistro` como referência.
# MAGIC
# MAGIC A operação foi realizada sobre uma cópia de trabalho, preservando o DataFrame original.
# MAGIC
# MAGIC ### 3.2 Tratamento de valores inválidos
# MAGIC
# MAGIC Foram identificadas inconsistências nas variáveis `idade` e `tempo_cliente_anos`.
# MAGIC
# MAGIC | Variável | Inconsistência identificada | Quantidade |
# MAGIC |---|---|---:|
# MAGIC | Idade | Valores -1 | 18 |
# MAGIC | Idade | Valores 0 | 20 |
# MAGIC | Idade | Valores 150 | 19 |
# MAGIC | Idade | Valores 999 | 24 |
# MAGIC | Tempo de relacionamento | Valores -1 | 75 |
# MAGIC
# MAGIC Os valores de idade fora do intervalo adotado de 18 a 100 anos foram convertidos para ausentes.
# MAGIC
# MAGIC Os valores negativos de tempo de relacionamento também foram convertidos para ausentes.
# MAGIC
# MAGIC Nenhum registro foi excluído por essas inconsistências.
# MAGIC
# MAGIC ### 3.3 Padronização das variáveis categóricas
# MAGIC
# MAGIC Foram identificadas variações de escrita, capitalização e acentuação em algumas categorias.
# MAGIC
# MAGIC As seguintes variáveis foram padronizadas:
# MAGIC
# MAGIC - `tipo_cobertura`;
# MAGIC - `boletim_ocorrencia`;
# MAGIC - `uf`.
# MAGIC
# MAGIC Após o tratamento, as categorias de cobertura passaram a apresentar quatro grupos:
# MAGIC
# MAGIC | Tipo de cobertura | Quantidade |
# MAGIC |---|---:|
# MAGIC | Compreensiva | 8.963 |
# MAGIC | Roubo e furto | 4.080 |
# MAGIC | Colisão | 4.027 |
# MAGIC | Básica | 2.930 |
# MAGIC
# MAGIC A variável `boletim_ocorrencia` passou a apresentar duas categorias:
# MAGIC
# MAGIC | Categoria | Quantidade |
# MAGIC |---|---:|
# MAGIC | Sim | 16.416 |
# MAGIC | Não | 3.584 |
# MAGIC
# MAGIC A variável `uf` foi normalizada para as oito unidades federativas representadas na base:
# MAGIC
# MAGIC | UF | Quantidade |
# MAGIC |---|---:|
# MAGIC | SP | 6.019 |
# MAGIC | RJ | 3.091 |
# MAGIC | MG | 2.388 |
# MAGIC | BA | 1.953 |
# MAGIC | PR | 1.841 |
# MAGIC | PE | 1.578 |
# MAGIC | SC | 1.572 |
# MAGIC | RS | 1.558 |
# MAGIC
# MAGIC Esses procedimentos reduziram a fragmentação das categorias e melhoraram a consistência das informações.
# MAGIC
# MAGIC ## 4. Análise de valores ausentes
# MAGIC
# MAGIC Após a limpeza, foram identificados valores ausentes nas seguintes variáveis:
# MAGIC
# MAGIC | Variável | Ausentes | Percentual |
# MAGIC |---|---:|---:|
# MAGIC | `qtd_testemunhas` | 2.414 | 12,07% |
# MAGIC | `renda_mensal` | 1.932 | 9,66% |
# MAGIC | `score_credito` | 1.618 | 8,09% |
# MAGIC | `oficina_credenciada` | 1.181 | 5,90% |
# MAGIC | `estado_civil` | 595 | 2,97% |
# MAGIC | `canal_venda` | 374 | 1,87% |
# MAGIC | `idade` | 81 | 0,40% |
# MAGIC | `tempo_cliente_anos` | 75 | 0,38% |
# MAGIC
# MAGIC Não foram removidos registros por apresentarem valores ausentes.
# MAGIC
# MAGIC ### 4.1 Ausência de score de crédito
# MAGIC
# MAGIC | Situação | Registros | Fraudes | Taxa de fraude |
# MAGIC |---|---:|---:|---:|
# MAGIC | Score ausente | 1.618 | 128 | 7,91% |
# MAGIC | Score informado | 18.382 | 1.224 | 6,66% |
# MAGIC
# MAGIC A taxa de fraude foi 1,25 ponto percentual maior entre os registros sem score.
# MAGIC
# MAGIC O resultado sugere que a ausência dessa informação pode conter algum sinal associado à variável-alvo.
# MAGIC
# MAGIC ### 4.2 Ausência de renda mensal
# MAGIC
# MAGIC | Situação | Registros | Fraudes | Taxa de fraude |
# MAGIC |---|---:|---:|---:|
# MAGIC | Renda ausente | 1.932 | 144 | 7,45% |
# MAGIC | Renda informada | 18.068 | 1.208 | 6,69% |
# MAGIC
# MAGIC Foi observada uma diferença de 0,76 ponto percentual entre os grupos.
# MAGIC
# MAGIC Essa diferença é moderada e poderá ser avaliada durante a modelagem.
# MAGIC
# MAGIC ### 4.3 Ausência da quantidade de testemunhas
# MAGIC
# MAGIC | Situação | Registros | Fraudes | Taxa de fraude |
# MAGIC |---|---:|---:|---:|
# MAGIC | Quantidade ausente | 2.414 | 162 | 6,71% |
# MAGIC | Quantidade informada | 17.586 | 1.190 | 6,77% |
# MAGIC
# MAGIC As taxas são praticamente iguais. Portanto, não foi identificada uma diferença relevante entre os grupos nessa análise descritiva.
# MAGIC
# MAGIC **Conclusão sobre os valores ausentes:** os registros foram preservados. O tratamento deverá ocorrer na preparação para Machine Learning, com imputação ajustada exclusivamente nos dados de treinamento. A criação de indicadores de ausência será avaliada de forma seletiva, e não aplicada indiscriminadamente.
# MAGIC
# MAGIC ## 5. Análise estatística das variáveis numéricas
# MAGIC
# MAGIC Foram analisadas as principais variáveis financeiras:
# MAGIC
# MAGIC | Variável | Média | Mediana | Desvio-padrão | Mínimo | Máximo |
# MAGIC |---|---:|---:|---:|---:|---:|
# MAGIC | `renda_mensal` | R$ 6.486,34 | R$ 4.875,04 | R$ 

# COMMAND ----------

# AUDITORIA 1: Verificar a estrutura e a qualidade geral do DataFrame

import pandas as pd

# Trabalhar somente com o DataFrame tratado, sem modificar seus dados
base_auditoria = df_limpo.copy()

# Criar um resumo da estrutura e dos tipos de dados
resumo_estrutura = pd.DataFrame({
    "coluna": base_auditoria.columns,
    "tipo_dado": base_auditoria.dtypes.astype(str).values,
    "valores_preenchidos": base_auditoria.notna().sum().values,
    "valores_ausentes": base_auditoria.isna().sum().values,
    "percentual_ausente": (
        base_auditoria.isna().mean().values * 100
    ).round(2),
    "valores_distintos": base_auditoria.nunique(dropna=True).values
})

# Ordenar as colunas pelo percentual de valores ausentes
resumo_estrutura = resumo_estrutura.sort_values(
    by="percentual_ausente",
    ascending=False
)

# Exibir o relatório de estrutura e valores ausentes
display(resumo_estrutura)

# Verificar duplicidades de registros completos
duplicados_completos = base_auditoria.duplicated().sum()

# Verificar duplicidades do identificador dos sinistros
duplicados_id = base_auditoria["id_sinistro"].duplicated().sum()

# Verificar quantidade de identificadores ausentes
ids_ausentes = base_auditoria["id_sinistro"].isna().sum()

# Verificar os valores existentes na variável-alvo
valores_fraude = sorted(
    base_auditoria["fraude"].dropna().unique().tolist()
)

# Consolidar os indicadores gerais
indicadores_gerais = pd.DataFrame({
    "indicador": [
        "Quantidade de registros",
        "Quantidade de colunas",
        "Registros completos duplicados",
        "Identificadores de sinistro duplicados",
        "Identificadores de sinistro ausentes",
        "Valores distintos encontrados em fraude"
    ],
    "resultado": [
        len(base_auditoria),
        len(base_auditoria.columns),
        duplicados_completos,
        duplicados_id,
        ids_ausentes,
        str(valores_fraude)
    ]
})

# Exibir os indicadores gerais da auditoria
display(indicadores_gerais)

# COMMAND ----------

# AUDITORIA 2: Verificar inconsistências nas colunas categóricas

import pandas as pd

# Criar uma cópia para garantir que os dados originais não sejam alterados
base_auditoria = df_limpo.copy()

# Selecionar colunas de texto, excluindo identificadores e datas
colunas_texto = [
    coluna for coluna in base_auditoria.select_dtypes(
        include=["object", "string"]
    ).columns
    if not coluna.startswith("id_")
    and not coluna.startswith("data_")
    and coluna != "valor_sinistro"
]

# Criar uma lista para armazenar os resultados
resultados_texto = []

# Analisar cada coluna textual
for coluna in colunas_texto:

    # Converter os valores para texto, preservando os ausentes
    valores = base_auditoria[coluna].dropna().astype("string")

    # Verificar valores com espaços no início ou no final
    com_espacos = (valores != valores.str.strip()).sum()

    # Verificar quantidade de categorias antes e depois de padronizar
    categorias_originais = valores.nunique()

    categorias_padronizadas = (
        valores.str.strip()
        .str.casefold()
        .nunique()
    )

    # Registrar os indicadores da coluna
    resultados_texto.append({
        "coluna": coluna,
        "categorias_originais": categorias_originais,
        "categorias_apos_padronizacao": categorias_padronizadas,
        "valores_com_espacos": int(com_espacos)
    })

# Organizar os resultados em uma tabela
relatorio_texto = pd.DataFrame(resultados_texto)

# Exibir o relatório de inconsistências textuais
display(
    relatorio_texto.sort_values(
        by="categorias_originais",
        ascending=False
    )
)

# COMMAND ----------

# AUDITORIA 3: Inspecionar os valores das categorias

# Criar uma cópia para preservar o DataFrame tratado
base_auditoria = df_limpo.copy()

# Definir as colunas categóricas que precisam de inspeção
colunas_categoricas = [
    "uf",
    "tipo_sinistro",
    "estado_civil",
    "tipo_cobertura",
    "canal_venda",
    "status_investigacao",
    "boletim_ocorrencia",
    "houve_vitima",
    "oficina_credenciada",
    "pais"
]

# Exibir os valores distintos de cada coluna
for coluna in colunas_categoricas:

    print(f"\nColuna: {coluna}")

    # Mostrar as categorias encontradas e suas frequências
    display(
        base_auditoria[coluna]
        .value_counts(dropna=False)
        .rename_axis("categoria")
        .reset_index(name="quantidade")
    )

# Verificar se UF e UF normalizada são exatamente iguais
print("\nComparação entre uf e uf_normalizada:")

print(
    "Quantidade de divergências:",
    (
        base_auditoria["uf"].astype("string")
        != base_auditoria["uf_normalizada"].astype("string")
    ).sum()
)

# COMMAND ----------

# AUDITORIA 4: Verificar consistência numérica e temporal

import pandas as pd

# Criar uma cópia para preservar o DataFrame tratado
base_auditoria = df_limpo.copy()

# Colunas numéricas que serão verificadas
colunas_numericas = [
    "idade",
    "tempo_cliente_anos",
    "score_credito",
    "renda_mensal",
    "valor_segurado",
    "franquia",
    "premio_anual",
    "alteracoes_apolice_90d",
    "qtd_sinistros_12m",
    "qtd_sinistros_total",
    "hora_sinistro",
    "qtd_testemunhas",
    "valor_sinistro_num",
    "valor_recuperado"
]

# Criar relatório com estatísticas e possíveis valores negativos
relatorio_numerico = []

for coluna in colunas_numericas:

    valores = base_auditoria[coluna]

    relatorio_numerico.append({
        "coluna": coluna,
        "minimo": valores.min(),
        "maximo": valores.max(),
        "quantidade_negativos": (valores < 0).sum(),
        "quantidade_zeros": (valores == 0).sum(),
        "valores_ausentes": valores.isna().sum()
    })

# Exibir o relatório numérico
display(pd.DataFrame(relatorio_numerico))

# Converter as colunas de datas para o formato datetime
colunas_datas = [
    "data_inicio_apolice",
    "data_sinistro",
    "data_aviso"
]

datas = pd.DataFrame()

for coluna in colunas_datas:

    datas[coluna] = pd.to_datetime(
        base_auditoria[coluna],
        errors="coerce"
    )

# Verificar datas que não puderam ser interpretadas
relatorio_datas = pd.DataFrame({
    "coluna": colunas_datas,
    "datas_invalidas": [
        datas[coluna].isna().sum()
        for coluna in colunas_datas
    ]
})

print("Verificação de datas:")
display(relatorio_datas)

# Verificar a ordem cronológica dos acontecimentos
print("Verificação da sequência temporal:")

print(
    "Sinistros anteriores ao início da apólice:",
    (
        datas["data_sinistro"] < datas["data_inicio_apolice"]
    ).sum()
)

print(
    "Avisos anteriores à data do sinistro:",
    (
        datas["data_aviso"] < datas["data_sinistro"]
    ).sum()
)

# COMMAND ----------



# COMMAND ----------

# AUDITORIA 5: Investigar o formato original das datas

# Criar uma cópia para preservar os dados
base_auditoria = df_limpo.copy()

# Colunas de datas que serão investigadas
colunas_datas = [
    "data_inicio_apolice",
    "data_sinistro",
    "data_aviso"
]

for coluna in colunas_datas:

    print(f"\nColuna: {coluna}")

    # Mostrar exemplos dos valores originais
    print("Exemplos dos valores originais:")
    display(base_auditoria[coluna].dropna().head(10))

    # Comparar a interpretação nos dois formatos
    conversao_padrao = pd.to_datetime(
        base_auditoria[coluna],
        errors="coerce"
    )

    conversao_brasileira = pd.to_datetime(
        base_auditoria[coluna],
        errors="coerce",
        dayfirst=True
    )

    # Exibir a quantidade de datas não interpretadas em cada tentativa
    print("Datas não interpretadas no formato padrão:",
          conversao_padrao.isna().sum())

    print("Datas não interpretadas com dayfirst=True:",
          conversao_brasileira.isna().sum())

# COMMAND ----------

# AUDITORIA 6: Testar a conversão de datas em formatos mistos

import pandas as pd

# Criar uma cópia para não modificar o DataFrame tratado
base_teste = df_limpo.copy()

# Definir as colunas de datas
colunas_datas = [
    "data_inicio_apolice",
    "data_sinistro",
    "data_aviso"
]

# Percorrer cada coluna de data
for coluna in colunas_datas:

    # Converter os valores para texto, preservando os ausentes
    valores = base_teste[coluna].astype("string").str.strip()

    # Identificar datas no formato ISO: AAAA-MM-DD
    formato_iso = valores.str.match(
        r"^\d{4}-\d{2}-\d{2}$",
        na=False
    )

    # Identificar datas no formato brasileiro: DD/MM/AAAA
    formato_br = valores.str.match(
        r"^\d{2}/\d{2}/\d{4}$",
        na=False
    )

    # Criar uma coluna temporária para armazenar as datas convertidas
    datas_convertidas = pd.Series(
        pd.NaT,
        index=base_teste.index,
        dtype="datetime64[ns]"
    )

    # Converter os registros no formato ISO
    datas_convertidas.loc[formato_iso] = pd.to_datetime(
        valores.loc[formato_iso],
        format="%Y-%m-%d",
        errors="coerce"
    )

    # Converter os registros no formato brasileiro
    datas_convertidas.loc[formato_br] = pd.to_datetime(
        valores.loc[formato_br],
        format="%d/%m/%Y",
        errors="coerce"
    )

    # Exibir o diagnóstico da conversão
    print(f"\nColuna: {coluna}")
    print("Registros no formato ISO:", formato_iso.sum())
    print("Registros no formato brasileiro:", formato_br.sum())
    print("Datas não interpretadas após o teste:",
          datas_convertidas.isna().sum())

# COMMAND ----------

# AUDITORIA 8: Verificar a consistência das variáveis numéricas

import pandas as pd

# Criar uma cópia para preservar o DataFrame tratado
base_auditoria = df_limpo.copy()

# Selecionar as variáveis numéricas
colunas_numericas = [
    "idade",
    "tempo_cliente_anos",
    "score_credito",
    "renda_mensal",
    "valor_segurado",
    "franquia",
    "premio_anual",
    "alteracoes_apolice_90d",
    "qtd_sinistros_12m",
    "qtd_sinistros_total",
    "hora_sinistro",
    "qtd_testemunhas",
    "valor_sinistro_num",
    "valor_recuperado"
]

# Criar uma lista para armazenar os resultados
resultados = []

# Analisar cada variável numérica
for coluna in colunas_numericas:

    valores = base_auditoria[coluna]

    # Calcular estatísticas e indicadores de qualidade
    resultados.append({
        "coluna": coluna,
        "tipo": str(valores.dtype),
        "ausentes": valores.isna().sum(),
        "negativos": (valores < 0).sum(),
        "zeros": (valores == 0).sum(),
        "mínimo": valores.min(),
        "mediana": valores.median(),
        "média": valores.mean(),
        "máximo": valores.max()
    })

# Organizar o relatório
relatorio_numerico = pd.DataFrame(resultados)

# Exibir os resultados com valores arredondados
display(
    relatorio_numerico.round(2)
)

# COMMAND ----------

# AUDITORIA 9: Investigar valores extremos e zeros relevantes

# Criar uma cópia para preservar o DataFrame tratado
base_auditoria = df_limpo.copy()

# Variáveis financeiras que precisam de investigação
colunas_financeiras = [
    "renda_mensal",
    "valor_segurado",
    "franquia",
    "premio_anual",
    "valor_sinistro_num"
]

# Exibir os dez maiores valores de cada variável
for coluna in colunas_financeiras:

    print(f"\nMaiores valores de {coluna}:")

    # Selecionar os dez maiores valores
    display(
        base_auditoria[coluna]
        .nlargest(10)
        .reset_index(drop=True)
    )

# Investigar registros com hora do sinistro igual a zero
print("\nQuantidade de sinistros registrados à meia-noite:")
print((base_auditoria["hora_sinistro"] == 0).sum())

# Investigar registros sem testemunhas
print("\nQuantidade de sinistros sem testemunhas:")
print((base_auditoria["qtd_testemunhas"] == 0).sum())

# Investigar valores recuperados maiores que o valor do sinistro
print("\nRecuperação superior ao valor do sinistro:")
print(
    (
        base_auditoria["valor_recuperado"]
        > base_auditoria["valor_sinistro_num"]
    ).sum()
)

# COMMAND ----------

# AUDITORIA 10: Verificar coerência entre valores financeiros

# Criar uma cópia para preservar os dados
base_auditoria = df_limpo.copy()

# Verificar relações financeiras entre as variáveis
inconsistencias = {
    "Franquia maior que valor segurado": (
        base_auditoria["franquia"]
        > base_auditoria["valor_segurado"]
    ).sum(),

    "Sinistro maior que valor segurado": (
        base_auditoria["valor_sinistro_num"]
        > base_auditoria["valor_segurado"]
    ).sum(),

    "Recuperação maior que sinistro": (
        base_auditoria["valor_recuperado"]
        > base_auditoria["valor_sinistro_num"]
    ).sum(),

    "Prêmio anual igual ou inferior a zero": (
        base_auditoria["premio_anual"] <= 0
    ).sum(),

    "Valor segurado igual ou inferior a zero": (
        base_auditoria["valor_segurado"] <= 0
    ).sum(),

    "Sinistro igual ou inferior a zero": (
        base_auditoria["valor_sinistro_num"] <= 0
    ).sum()
}

# Transformar os resultados em tabela
relatorio_financeiro = pd.DataFrame({
    "verificacao": inconsistencias.keys(),
    "quantidade": inconsistencias.values()
})

# Exibir o resultado
display(relatorio_financeiro)

# COMMAND ----------

# AUDITORIA 11: Verificar integridade dos identificadores e da variável-alvo

# Criar uma cópia para preservar os dados
base_auditoria = df_limpo.copy()

# Verificar os valores da variável-alvo
print("Distribuição da variável fraude:")
display(
    base_auditoria["fraude"]
    .value_counts(dropna=False)
    .rename_axis("fraude")
    .reset_index(name="quantidade")
)

# Verificar se a variável-alvo contém somente 0 e 1
print(
    "Valores diferentes de 0 e 1:",
    (~base_auditoria["fraude"].isin([0, 1])).sum()
)

# Verificar duplicidade dos identificadores
print(
    "IDs de sinistro duplicados:",
    base_auditoria["id_sinistro"].duplicated().sum()
)

print(
    "IDs de segurado ausentes:",
    base_auditoria["id_segurado"].isna().sum()
)

# Verificar se a contagem de sinistros nos últimos 12 meses
# supera a contagem histórica total
print(
    "Sinistros em 12 meses maiores que o total histórico:",
    (
        base_auditoria["qtd_sinistros_12m"]
        > base_auditoria["qtd_sinistros_total"]
    ).sum()
)

# Verificar se há mais sinistros no histórico do que nos últimos 12 meses
print(
    "Registros em que o total histórico supera os últimos 12 meses:",
    (
        base_auditoria["qtd_sinistros_total"]
        > base_auditoria["qtd_sinistros_12m"]
    ).sum()
)

# COMMAND ----------

# AUDITORIA 12: Investigar a relação entre sinistros recentes e históricos

# Criar uma cópia para preservar os dados
base_auditoria = df_limpo.copy()

# Classificar a relação entre as duas variáveis
base_auditoria["relacao_sinistros"] = "Histórico maior"

# Identificar registros em que os valores são iguais
base_auditoria.loc[
    base_auditoria["qtd_sinistros_total"]
    == base_auditoria["qtd_sinistros_12m"],
    "relacao_sinistros"
] = "Valores iguais"

# Verificar a distribuição das relações
display(
    base_auditoria["relacao_sinistros"]
    .value_counts()
    .rename_axis("relacao")
    .reset_index(name="quantidade")
)

# Mostrar exemplos em que o histórico é maior
print("Exemplos de registros com histórico maior:")

display(
    base_auditoria.loc[
        base_auditoria["qtd_sinistros_total"]
        > base_auditoria["qtd_sinistros_12m"],
        [
            "id_segurado",
            "qtd_sinistros_12m",
            "qtd_sinistros_total"
        ]
    ].head(10)
)


# COMMAND ----------

# AUDITORIA 13: Inspecionar todas as categorias do conjunto de dados

# Criar uma cópia para preservar os dados tratados
base_auditoria = df_limpo.copy()

# Definir as colunas categóricas que serão verificadas
colunas_categoricas = [
    "uf",
    "tipo_sinistro",
    "estado_civil",
    "tipo_cobertura",
    "canal_venda",
    "status_investigacao",
    "boletim_ocorrencia",
    "houve_vitima",
    "oficina_credenciada",
    "pais"
]

# Exibir as categorias e suas respectivas frequências
for coluna in colunas_categoricas:

    print(f"\n{'=' * 50}")
    print(f"COLUNA: {coluna}")
    print(f"{'=' * 50}")

    # Contar os valores de cada categoria, incluindo ausentes
    frequencias = (
        base_auditoria[coluna]
        .value_counts(dropna=False)
        .rename_axis("categoria")
        .reset_index(name="quantidade")
    )

    # Calcular o percentual de cada categoria
    frequencias["percentual"] = (
        frequencias["quantidade"] / len(base_auditoria) * 100
    ).round(2)

    # Exibir a tabela de frequências
    display(frequencias)

# COMMAND ----------

# AUDITORIA 14: Validar a sequência cronológica das datas

# Criar uma cópia para preservar df_limpo
base_teste = df_limpo.copy()

# Converter as datas considerando os dois formatos identificados
for coluna in [
    "data_inicio_apolice",
    "data_sinistro",
    "data_aviso"
]:

    valores = base_teste[coluna].astype("string").str.strip()

    # Identificar os formatos ISO e brasileiro
    formato_iso = valores.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)
    formato_br = valores.str.match(r"^\d{2}/\d{2}/\d{4}$", na=False)

    # Criar uma coluna temporária para as datas convertidas
    convertida = pd.Series(
        pd.NaT,
        index=base_teste.index,
        dtype="datetime64[ns]"
    )

    # Converter cada formato separadamente
    convertida.loc[formato_iso] = pd.to_datetime(
        valores.loc[formato_iso],
        format="%Y-%m-%d",
        errors="coerce"
    )

    convertida.loc[formato_br] = pd.to_datetime(
        valores.loc[formato_br],
        format="%d/%m/%Y",
        errors="coerce"
    )

    base_teste[coluna + "_convertida"] = convertida

# Recuperar as datas convertidas
inicio = base_teste["data_inicio_apolice_convertida"]
sinistro = base_teste["data_sinistro_convertida"]
aviso = base_teste["data_aviso_convertida"]

# Verificar a ordem dos acontecimentos
print("Sinistro anterior ao início da apólice:", (sinistro < inicio).sum())
print("Aviso anterior ao sinistro:", (aviso < sinistro).sum())
print("Aviso na mesma data do sinistro:", (aviso == sinistro).sum())
print("Aviso posterior ao sinistro:", (aviso > sinistro).sum())

# COMMAND ----------

# Criamos uma cópia independente da base limpa, preservando os dados originais.
df_modelagem_base = df_limpo.copy()

# Importamos o pandas para trabalhar com as datas.
import pandas as pd

# Função para converter datas nos dois formatos encontrados na base:
# ISO: AAAA-MM-DD
# Brasileiro: DD/MM/AAAA
def converter_data_segura(valor):
    if pd.isna(valor):
        return pd.NaT

    valor = str(valor).strip()

    try:
        if len(valor) == 10 and valor[4] == "-":
            return pd.to_datetime(valor, format="%Y-%m-%d")

        if len(valor) == 10 and valor[2] == "/":
            return pd.to_datetime(valor, format="%d/%m/%Y")

        return pd.NaT

    except (ValueError, TypeError):
        return pd.NaT

# Convertemos as três colunas de datas na cópia de trabalho.
colunas_data = [
    "data_sinistro",
    "data_inicio_apolice",
    "data_aviso"
]

for coluna in colunas_data:
    df_modelagem_base[coluna] = df_modelagem_base[coluna].apply(
        converter_data_segura
    )

# Calculamos o intervalo entre a ocorrência e o aviso do sinistro.
df_modelagem_base["dias_ate_aviso"] = (
    df_modelagem_base["data_aviso"] -
    df_modelagem_base["data_sinistro"]
).dt.days

# Exibimos estatísticas para avaliar a nova variável temporal.
print("Resumo dos dias entre o sinistro e o aviso:")
display(df_modelagem_base["dias_ate_aviso"].describe())

# Verificamos valores ausentes e intervalos negativos.
print("Valores ausentes:", df_modelagem_base["dias_ate_aviso"].isna().sum())
print("Intervalos negativos:", (df_modelagem_base["dias_ate_aviso"] < 0).sum())

# Exibimos a distribuição dos intervalos mais frequentes.
display(
    df_modelagem_base["dias_ate_aviso"]
    .value_counts()
    .sort_index()
    .head(15)
)

# COMMAND ----------

# Extraímos o mês da data de ocorrência do sinistro.
df_modelagem_base["mes_sinistro"] = (
    df_modelagem_base["data_sinistro"].dt.month
)

# Extraímos o dia da semana da ocorrência.
# O pandas utiliza: segunda-feira = 0 e domingo = 6.
df_modelagem_base["dia_semana_sinistro"] = (
    df_modelagem_base["data_sinistro"].dt.dayofweek
)

# Exibimos as primeiras linhas para conferir as novas variáveis.
display(
    df_modelagem_base[
        [
            "data_sinistro",
            "mes_sinistro",
            "dia_semana_sinistro",
            "dias_ate_aviso"
        ]
    ].head(10)
)

# Verificamos se as novas variáveis possuem valores ausentes.
print("Valores ausentes por variável:")
display(
    df_modelagem_base[
        ["mes_sinistro", "dia_semana_sinistro"]
    ].isna().sum()
)

# COMMAND ----------

# Exibimos todas as colunas disponíveis na base de modelagem.
print("Total de colunas:", len(df_modelagem_base.columns))

# Listamos os nomes das colunas e seus tipos de dados.
display(
    pd.DataFrame({
        "coluna": df_modelagem_base.columns,
        "tipo": df_modelagem_base.dtypes.astype(str).values,
        "valores_ausentes": df_modelagem_base.isna().sum().values
    })
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### ## # CRIANDO BASE PREDITORA

# COMMAND ----------

# Definimos explicitamente as 24 variáveis que poderão ser utilizadas pelo modelo.
colunas_preditoras = [
    "idade",
    "tempo_cliente_anos",
    "score_credito",
    "estado_civil",
    "renda_mensal",
    "tipo_cobertura",
    "valor_segurado",
    "franquia",
    "premio_anual",
    "canal_venda",
    "alteracoes_apolice_90d",
    "qtd_sinistros_12m",
    "qtd_sinistros_total",
    "tipo_sinistro",
    "hora_sinistro",
    "uf",
    "boletim_ocorrencia",
    "qtd_testemunhas",
    "houve_vitima",
    "oficina_credenciada",
    "valor_sinistro_num",
    "dias_ate_aviso",
    "mes_sinistro",
    "dia_semana_sinistro"
]

# Criamos uma cópia independente das variáveis preditoras.
X = df_modelagem_base[colunas_preditoras].copy()

# Criamos uma cópia independente da variável que queremos prever.
y = df_modelagem_base["fraude"].copy()

# Preservamos o identificador do segurado para controlar a separação dos dados.
grupos_segurado = df_modelagem_base["id_segurado"].copy()

# Conferimos as dimensões das três estruturas.
print("Dimensões dos preditores (X):", X.shape)
print("Dimensões do alvo (y):", y.shape)
print("Quantidade de segurados distintos:", grupos_segurado.nunique())

# Conferimos a distribuição da variável-alvo.
display(y.value_counts().sort_index())

# COMMAND ----------

# Identificamos a data mais antiga e a mais recente dos sinistros.
print("Primeiro sinistro:", df_modelagem_base["data_sinistro"].min())
print("Último sinistro:", df_modelagem_base["data_sinistro"].max())

# Contamos os sinistros registrados em cada ano.
print("\nQuantidade de sinistros por ano:")
display(
    df_modelagem_base["data_sinistro"]
    .dt.year
    .value_counts()
    .sort_index()
)

# COMMAND ----------

# Criamos uma cópia apenas para auditar o histórico dos segurados.
auditoria_historico = df_modelagem_base[
    ["id_segurado", "data_sinistro", "qtd_sinistros_total"]
].copy()

# Ordenamos os sinistros de cada segurado pela data de ocorrência.
auditoria_historico = auditoria_historico.sort_values(
    ["id_segurado", "data_sinistro"]
)

# Calculamos quantos sinistros anteriores cada segurado possui na base.
auditoria_historico["sinistros_anteriores_na_base"] = (
    auditoria_historico.groupby("id_segurado").cumcount()
)

# Comparamos o histórico informado com a quantidade de sinistros anteriores.
auditoria_historico["diferenca_historico"] = (
    auditoria_historico["qtd_sinistros_total"]
    - auditoria_historico["sinistros_anteriores_na_base"]
)

# Exibimos quantos registros apresentam diferença entre os valores.
print("Distribuição da diferença entre histórico informado e histórico observado:")
display(
    auditoria_historico["diferenca_historico"]
    .value_counts()
    .sort_index()
)

# Exibimos alguns registros para análise.
display(auditoria_historico.head(15))

# COMMAND ----------

# Identificamos as variáveis históricas que foram geradas aleatoriamente.
colunas_excluir = [
    "qtd_sinistros_12m",
    "qtd_sinistros_total"
]

# Criamos uma nova versão dos preditores sem essas duas variáveis.
# A variável X original permanece preservada.
X_modelagem = X.drop(columns=colunas_excluir).copy()

# Conferimos a quantidade final de variáveis preditoras.
print("Dimensões anteriores:", X.shape)
print("Dimensões atualizadas:", X_modelagem.shape)

# Verificamos se as variáveis foram realmente removidas.
print("\nVariáveis excluídas:")
print([coluna for coluna in colunas_excluir if coluna not in X_modelagem.columns])

# Conferimos a distribuição do alvo, sem modificá-lo.
print("\nDistribuição da variável-alvo:")
display(y.value_counts().sort_index())

# COMMAND ----------

# Criamos uma cópia com o ano de ocorrência de cada sinistro.
base_divisao = df_modelagem_base[
    ["data_sinistro", "fraude"]
].copy()

# Extraímos o ano da data do sinistro.
base_divisao["ano_sinistro"] = (
    base_divisao["data_sinistro"].dt.year
)

# Agrupamos os registros por ano e resultado de fraude.
# A tabela mostra a quantidade de casos de cada classe.
distribuicao_temporal = pd.crosstab(
    base_divisao["ano_sinistro"],
    base_divisao["fraude"]
)

# Calculamos também o percentual de fraudes em cada ano.
distribuicao_temporal["percentual_fraude"] = (
    distribuicao_temporal[1]
    / distribuicao_temporal.sum(axis=1) * 100
)

# Exibimos a distribuição para avaliar a divisão temporal.
display(distribuicao_temporal)

# COMMAND ----------

# Identificamos o ano de ocorrência de cada sinistro.
anos_sinistro = df_modelagem_base["data_sinistro"].dt.year

# Selecionamos os índices dos sinistros de 2023 e 2024 para treinamento.
indices_treino = anos_sinistro.isin([2023, 2024])

# Selecionamos os índices dos sinistros de 2025 para teste.
indices_teste = anos_sinistro == 2025

# Criamos os preditores de treinamento.
X_treino = X_modelagem.loc[indices_treino].copy()

# Criamos os preditores de teste.
X_teste = X_modelagem.loc[indices_teste].copy()

# Separamos os respectivos resultados de fraude.
y_treino = y.loc[indices_treino].copy()
y_teste = y.loc[indices_teste].copy()

# Conferimos as dimensões dos conjuntos.
print("Treinamento:", X_treino.shape)
print("Teste:", X_teste.shape)

# Conferimos a distribuição das classes no treinamento.
print("\nDistribuição de fraude no treinamento:")
display(y_treino.value_counts().sort_index())

# Conferimos a distribuição das classes no teste.
print("\nDistribuição de fraude no teste:")
display(y_teste.value_counts().sort_index())

# Confirmamos os anos presentes em cada conjunto.
print("\nAnos no treinamento:", sorted(anos_sinistro.loc[indices_treino].unique()))
print("Anos no teste:", sorted(anos_sinistro.loc[indices_teste].unique()))

# COMMAND ----------

# Identificamos as colunas numéricas do conjunto de treinamento.
colunas_numericas = X_treino.select_dtypes(
    include=["number"]
).columns.tolist()

# Identificamos as colunas categóricas do conjunto de treinamento.
colunas_categoricas = X_treino.select_dtypes(
    include=["object", "string", "category"]
).columns.tolist()

# Exibimos a quantidade e os nomes das variáveis de cada grupo.
print("Quantidade de variáveis numéricas:", len(colunas_numericas))
print("Variáveis numéricas:", colunas_numericas)

print("\nQuantidade de variáveis categóricas:", len(colunas_categoricas))
print("Variáveis categóricas:", colunas_categoricas)

# Verificamos os valores ausentes em cada grupo no treinamento.
print("\nAusências nas variáveis numéricas:")
display(X_treino[colunas_numericas].isna().sum())

print("\nAusências nas variáveis categóricas:")
display(X_treino[colunas_categoricas].isna().sum())

# COMMAND ----------

# Importamos as ferramentas necessárias para construir o pré-processamento.
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Criamos o fluxo de tratamento das variáveis numéricas.
pipeline_numerico = Pipeline(steps=[
    # Preenchemos os valores ausentes utilizando a mediana de cada coluna.
    ("imputador", SimpleImputer(
        strategy="median",
        add_indicator=True
    )),

    # Padronizamos as variáveis numéricas.
    ("escalonador", StandardScaler())
])

# Criamos o fluxo de tratamento das variáveis categóricas.
pipeline_categorico = Pipeline(steps=[
    # Substituímos valores ausentes pela categoria "não informado".
    ("imputador", SimpleImputer(
        strategy="constant",
        fill_value="não informado"
    )),

    # Transformamos categorias em colunas numéricas.
    # Categorias desconhecidas no teste serão ignoradas.
    ("codificador", OneHotEncoder(
        handle_unknown="ignore"
    ))
])

# Combinamos os dois fluxos em um único pré-processador.
preprocessador = ColumnTransformer(transformers=[
    ("numericas", pipeline_numerico, colunas_numericas),
    ("categoricas", pipeline_categorico, colunas_categoricas)
])

# Ajustamos o pré-processador exclusivamente com os dados de treinamento.
X_treino_processado = preprocessador.fit_transform(X_treino)

# Aplicamos ao teste as transformações aprendidas no treinamento.
X_teste_processado = preprocessador.transform(X_teste)

# Exibimos as dimensões após o pré-processamento.
print("Dimensão do treino processado:", X_treino_processado.shape)
print("Dimensão do teste processado:", X_teste_processado.shape)

# Verificamos se ainda existem valores ausentes após as transformações.
import numpy as np

print("\nValores ausentes no treino processado:",
      np.isnan(X_treino_processado.data).sum()
      if hasattr(X_treino_processado, "data")
      else np.isnan(X_treino_processado).sum())

print("Valores ausentes no teste processado:",
      np.isnan(X_teste_processado.data).sum()
      if hasattr(X_teste_processado, "data")
      else np.isnan(X_teste_processado).sum())

# COMMAND ----------

# Importamos o MLflow para rastrear os experimentos.
import mlflow

# Consultamos o endereço de rastreamento utilizado pelo ambiente.
print("Tracking URI:", mlflow.get_tracking_uri())

# Consultamos o experimento atualmente selecionado.
experimento_atual = mlflow.get_experiment(
    mlflow.active_run().info.experiment_id
) if mlflow.active_run() else None

# Exibimos o experimento ativo, caso exista.
if experimento_atual:
    print("Experimento atual:", experimento_atual.name)
    print("ID do experimento:", experimento_atual.experiment_id)
else:
    print("Nenhuma execução está ativa neste momento.")

# COMMAND ----------

# Definimos o caminho absoluto do novo experimento no Workspace.
nome_experimento = (
    "/Users/vbtosta@gmail.com/"
    "PREVENCAO-DE-FRAUDE-EM-SINISTROS/"
    "Prevencao_Fraudes_Sinistros_2"
)

# Criamos o experimento ou selecionamos o existente.
mlflow.set_experiment(nome_experimento)

# Recuperamos as informações do experimento.
experimento = mlflow.get_experiment_by_name(nome_experimento)

# Exibimos os dados para confirmar a criação.
print("Experimento:", experimento.name)
print("ID:", experimento.experiment_id)
print("Localização:", experimento.artifact_location)

# COMMAND ----------

# Selecionamos o experimento criado para este projeto.
mlflow.set_experiment(nome_experimento)

# Iniciamos uma execução para registrar o pré-processamento.
with mlflow.start_run(run_name="preprocessamento_v1"):

    # Registramos informações gerais da base utilizada.
    mlflow.log_param("total_registros", 20000)
    mlflow.log_param("total_preditores_originais", 24)
    mlflow.log_param("total_preditores_selecionados", 22)

    # Registramos a estratégia de divisão temporal.
    mlflow.log_param("periodo_treinamento", "2023-2024")
    mlflow.log_param("periodo_teste", "2025")

    # Registramos as configurações de pré-processamento.
    mlflow.log_param("imputacao_numerica", "mediana")
    mlflow.log_param("imputacao_categorica", "nao_informado")
    mlflow.log_param("codificacao_categorica", "OneHotEncoder")
    mlflow.log_param("padronizacao", "StandardScaler")

    # Registramos as dimensões após a transformação.
    mlflow.log_metric("registros_treinamento", X_treino_processado.shape[0])
    mlflow.log_metric("registros_teste", X_teste_processado.shape[0])
    mlflow.log_metric("variaveis_transformadas", X_treino_processado.shape[1])

    # Registramos a quantidade de valores ausentes após o processamento.
    mlflow.log_metric("ausencias_treino", 0)
    mlflow.log_metric("ausencias_teste", 0)

    # Exibimos o identificador da execução criada.
    print("Execução registrada:", mlflow.active_run().info.run_id)

# COMMAND ----------

# Recuperamos as execuções registradas no experimento selecionado.
execucoes = mlflow.search_runs(
    experiment_ids=[experimento.experiment_id],
    order_by=["start_time DESC"]
)

# Exibimos o nome, o status e o identificador das execuções.
display(
    execucoes[
        ["run_id", "tags.mlflow.runName", "status", "start_time"]
    ]
)

# COMMAND ----------

# Importamos as bibliotecas necessárias para treinamento e avaliação.
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

# Criamos o modelo de Regressão Logística com pesos balanceados.
modelo_lr = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    random_state=42
)

# Iniciamos um experimento no MLflow para registrar o treinamento.
with mlflow.start_run(run_name="regressao_logistica_v1"):

    # Treinamos o modelo exclusivamente com os dados de treinamento.
    modelo_lr.fit(X_treino_processado, y_treino)

    # Geramos as previsões de classe para os dados de teste de 2025.
    y_pred = modelo_lr.predict(X_teste_processado)

    # Calculamos as probabilidades previstas para a classe fraude.
    y_proba = modelo_lr.predict_proba(X_teste_processado)[:, 1]

    # Calculamos as métricas de avaliação do modelo.
    acuracia = accuracy_score(y_teste, y_pred)
    precisao = precision_score(y_teste, y_pred, zero_division=0)
    recall = recall_score(y_teste, y_pred, zero_division=0)
    f1 = f1_score(y_teste, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_teste, y_proba)
    pr_auc = average_precision_score(y_teste, y_proba)

    # Exibimos os resultados das métricas.
    print("===== AVALIAÇÃO DA REGRESSÃO LOGÍSTICA =====")
    print(f"Acurácia:  {acuracia:.4f}")
    print(f"Precisão:  {precisao:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print(f"PR-AUC:    {pr_auc:.4f}")

    # Exibimos a matriz de confusão.
    print("\n===== MATRIZ DE CONFUSÃO =====")
    print(confusion_matrix(y_teste, y_pred))

    # Exibimos o relatório detalhado por classe.
    print("\n===== RELATÓRIO DE CLASSIFICAÇÃO =====")
    print(classification_report(y_teste, y_pred, zero_division=0))

    # Registramos os parâmetros utilizados no MLflow.
    mlflow.log_param("modelo", "Regressao_Logistica")
    mlflow.log_param("class_weight", "balanced")
    mlflow.log_param("max_iter", 1000)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("periodo_treinamento", "2023-2024")
    mlflow.log_param("periodo_teste", "2025")
    mlflow.log_param("limiar_classificacao", 0.5)

    # Registramos as métricas calculadas no MLflow.
    mlflow.log_metric("acuracia", acuracia)
    mlflow.log_metric("precisao", precisao)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("roc_auc", roc_auc)
    mlflow.log_metric("pr_auc", pr_auc)

    # Registramos o modelo e o pré-processador já ajustado.
    pipeline_completo = Pipeline(steps=[
        ("preprocessador", preprocessador),
        ("modelo", modelo_lr)
    ])

    mlflow.sklearn.log_model(
        pipeline_completo,
        artifact_path="modelo"
    )

    # Exibimos a confirmação do registro do experimento.
    print("\nTreinamento, avaliação e registro no MLflow concluídos!")

# COMMAND ----------

# Importamos as ferramentas para dividir os dados e duplicar o pré-processador.
from sklearn.model_selection import train_test_split
from sklearn.base import clone

# Separamos os dados de treinamento em duas partes.
X_treino_interno, X_validacao = train_test_split(
    X_treino,
    test_size=0.20,
    random_state=42,
    stratify=y_treino
)

# Separamos os respectivos rótulos de cada conjunto.
y_treino_interno = y_treino.loc[X_treino_interno.index]
y_validacao = y_treino.loc[X_validacao.index]

# Criamos uma cópia independente do pré-processador original.
preprocessador_validacao = clone(preprocessador)

# Ajustamos o pré-processador somente nos dados de treinamento interno.
X_treino_interno_processado = preprocessador_validacao.fit_transform(
    X_treino_interno
)

# Aplicamos as transformações aos dados de validação sem reajustar o pré-processador.
X_validacao_processado = preprocessador_validacao.transform(
    X_validacao
)

# Exibimos o tamanho dos conjuntos e a distribuição das classes.
print("Treinamento interno:", X_treino_interno.shape)
print("Validação:", X_validacao.shape)

print("\nFraudes no treinamento interno:")
print(y_treino_interno.value_counts())

print("\nFraudes na validação:")
print(y_validacao.value_counts())

print("\nVariáveis após o pré-processamento:",
      X_treino_interno_processado.shape[1])

# COMMAND ----------

# Importamos as métricas necessárias para avaliar o modelo.
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

# Criamos uma nova Regressão Logística para o experimento de validação.
modelo_lr_validacao = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    random_state=42
)

# Iniciamos um novo registro no MLflow.
with mlflow.start_run(run_name="regressao_logistica_validacao_v1"):

    # Treinamos o modelo somente com os dados de treinamento interno.
    modelo_lr_validacao.fit(
        X_treino_interno_processado,
        y_treino_interno
    )

    # Prevemos as classes do conjunto de validação.
    y_pred_validacao = modelo_lr_validacao.predict(
        X_validacao_processado
    )

    # Obtemos as probabilidades de fraude previstas pelo modelo.
    y_proba_validacao = modelo_lr_validacao.predict_proba(
        X_validacao_processado
    )[:, 1]

    # Calculamos as métricas de desempenho na validação.
    metricas_validacao = {
        "acuracia": accuracy_score(y_validacao, y_pred_validacao),
        "precisao": precision_score(
            y_validacao, y_pred_validacao, zero_division=0
        ),
        "recall": recall_score(
            y_validacao, y_pred_validacao, zero_division=0
        ),
        "f1_score": f1_score(
            y_validacao, y_pred_validacao, zero_division=0
        ),
        "roc_auc": roc_auc_score(y_validacao, y_proba_validacao),
        "pr_auc": average_precision_score(
            y_validacao, y_proba_validacao
        )
    }

    # Exibimos as métricas calculadas.
    print("===== RESULTADOS NA VALIDAÇÃO =====")
    for nome, valor in metricas_validacao.items():
        print(f"{nome}: {valor:.4f}")

    # Exibimos a matriz de confusão.
    print("\n===== MATRIZ DE CONFUSÃO =====")
    print(confusion_matrix(y_validacao, y_pred_validacao))

    # Exibimos o relatório detalhado por classe.
    print("\n===== RELATÓRIO DE CLASSIFICAÇÃO =====")
    print(classification_report(
        y_validacao,
        y_pred_validacao,
        zero_division=0
    ))

    # Registramos os parâmetros do experimento no MLflow.
    mlflow.log_param("modelo", "Regressao_Logistica")
    mlflow.log_param("class_weight", "balanced")
    mlflow.log_param("max_iter", 1000)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("limiar_classificacao", 0.5)
    mlflow.log_param("conjunto_validacao", "2023-2024")
    mlflow.log_param("proporcao_validacao", 0.20)

    # Registramos todas as métricas no MLflow.
    mlflow.log_metrics(metricas_validacao)

    # Reunimos o pré-processador ajustado e o modelo em um único pipeline.
    pipeline_validacao = Pipeline(steps=[
        ("preprocessador", preprocessador_validacao),
        ("modelo", modelo_lr_validacao)
    ])

    # Registramos o pipeline completo com exemplo de entrada para inferir a assinatura.
    mlflow.sklearn.log_model(
        sk_model=pipeline_validacao,
        name="modelo_validacao",
        input_example=X_validacao.head(5)
    )

    # Confirmamos o término do experimento.
    print("\nExperimento de validação registrado no MLflow!")

# COMMAND ----------

# Importamos as métricas necessárias para avaliar diferentes limiares.
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

# Definimos os limiares que serão investigados.
limiares = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]

# Criamos uma lista para armazenar os resultados.
resultados_limiares = []

# Avaliamos o modelo em cada limiar definido.
for limiar in limiares:

    # Transformamos as probabilidades em classificações de fraude ou não fraude.
    previsoes = (y_proba_validacao >= limiar).astype(int)

    # Calculamos as métricas para o limiar atual.
    resultados_limiares.append({
        "limiar": limiar,
        "precisao": precision_score(
            y_validacao, previsoes, zero_division=0
        ),
        "recall": recall_score(
            y_validacao, previsoes, zero_division=0
        ),
        "f1_score": f1_score(
            y_validacao, previsoes, zero_division=0
        ),
        "falsos_positivos": (
            ((y_validacao == 0) & (previsoes == 1)).sum()
        ),
        "fraudes_identificadas": (
            ((y_validacao == 1) & (previsoes == 1)).sum()
        )
    })

# Organizamos os resultados em uma tabela.
tabela_limiares = pd.DataFrame(resultados_limiares)

# Exibimos a comparação dos diferentes limiares.
display(tabela_limiares.round(4))

# COMMAND ----------

# Importamos o Random Forest e as métricas de avaliação.
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

# Criamos o modelo Random Forest com tratamento do desbalanceamento.
modelo_rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=4,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# Iniciamos um novo experimento no MLflow.
with mlflow.start_run(run_name="random_forest_validacao_v1"):

    # Treinamos o modelo somente com os dados de treinamento interno.
    modelo_rf.fit(
        X_treino_interno_processado,
        y_treino_interno
    )

    # Geramos as classificações usando o limiar padrão de 0,50.
    y_pred_rf = modelo_rf.predict(X_validacao_processado)

    # Obtemos as probabilidades previstas para a classe fraude.
    y_proba_rf = modelo_rf.predict_proba(
        X_validacao_processado
    )[:, 1]

    # Calculamos as métricas de avaliação.
    metricas_rf = {
        "acuracia": accuracy_score(y_validacao, y_pred_rf),
        "precisao": precision_score(
            y_validacao, y_pred_rf, zero_division=0
        ),
        "recall": recall_score(
            y_validacao, y_pred_rf, zero_division=0
        ),
        "f1_score": f1_score(
            y_validacao, y_pred_rf, zero_division=0
        ),
        "roc_auc": roc_auc_score(y_validacao, y_proba_rf),
        "pr_auc": average_precision_score(
            y_validacao, y_proba_rf
        )
    }

    # Exibimos os resultados do Random Forest.
    print("===== RESULTADOS RANDOM FOREST =====")
    for nome, valor in metricas_rf.items():
        print(f"{nome}: {valor:.4f}")

    # Exibimos a matriz de confusão.
    print("\n===== MATRIZ DE CONFUSÃO =====")
    print(confusion_matrix(y_validacao, y_pred_rf))

    # Exibimos o relatório detalhado por classe.
    print("\n===== RELATÓRIO DE CLASSIFICAÇÃO =====")
    print(classification_report(
        y_validacao,
        y_pred_rf,
        zero_division=0
    ))

    # Registramos os parâmetros do Random Forest no MLflow.
    mlflow.log_param("modelo", "RandomForest")
    mlflow.log_param("n_estimators", 300)
    mlflow.log_param("max_depth", 15)
    mlflow.log_param("min_samples_split", 10)
    mlflow.log_param("min_samples_leaf", 4)
    mlflow.log_param("class_weight", "balanced")
    mlflow.log_param("random_state", 42)
    mlflow.log_param("limiar_classificacao", 0.5)
    mlflow.log_param("periodo_validacao", "2023-2024")

    # Registramos as métricas no MLflow.
    mlflow.log_metrics(metricas_rf)

    # Montamos o pipeline completo com o pré-processador já ajustado.
    pipeline_rf = Pipeline(steps=[
        ("preprocessador", preprocessador_validacao),
        ("modelo", modelo_rf)
    ])

    # Registramos o pipeline completo no MLflow.
    mlflow.sklearn.log_model(
        sk_model=pipeline_rf,
        name="random_forest_validacao",
        input_example=X_validacao.head(5)
    )

    # Confirmamos a conclusão do experimento.
    print("\nRandom Forest treinado e registrado no MLflow!")

# COMMAND ----------

# Importamos as métricas necessárias para avaliar os limiares.
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

# Definimos os limiares que serão investigados.
limiares_rf = [
    0.01, 0.02, 0.03, 0.05, 0.08,
    0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50
]

# Criamos uma lista para armazenar os resultados.
resultados_rf = []

# Avaliamos o comportamento do Random Forest em cada limiar.
for limiar in limiares_rf:

    # Classificamos como fraude os casos com probabilidade acima do limiar.
    previsoes_rf = (y_proba_rf >= limiar).astype(int)

    # Calculamos e armazenamos as métricas e quantidades.
    resultados_rf.append({
        "limiar": limiar,
        "precisao": precision_score(
            y_validacao, previsoes_rf, zero_division=0
        ),
        "recall": recall_score(
            y_validacao, previsoes_rf, zero_division=0
        ),
        "f1_score": f1_score(
            y_validacao, previsoes_rf, zero_division=0
        ),
        "fraudes_identificadas": (
            ((y_validacao == 1) & (previsoes_rf == 1)).sum()
        ),
        "falsos_positivos": (
            ((y_validacao == 0) & (previsoes_rf == 1)).sum()
        ),
        "total_alertas": previsoes_rf.sum()
    })

# Organizamos os resultados em uma tabela.
tabela_limiares_rf = pd.DataFrame(resultados_rf)

# Exibimos a comparação dos limiares.
display(tabela_limiares_rf.round(4))

# COMMAND ----------


import pandas as pd
from sklearn.metrics import confusion_matrix

# Limiares definidos para a comparação inicial
limiar_lr = 0.50
limiar_rf = 0.25

# Gerar previsões mantendo os índices originais da validação
pred_lr = pd.Series(
    (y_proba_validacao >= limiar_lr).astype(int),
    index=y_validacao.index
)

pred_rf = pd.Series(
    (y_proba_rf >= limiar_rf).astype(int),
    index=y_validacao.index
)

# Função para resumir erros e exposição financeira potencial
def analisar_erros(nome, y_real, y_pred, X):
    # Identificar falsos positivos e falsos negativos
    falsos_positivos = (y_real == 0) & (y_pred == 1)
    falsos_negativos = (y_real == 1) & (y_pred == 0)

    # Recuperar os valores dos sinistros não identificados como fraude
    valores_fn = pd.to_numeric(
        X.loc[falsos_negativos, "valor_sinistro_num"],
        errors="coerce"
    )

    return {
        "Modelo": nome,
        "Falsos positivos": int(falsos_positivos.sum()),
        "Falsos negativos": int(falsos_negativos.sum()),
        "Fraudes identificadas": int(((y_real == 1) & (y_pred == 1)).sum()),
        "Valor potencial não detectado (R$)": valores_fn.sum(),
        "Valor médio por fraude não detectada (R$)": valores_fn.mean(),
        "Valores ausentes": int(valores_fn.isna().sum())
    }

# Comparar os dois modelos
comparacao_erros = pd.DataFrame([
    analisar_erros(
        "Regressão Logística",
        y_validacao,
        pred_lr,
        X_validacao
    ),
    analisar_erros(
        "Random Forest",
        y_validacao,
        pred_rf,
        X_validacao
    )
])

display(comparacao_erros.round(2))


# COMMAND ----------


# Custos hipotéticos por investigação, em reais
custos_unitarios = [100, 200, 300]

# Quantidade total de sinistros encaminhados para investigação
investigacoes = {
    "Regressão Logística": 864,
    "Random Forest": 539
}

# Exposição financeira potencial não detectada
exposicao = {
    "Regressão Logística": 1644774.79,
    "Random Forest": 2416089.60
}

# Construir a análise de sensibilidade
resultados_custos = []

for custo in custos_unitarios:
    for modelo in investigacoes:
        custo_investigacao = investigacoes[modelo] * custo
        custo_estimado = custo_investigacao + exposicao[modelo]

        resultados_custos.append({
            "Modelo": modelo,
            "Custo unitário (R$)": custo,
            "Investigações": investigacoes[modelo],
            "Custo das investigações (R$)": custo_investigacao,
            "Exposição potencial (R$)": exposicao[modelo],
            "Custo estimado total (R$)": custo_estimado
        })

df_custos = pd.DataFrame(resultados_custos)

display(df_custos.round(2))


# COMMAND ----------


# Percentuais hipotéticos de efetividade das investigações
efetividades = [0.25, 0.50, 0.75, 1.00]

# Custos hipotéticos por investigação
custos_unitarios = [100, 200, 300]

# Dados da validação para cada modelo
modelos = {
    "Regressão Logística": {
        "investigacoes": 864,
        "exposicao": 1644774.79
    },
    "Random Forest": {
        "investigacoes": 539,
        "exposicao": 2416089.60
    }
}

# Lista para armazenar os cenários simulados
resultados_sensibilidade = []

# Avaliar todas as combinações de custo e efetividade
for nome_modelo, dados in modelos.items():

    for custo_unitario in custos_unitarios:

        for efetividade in efetividades:

            # Custo operacional das investigações
            custo_investigacao = (
                dados["investigacoes"] * custo_unitario
            )

            # Exposição financeira que permaneceria após a investigação
            exposicao_residual = (
                dados["exposicao"] * (1 - efetividade)
            )

            # Custo econômico estimado no cenário
            custo_total = custo_investigacao + exposicao_residual

            resultados_sensibilidade.append({
                "Modelo": nome_modelo,
                "Custo unitário (R$)": custo_unitario,
                "Efetividade (%)": efetividade * 100,
                "Investigações": dados["investigacoes"],
                "Custo investigação (R$)": custo_investigacao,
                "Exposição residual (R$)": exposicao_residual,
                "Custo total estimado (R$)": custo_total
            })

# Criar tabela final da análise
df_sensibilidade = pd.DataFrame(resultados_sensibilidade)

# Exibir resultados ordenados
display(
    df_sensibilidade.sort_values(
        ["Custo unitário (R$)", "Efetividade (%)", "Modelo"]
    ).round(2)
)


# COMMAND ----------


# Calcular a efetividade em que os dois modelos teriam o mesmo custo

dados_lr = modelos["Regressão Logística"]
dados_rf = modelos["Random Forest"]

pontos_equilibrio = []

for custo_unitario in custos_unitarios:

    # Diferença entre os custos de investigação
    diferenca_investigacao = (
        dados_lr["investigacoes"] - dados_rf["investigacoes"]
    ) * custo_unitario

    # Diferença entre as exposições potenciais
    diferenca_exposicao = (
        dados_rf["exposicao"] - dados_lr["exposicao"]
    )

    # Efetividade de equilíbrio do Random Forest
    efetividade_equilibrio = (
        1 - diferenca_investigacao / diferenca_exposicao
    ) * 100

    pontos_equilibrio.append({
        "Custo por investigação (R$)": custo_unitario,
        "Efetividade de equilíbrio do RF (%)": efetividade_equilibrio
    })

df_equilibrio = pd.DataFrame(pontos_equilibrio)

display(df_equilibrio.round(2))


# COMMAND ----------


import pandas as pd
import numpy as np

# Recuperar os nomes das variáveis após o pré-processamento
nomes_features = preprocessador_validacao.get_feature_names_out()

# Extrair os coeficientes da Regressão Logística
coeficientes = modelo_lr_validacao.coef_[0]

# Construir uma tabela com os resultados
df_coeficientes = pd.DataFrame({
    "Variavel": nomes_features,
    "Coeficiente": coeficientes,
    "Importancia_absoluta": np.abs(coeficientes),
    "Razao_de_chances": np.exp(coeficientes)
})

# Ordenar pelas maiores magnitudes dos coeficientes
df_coeficientes = df_coeficientes.sort_values(
    by="Importancia_absoluta",
    ascending=False
).reset_index(drop=True)

# Exibir as 20 variáveis com maiores magnitudes
display(df_coeficientes.head(20).round(4))


# COMMAND ----------


import matplotlib.pyplot as plt

# Selecionar as 20 variáveis com maior magnitude de coeficiente
df_top_coef = df_coeficientes.head(20).copy()

# Ordenar para facilitar a leitura do gráfico
df_top_coef = df_top_coef.sort_values("Coeficiente")

# Definir cores conforme o sentido do coeficiente
cores = [
    "steelblue" if valor < 0 else "indianred"
    for valor in df_top_coef["Coeficiente"]
]

# Construir o gráfico
plt.figure(figsize=(12, 9))

plt.barh(
    df_top_coef["Variavel"],
    df_top_coef["Coeficiente"],
    color=cores
)

plt.axvline(0, color="black", linewidth=0.8)

plt.title(
    "Regressão Logística — Coeficientes das 20 principais variáveis",
    fontsize=14
)
plt.xlabel("Coeficiente do modelo")
plt.ylabel("Variáveis")
plt.grid(axis="x", alpha=0.25)
plt.tight_layout()
plt.show()


# COMMAND ----------

# Verificar a instalação da biblioteca SHAP
import shap

print("SHAP instalado com sucesso!")
print("Versão:", shap.__version__)

# COMMAND ----------

import pandas as pd

# Recupera os nomes das 53 variáveis após o pré-processamento
nomes_features_shap = preprocessador_validacao.get_feature_names_out()

# Converte os dados de treinamento processados para formato compatível com SHAP
dados_treino_shap = (
    X_treino_interno_processado.toarray()
    if hasattr(X_treino_interno_processado, "toarray")
    else X_treino_interno_processado
)

# Organiza os dados em um DataFrame com os nomes das variáveis
df_treino_shap = pd.DataFrame(
    dados_treino_shap,
    columns=nomes_features_shap
)

# Seleciona uma amostra de referência para o explicador
background_shap = df_treino_shap.sample(
    n=min(200, len(df_treino_shap)),
    random_state=42
)

print("Preparação concluída!")
print("Dimensão dos dados de referência:", background_shap.shape)
print("Quantidade de variáveis:", len(nomes_features_shap))

# COMMAND ----------

# Cria o explicador SHAP para a Regressão Logística
explainer_shap = shap.LinearExplainer(
    modelo_lr_validacao,
    background_shap
)

print("Explicador SHAP criado com sucesso!")

# COMMAND ----------

# Converte os dados de validação processados para formato compatível
dados_validacao_shap = (
    X_validacao_processado.toarray()
    if hasattr(X_validacao_processado, "toarray")
    else X_validacao_processado
)

# Organiza os dados com os nomes das 53 variáveis
df_validacao_shap = pd.DataFrame(
    dados_validacao_shap,
    columns=nomes_features_shap
)

# Seleciona 300 registros para análise
amostra_validacao_shap = df_validacao_shap.sample(
    n=min(300, len(df_validacao_shap)),
    random_state=42
)

# Calcula as contribuições SHAP
valores_shap = explainer_shap(amostra_validacao_shap)

print("Cálculo SHAP concluído!")
print("Registros analisados:", valores_shap.shape[0])
print("Variáveis analisadas:", valores_shap.shape[1])

# COMMAND ----------

# Gráfico global de explicabilidade SHAP
shap.plots.beeswarm(
    valores_shap,
    max_display=20
)

# COMMAND ----------

# Gráfico de importância global das variáveis pelo SHAP
shap.plots.bar(
    valores_shap,
    max_display=20
)

# COMMAND ----------

import numpy as np
import pandas as pd

# Calcula as probabilidades de fraude no conjunto de validação
probabilidades_validacao = modelo_lr_validacao.predict_proba(
    X_validacao_processado
)[:, 1]

# Aplica o limiar de classificação de 0,50
previsoes_validacao = (probabilidades_validacao >= 0.50).astype(int)

# Converte os valores reais para um array, preservando a ordem dos registros
valores_reais = np.asarray(y_validacao)

# Identifica os verdadeiros positivos: fraude real identificada pelo modelo
posicoes_tp = np.where(
    (valores_reais == 1) & (previsoes_validacao == 1)
)[0]

# Identifica os falsos positivos: não fraude classificada como fraude
posicoes_fp = np.where(
    (valores_reais == 0) & (previsoes_validacao == 1)
)[0]

# Seleciona o caso com maior probabilidade em cada grupo
posicao_tp = posicoes_tp[
    np.argmax(probabilidades_validacao[posicoes_tp])
]

posicao_fp = posicoes_fp[
    np.argmax(probabilidades_validacao[posicoes_fp])
]

# Exibe os dois casos selecionados
casos_selecionados = pd.DataFrame({
    "Caso": ["Verdadeiro positivo", "Falso positivo"],
    "Posição": [posicao_tp, posicao_fp],
    "Classe_real": [valores_reais[posicao_tp], valores_reais[posicao_fp]],
    "Probabilidade_fraude": [
        probabilidades_validacao[posicao_tp],
        probabilidades_validacao[posicao_fp]
    ],
    "Previsao_modelo": [
        previsoes_validacao[posicao_tp],
        previsoes_validacao[posicao_fp]
    ]
})

display(casos_selecionados)

# COMMAND ----------

# Seleciona os dois registros na mesma ordem usada na validação
casos_shap = df_validacao_shap.iloc[
    [posicao_tp, posicao_fp]
].copy()

# Calcula os valores SHAP individuais
explicacoes_shap = explainer_shap(casos_shap)

print("Explicações individuais calculadas!")
print("Quantidade de casos:", explicacoes_shap.shape[0])
print("Variáveis explicadas:", explicacoes_shap.shape[1])

# COMMAND ----------

# Gráfico Waterfall: explicação individual do verdadeiro positivo
shap.plots.waterfall(
    explicacoes_shap[0],
    max_display=20
)

# COMMAND ----------

# Gráfico Waterfall: explicação individual do falso positivo
shap.plots.waterfall(
    explicacoes_shap[1],
    max_display=20
)

# COMMAND ----------

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Modelo final de Regressão Logística
modelo_lr_final = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    random_state=42
)

# Modelo final Random Forest
modelo_rf_final = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=4,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# Treina os modelos com todo o período de 2023 e 2024
modelo_lr_final.fit(X_treino_processado, y_treino)
modelo_rf_final.fit(X_treino_processado, y_treino)

print("Treinamento final concluído!")
print("Regressão Logística:", modelo_lr_final)
print("Random Forest:", modelo_rf_final)

# COMMAND ----------

import numpy as np

# Calcula as probabilidades de fraude para os dados de 2025
prob_lr_teste = modelo_lr_final.predict_proba(X_teste_processado)[:, 1]
prob_rf_teste = modelo_rf_final.predict_proba(X_teste_processado)[:, 1]

# Aplica os limiares definidos anteriormente na validação
pred_lr_teste = (prob_lr_teste >= 0.50).astype(int)
pred_rf_teste = (prob_rf_teste >= 0.25).astype(int)

print("Previsões realizadas com sucesso!")
print("Registros avaliados:", len(y_teste))
print("Fraudes previstas pela Regressão Logística:", pred_lr_teste.sum())
print("Fraudes previstas pelo Random Forest:", pred_rf_teste.sum())

# COMMAND ----------

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)

# Função para calcular as métricas de avaliação
def avaliar_modelo(nome, y_real, y_pred, probabilidades):

    matriz = confusion_matrix(y_real, y_pred)
    tn, fp, fn, tp = matriz.ravel()

    return {
        "Modelo": nome,
        "Accuracy": accuracy_score(y_real, y_pred),
        "Precision": precision_score(y_real, y_pred),
        "Recall": recall_score(y_real, y_pred),
        "F1": f1_score(y_real, y_pred),
        "ROC_AUC": roc_auc_score(y_real, probabilidades),
        "PR_AUC": average_precision_score(y_real, probabilidades),
        "Verdadeiros_Pos": tp,
        "Falsos_Pos": fp,
        "Verdadeiros_Neg": tn,
        "Falsos_Neg": fn
    }

# Avalia os dois modelos no conjunto de teste de 2025
resultados_finais = pd.DataFrame([
    avaliar_modelo(
        "Regressão Logística",
        y_teste,
        pred_lr_teste,
        prob_lr_teste
    ),
    avaliar_modelo(
        "Random Forest",
        y_teste,
        pred_rf_teste,
        prob_rf_teste
    )
])

display(resultados_finais.round(4))

# COMMAND ----------

# Recupera os valores dos sinistros de 2025 pelos índices do conjunto de teste
valores_sinistros_teste = df_modelagem_base.loc[
    X_teste.index, "valor_sinistro_num"
]

# Confere a recuperação dos valores
print("Quantidade de registros:", len(valores_sinistros_teste))
print("Valores ausentes:", valores_sinistros_teste.isna().sum())
print("Valor total dos sinistros: R$", round(valores_sinistros_teste.sum(), 2))

# COMMAND ----------



# COMMAND ----------

# Converte os valores reais e as previsões em arrays
y_teste_array = np.asarray(y_teste)
valores_array = np.asarray(valores_sinistros_teste)

# Identifica as fraudes não detectadas por cada modelo
mascara_fn_lr = (
    (y_teste_array == 1) &
    (pred_lr_teste == 0)
)

mascara_fn_rf = (
    (y_teste_array == 1) &
    (pred_rf_teste == 0)
)

# Calcula a exposição financeira potencial das fraudes não detectadas
exposicao_lr = valores_array[mascara_fn_lr].sum()
exposicao_rf = valores_array[mascara_fn_rf].sum()

# Quantidade de investigações: verdadeiros positivos + falsos positivos
investigacoes_lr = int(pred_lr_teste.sum())
investigacoes_rf = int(pred_rf_teste.sum())

# Organiza os resultados
analise_economica_teste = pd.DataFrame({
    "Indicador": [
        "Investigações geradas",
        "Fraudes não identificadas",
        "Exposição potencial não identificada",
        "Valor médio por fraude não identificada"
    ],
    "Regressão Logística": [
        investigacoes_lr,
        int(mascara_fn_lr.sum()),
        exposicao_lr,
        exposicao_lr / mascara_fn_lr.sum()
    ],
    "Random Forest": [
        investigacoes_rf,
        int(mascara_fn_rf.sum()),
        exposicao_rf,
        exposicao_rf / mascara_fn_rf.sum()
    ]
})

display(analise_economica_teste)

# COMMAND ----------

# Define os custos unitários hipotéticos por investigação
custos_unitarios = [100, 200, 300]

# Armazena os resultados da simulação
resultados_custos = []

# Calcula o custo total para cada cenário
for custo in custos_unitarios:

    # Custo operacional da Regressão Logística
    custo_lr = (
        investigacoes_lr * custo + exposicao_lr
    )

    # Custo operacional do Random Forest
    custo_rf = (
        investigacoes_rf * custo + exposicao_rf
    )

    resultados_custos.append({
        "Custo_por_investigacao": custo,
        "Custo_total_LR": custo_lr,
        "Custo_total_RF": custo_rf,
        "Vantagem_LR": custo_rf - custo_lr
    })

# Organiza os resultados em uma tabela
df_custos_operacionais = pd.DataFrame(resultados_custos)

display(df_custos_operacionais.round(2))

# Calcula o custo unitário de investigação no ponto de equilíbrio
custo_equilibrio = (
    exposicao_rf - exposicao_lr
) / (
    investigacoes_lr - investigacoes_rf
)

print(
    "Custo unitário de investigação no ponto de equilíbrio: R$",
    round(custo_equilibrio, 2)
)

# COMMAND ----------

import mlflow

# Define o experimento do projeto
mlflow.set_experiment(
    "/Users/vbtosta@gmail.com/PREVENCAO-DE-FRAUDE-EM-SINISTROS/Prevencao_Fraudes_Sinistros_2"
)

# Recupera o experimento ativo
experimento = mlflow.get_experiment_by_name(
    "/Users/vbtosta@gmail.com/PREVENCAO-DE-FRAUDE-EM-SINISTROS/Prevencao_Fraudes_Sinistros_2"
)

print("Experimento:", experimento.name)
print("ID:", experimento.experiment_id)
print("Local dos artefatos:", experimento.artifact_location)

# COMMAND ----------

from sklearn.pipeline import Pipeline
import numpy as np

# Monta o pipeline completo com o pré-processador já ajustado
pipeline_lr_final = Pipeline([
    ("preprocessador", preprocessador),
    ("classificador", modelo_lr_final)
])

# Gera novamente as probabilidades usando os dados originais de teste
probabilidades_pipeline_lr = pipeline_lr_final.predict_proba(
    X_teste
)[:, 1]

# Verifica se o pipeline reproduz as probabilidades já avaliadas
diferenca_maxima = np.max(
    np.abs(probabilidades_pipeline_lr - prob_lr_teste)
)

print("Pipeline completo criado!")
print("Quantidade de registros:", len(probabilidades_pipeline_lr))
print("Diferença máxima entre probabilidades:", diferenca_maxima)
print(
    "Resultados reproduzidos:",
    np.allclose(probabilidades_pipeline_lr, prob_lr_teste)
)

# COMMAND ----------

from mlflow.models import infer_signature

# Seleciona registros de treinamento que possuem pelo menos um valor ausente
amostra_assinatura = X_treino.loc[
    X_treino.isna().any(axis=1)
].head(5).copy()

# Gera as previsões usando os dados originais
previsoes_assinatura = pipeline_lr_final.predict(amostra_assinatura)

# Infere a assinatura de entrada e saída do pipeline
assinatura_lr = infer_signature(
    amostra_assinatura,
    previsoes_assinatura
)

print("Registros usados:", len(amostra_assinatura))
print("Colunas de entrada:", amostra_assinatura.shape[1])
print("Valores ausentes na amostra:", amostra_assinatura.isna().sum().sum())
print("Assinatura preparada:", assinatura_lr is not None)

# COMMAND ----------

# Cria uma cópia da amostra para preparar a assinatura
amostra_assinatura_corrigida = amostra_assinatura.copy()

# Identifica as colunas inteiras da amostra
colunas_inteiras = amostra_assinatura_corrigida.select_dtypes(
    include=["int", "int32", "int64"]
).columns

# Converte essas colunas para float64
# Isso permite representar valores ausentes sem incompatibilidade de tipos
amostra_assinatura_corrigida[colunas_inteiras] = (
    amostra_assinatura_corrigida[colunas_inteiras].astype("float64")
)

# Gera previsões com a amostra corrigida
previsoes_assinatura = pipeline_lr_final.predict(
    amostra_assinatura_corrigida
)

# Reconstrói a assinatura do modelo
assinatura_lr = infer_signature(
    amostra_assinatura_corrigida,
    previsoes_assinatura
)

print("Colunas convertidas:", len(colunas_inteiras))
print("Valores ausentes:", amostra_assinatura_corrigida.isna().sum().sum())
print("Assinatura preparada:", assinatura_lr is not None)
print("Tipos inteiros restantes:",
      len(amostra_assinatura_corrigida.select_dtypes(include=["int"]).columns))

# COMMAND ----------

import mlflow
import mlflow.sklearn

# Define o experimento do projeto
mlflow.set_experiment(
    "/Users/vbtosta@gmail.com/PREVENCAO-DE-FRAUDE-EM-SINISTROS/Prevencao_Fraudes_Sinistros_2"
)

# Abre uma nova execução para registrar o modelo final
with mlflow.start_run(
    run_name="modelo_final_regressao_logistica_teste_2025"
) as run:

    # Registra os parâmetros do modelo
    mlflow.log_params({
        "algoritmo": "Regressao Logistica",
        "class_weight": "balanced",
        "max_iter": 1000,
        "random_state": 42,
        "limiar_classificacao": 0.50,
        "periodo_treinamento": "2023-2024",
        "periodo_teste": "2025",
        "quantidade_features": 22,
        "quantidade_registros_teste": 6649
    })

    # Registra as métricas de desempenho no teste de 2025
    mlflow.log_metrics({
        "accuracy": 0.6924,
        "precision": 0.1432,
        "recall": 0.6618,
        "f1": 0.2355,
        "roc_auc": 0.7631,
        "pr_auc": 0.2244,
        "verdadeiros_positivos": 315,
        "falsos_positivos": 1884,
        "verdadeiros_negativos": 4289,
        "falsos_negativos": 161,
        "alertas_investigacao": 2199,
        "exposicao_potencial_fraudes_nao_detectadas": 2935123.43
    })

    # Registra o pipeline completo, incluindo assinatura e exemplo de entrada
    mlflow.sklearn.log_model(
        sk_model=pipeline_lr_final,
        name="modelo_regressao_logistica_final",
        signature=assinatura_lr,
        input_example=amostra_assinatura_corrigida
    )

    # Guarda o identificador da execução
    id_execucao_lr_final = run.info.run_id

    print("Modelo registrado com sucesso!")
    print("ID da execução:", id_execucao_lr_final)

# COMMAND ----------

from sklearn.pipeline import Pipeline
import numpy as np

# Monta o pipeline completo do Random Forest
pipeline_rf_final = Pipeline([
    ("preprocessador", preprocessador),
    ("classificador", modelo_rf_final)
])

# Calcula as probabilidades usando os dados originais de teste
probabilidades_pipeline_rf = pipeline_rf_final.predict_proba(
    X_teste
)[:, 1]

# Compara com as probabilidades já calculadas na avaliação de 2025
diferenca_maxima_rf = np.max(
    np.abs(probabilidades_pipeline_rf - prob_rf_teste)
)

print("Pipeline Random Forest criado!")
print("Quantidade de registros:", len(probabilidades_pipeline_rf))
print("Diferença máxima entre probabilidades:", diferenca_maxima_rf)
print(
    "Resultados reproduzidos:",
    np.allclose(probabilidades_pipeline_rf, prob_rf_teste)
)

# COMMAND ----------

from mlflow.models import infer_signature

# Seleciona cinco registros com pelo menos um valor ausente
amostra_assinatura_rf = X_treino.loc[
    X_treino.isna().any(axis=1)
].head(5).copy()

# Identifica as colunas inteiras
colunas_inteiras_rf = amostra_assinatura_rf.select_dtypes(
    include=["int", "int32", "int64"]
).columns

# Converte as colunas inteiras para float64
amostra_assinatura_rf[colunas_inteiras_rf] = (
    amostra_assinatura_rf[colunas_inteiras_rf].astype("float64")
)

# Gera previsões com o pipeline completo
previsoes_assinatura_rf = pipeline_rf_final.predict(
    amostra_assinatura_rf
)

# Infere a assinatura de entrada e saída
assinatura_rf = infer_signature(
    amostra_assinatura_rf,
    previsoes_assinatura_rf
)

print("Registros utilizados:", len(amostra_assinatura_rf))
print("Colunas convertidas:", len(colunas_inteiras_rf))
print("Valores ausentes:", amostra_assinatura_rf.isna().sum().sum())
print("Assinatura preparada:", assinatura_rf is not None)
print(
    "Colunas inteiras restantes:",
    len(amostra_assinatura_rf.select_dtypes(include=["int"]).columns)
)

# COMMAND ----------

import mlflow
import mlflow.sklearn

# Define o experimento do projeto
mlflow.set_experiment(
    "/Users/vbtosta@gmail.com/PREVENCAO-DE-FRAUDE-EM-SINISTROS/Prevencao_Fraudes_Sinistros_2"
)

# Cria uma execução para o Random Forest final
with mlflow.start_run(
    run_name="modelo_final_random_forest_teste_2025"
) as run:

    # Registra os parâmetros utilizados
    mlflow.log_params({
        "algoritmo": "Random Forest",
        "n_estimators": 300,
        "max_depth": 15,
        "min_samples_split": 10,
        "min_samples_leaf": 4,
        "class_weight": "balanced",
        "random_state": 42,
        "n_jobs": -1,
        "limiar_classificacao": 0.25,
        "periodo_treinamento": "2023-2024",
        "periodo_teste": "2025",
        "quantidade_features": 22,
        "quantidade_registros_teste": 6649
    })

    # Registra as métricas do teste de 2025
    mlflow.log_metrics({
        "accuracy": 0.7756,
        "precision": 0.1764,
        "recall": 0.5819,
        "f1": 0.2708,
        "roc_auc": 0.7462,
        "pr_auc": 0.1954,
        "verdadeiros_positivos": 277,
        "falsos_positivos": 1293,
        "verdadeiros_negativos": 4880,
        "falsos_negativos": 199,
        "alertas_investigacao": 1570,
        "exposicao_potencial_fraudes_nao_detectadas": 3951496.83
    })

    # Registra o pipeline completo com assinatura e exemplo de entrada
    mlflow.sklearn.log_model(
        sk_model=pipeline_rf_final,
        name="modelo_random_forest_final",
        signature=assinatura_rf,
        input_example=amostra_assinatura_rf
    )

    # Guarda o identificador da execução
    id_execucao_rf_final = run.info.run_id

    print("Random Forest registrado com sucesso!")
    print("ID da execução:", id_execucao_rf_final)

# COMMAND ----------

# Consulta todas as execuções do experimento
execucoes = mlflow.search_runs(
    experiment_ids=["4429628036624567"],
    output_format="pandas"
)

# Define os nomes das duas execuções finais
nomes_modelos = [
    "modelo_final_regressao_logistica_teste_2025",
    "modelo_final_random_forest_teste_2025"
]

# Filtra os modelos finais usando Pandas
execucoes_finais = execucoes[
    execucoes["tags.mlflow.runName"].isin(nomes_modelos)
].copy()

# Seleciona as informações para conferência
colunas_verificacao = [
    "run_id",
    "tags.mlflow.runName",
    "status",
    "metrics.accuracy",
    "metrics.precision",
    "metrics.recall",
    "metrics.f1",
    "metrics.roc_auc",
    "metrics.pr_auc"
]

# Exibe os resultados
display(execucoes_finais[colunas_verificacao])

# COMMAND ----------

import mlflow

# Identifica o modelo registrado na execução final
uri_modelo_lr = (
    "runs:/7732cb6ed7e04222b46b603a578c680c/"
    "modelo_regressao_logistica_final"
)

# Carrega o pipeline completo armazenado no MLflow
modelo_lr_carregado = mlflow.sklearn.load_model(uri_modelo_lr)

# Confere o objeto recuperado
print("Modelo recuperado com sucesso!")
print("Tipo:", type(modelo_lr_carregado))
print("Etapas do pipeline:", modelo_lr_carregado.named_steps.keys())

# COMMAND ----------

import numpy as np

# Exibe as etapas do pipeline recuperado
print("Etapas:", list(modelo_lr_carregado.named_steps.keys()))

# Gera probabilidades com o modelo recuperado
probabilidades_lr_recuperado = (
    modelo_lr_carregado.predict_proba(X_teste)[:, 1]
)

# Compara com as probabilidades originais
diferenca_lr_recuperada = np.max(
    np.abs(probabilidades_lr_recuperado - prob_lr_teste)
)

print("Registros avaliados:", len(probabilidades_lr_recuperado))
print("Diferença máxima:", diferenca_lr_recuperada)
print(
    "Previsões reproduzidas:",
    np.allclose(probabilidades_lr_recuperado, prob_lr_teste)
)

# COMMAND ----------

import mlflow

# URI do artefato registrado no MLflow
uri_modelo_rf = (
    "runs:/35deeb8379624e939021321d7cf76240/"
    "modelo_random_forest_final"
)

# Recupera o pipeline completo
modelo_rf_carregado = mlflow.sklearn.load_model(uri_modelo_rf)

# Confere as etapas recuperadas
print("Modelo recuperado com sucesso!")
print("Tipo:", type(modelo_rf_carregado))
print("Etapas:", list(modelo_rf_carregado.named_steps.keys()))

# COMMAND ----------

# Monta o pipeline completo do Random Forest
pipeline_rf_final = Pipeline([
    ("preprocessador", preprocessador),
    ("classificador", modelo_rf_final)
])

# Gera probabilidades diretamente a partir dos dados originais
probabilidades_pipeline_rf = pipeline_rf_final.predict_proba(
    X_teste
)[:, 1]

# Compara com as probabilidades já calculadas na avaliação final
diferenca_maxima_rf = np.max(
    np.abs(probabilidades_pipeline_rf - prob_rf_teste)
)

print("Pipeline Random Forest criado!")
print("Registros avaliados:", len(probabilidades_pipeline_rf))
print("Diferença máxima:", diferenca_maxima_rf)
print(
    "Previsões reproduzidas:",
    np.allclose(probabilidades_pipeline_rf, prob_rf_teste)
)

# COMMAND ----------

import mlflow

# Identificadores das execuções finais
run_id_lr = "7732cb6ed7e04222b46b603a578c680c"
run_id_rf = "35deeb8379624e939021321d7cf76240"

# Recupera os dados das execuções
run_lr = mlflow.get_run(run_id_lr)
run_rf = mlflow.get_run(run_id_rf)

# Exibe os parâmetros e métricas registrados
print("REGRESSÃO LOGÍSTICA")
print("Status:", run_lr.info.status)
print("Parâmetros:", run_lr.data.params)
print("Métricas:", run_lr.data.metrics)

print("\nRANDOM FOREST")
print("Status:", run_rf.info.status)
print("Parâmetros:", run_rf.data.params)
print("Métricas:", run_rf.data.metrics)

# COMMAND ----------

import mlflow

# Identificadores dos modelos registrados
run_id_lr = "7732cb6ed7e04222b46b603a578c680c"
run_id_rf = "35deeb8379624e939021321d7cf76240"

# Recupera o URI dos modelos armazenados em cada execução
uri_lr = f"runs:/{run_id_lr}/modelo_regressao_logistica_final"
uri_rf = f"runs:/{run_id_rf}/modelo_random_forest_final"

# Recupera os pipelines completos
modelo_lr_recuperado = mlflow.sklearn.load_model(uri_lr)
modelo_rf_recuperado = mlflow.sklearn.load_model(uri_rf)

# Confere os tipos e as etapas dos pipelines
print("REGRESSÃO LOGÍSTICA")
print("Tipo:", type(modelo_lr_recuperado))
print("Etapas:", list(modelo_lr_recuperado.named_steps.keys()))

print("\nRANDOM FOREST")
print("Tipo:", type(modelo_rf_recuperado))
print("Etapas:", list(modelo_rf_recuperado.named_steps.keys()))

# COMMAND ----------

import numpy as np

# Gera probabilidades com a Regressão Logística recuperada
prob_lr_recuperado = modelo_lr_recuperado.predict_proba(
    X_teste
)[:, 1]

# Gera probabilidades com o Random Forest recuperado
prob_rf_recuperado = modelo_rf_recuperado.predict_proba(
    X_teste
)[:, 1]

# Compara as probabilidades com os resultados originais
diferenca_lr = np.max(
    np.abs(prob_lr_recuperado - prob_lr_teste)
)

diferenca_rf = np.max(
    np.abs(prob_rf_recuperado - prob_rf_teste)
)

# Apresenta os resultados
print("REGRESSÃO LOGÍSTICA")
print("Diferença máxima:", diferenca_lr)
print("Resultados reproduzidos:",
      np.allclose(prob_lr_recuperado, prob_lr_teste))

print("\nRANDOM FOREST")
print("Diferença máxima:", diferenca_rf)
print("Resultados reproduzidos:",
      np.allclose(prob_rf_recuperado, prob_rf_teste))

# COMMAND ----------

import numpy as np

# Aplica os limiares definidos durante a validação
pred_lr_recuperado = (
    prob_lr_recuperado >= 0.50
).astype(int)

pred_rf_recuperado = (
    prob_rf_recuperado >= 0.25
).astype(int)

# Compara as classificações recuperadas com as originais
print("REGRESSÃO LOGÍSTICA")
print(
    "Classificações reproduzidas:",
    np.array_equal(pred_lr_recuperado, pred_lr_teste)
)

print("\nRANDOM FOREST")
print(
    "Classificações reproduzidas:",
    np.array_equal(pred_rf_recuperado, pred_rf_teste)
)

# COMMAND ----------

# Verifica as colunas esperadas pelos modelos
print("Quantidade de variáveis:", len(X_teste.columns))

print("\nColunas utilizadas na modelagem:")
print(X_teste.columns.tolist())

print("\nFormato dos dados:")
print(X_teste.shape)

print("\nTipos de dados:")
print(X_teste.dtypes.value_counts())

# COMMAND ----------

import pandas as pd
import numpy as np

def prever_fraudes(novos_dados):

    # Verifica se os dados recebidos possuem as 22 variáveis esperadas
    colunas_esperadas = X_teste.columns.tolist()

    colunas_recebidas = novos_dados.columns.tolist()

    if set(colunas_recebidas) != set(colunas_esperadas):
        raise ValueError(
            "As colunas recebidas não correspondem às variáveis do treinamento."
        )

    # Reorganiza as colunas na mesma ordem do treinamento
    novos_dados = novos_dados[colunas_esperadas].copy()

    # Calcula as probabilidades de fraude
    prob_lr = modelo_lr_recuperado.predict_proba(
        novos_dados
    )[:, 1]

    prob_rf = modelo_rf_recuperado.predict_proba(
        novos_dados
    )[:, 1]

    # Aplica os limiares operacionais definidos na validação
    classificacao_lr = (prob_lr >= 0.50).astype(int)

    classificacao_rf = (prob_rf >= 0.25).astype(int)

    # Organiza os resultados em uma tabela
    resultados = pd.DataFrame({
        "probabilidade_lr": prob_lr,
        "classificacao_lr": classificacao_lr,
        "probabilidade_rf": prob_rf,
        "classificacao_rf": classificacao_rf
    })

    # Define uma recomendação de investigação baseada nos dois modelos
    resultados["recomendacao"] = np.select(
        [
            (classificacao_lr == 1) & (classificacao_rf == 1),
            (classificacao_lr == 1) | (classificacao_rf == 1)
        ],
        [
            "Investigar - concordância dos modelos",
            "Revisar - divergência entre modelos"
        ],
        default="Sem alerta pelos modelos"
    )

    return resultados

# COMMAND ----------

# Seleciona uma amostra de 5 sinistros para teste
amostra_teste = X_teste.head(5).copy()

# Executa a função de inferência
resultado_teste = prever_fraudes(amostra_teste)

# Exibe os resultados
display(resultado_teste)

# COMMAND ----------

# Executa a inferência em todos os registros de teste
resultados_inferencia_2025 = prever_fraudes(X_teste)

# Verifica a quantidade de registros processados
print("Registros processados:",
      len(resultados_inferencia_2025))

# Verifica se existem probabilidades ausentes
print("\nValores ausentes:")
print(resultados_inferencia_2025.isnull().sum())

# Apresenta a distribuição das recomendações
print("\nDistribuição das recomendações:")
print(
    resultados_inferencia_2025["recomendacao"]
    .value_counts()
)

# Exibe as primeiras linhas
display(resultados_inferencia_2025.head())

# COMMAND ----------

print("REGRESSÃO LOGÍSTICA")
print(
    np.array_equal(
        resultados_inferencia_2025["classificacao_lr"].to_numpy(),
        pred_lr_teste
    )
)

print("\nRANDOM FOREST")
print(
    np.array_equal(
        resultados_inferencia_2025["classificacao_rf"].to_numpy(),
        pred_rf_teste
    )
)

print("\nTOTAL DE ALERTAS")
print("Regressão Logística:",
      resultados_inferencia_2025["classificacao_lr"].sum())

print("Random Forest:",
      resultados_inferencia_2025["classificacao_rf"].sum())

# COMMAND ----------

# Recupera os identificadores e os resultados reais dos sinistros
dados_reais = df_modelagem_base.loc[
    X_teste.index,
    ["id_sinistro", "fraude"]
].copy()

# Combina os dados reais com as previsões dos modelos
resultados_finais_2025 = pd.concat(
    [
        dados_reais.reset_index(drop=True),
        resultados_inferencia_2025.reset_index(drop=True)
    ],
    axis=1
)

# Verifica a estrutura da tabela consolidada
print("Dimensão da tabela:", resultados_finais_2025.shape)

print("\nColunas:")
print(resultados_finais_2025.columns.tolist())

print("\nValores ausentes:")
print(resultados_finais_2025.isnull().sum())

print("\nAmostra dos resultados:")
display(resultados_finais_2025.head(10))

# COMMAND ----------

# Verifica a integridade da tabela consolidada
print("Quantidade de registros:", len(resultados_finais_2025))
print("Quantidade de colunas:", len(resultados_finais_2025.columns))

print("\nValores ausentes:")
print(resultados_finais_2025.isnull().sum().sum())

print("\nIdentificadores duplicados:")
print(resultados_finais_2025["id_sinistro"].duplicated().sum())

print("\nDistribuição da variável real:")
print(resultados_finais_2025["fraude"].value_counts())

# COMMAND ----------



# COMMAND ----------

