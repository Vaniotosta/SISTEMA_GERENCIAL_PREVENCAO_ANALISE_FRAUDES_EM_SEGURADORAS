import streamlit as st
import pandas as pd
import mlflow.sklearn
from pathlib import Path

# ============================================================
# 1. CONFIGURAÇÃO GERAL
# ============================================================

st.set_page_config(
    page_title="Central de Inteligência de Sinistros",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_LR_PATH = BASE_DIR / "models" / "regressao_logistica"
MODEL_RF_PATH = BASE_DIR / "models" / "random_forest"

THRESHOLD_LR = 0.50
THRESHOLD_RF = 0.25

# ============================================================
# 2. RESULTADOS REAIS DA AVALIAÇÃO DE 2025
# ============================================================

TOTAL_SINISTROS = 20000
TOTAL_FRAUDES = 1352
TOTAL_NAO_FRAUDES = 18648
TAXA_FRAUDE = 6.76

metricas = pd.DataFrame({
    "Modelo": ["Regressão Logística", "Random Forest"],
    "Acurácia": [0.6924, 0.7756],
    "Precisão": [0.1432, 0.1764],
    "Recall": [0.6618, 0.5819],
    "F1-score": [0.2355, 0.2708],
    "ROC-AUC": [0.7631, 0.7462],
    "PR-AUC": [0.2244, 0.1954]
})

resultados = pd.DataFrame({
    "Modelo": ["Regressão Logística", "Random Forest"],
    "Verdadeiros positivos": [315, 277],
    "Falsos positivos": [1884, 1293],
    "Verdadeiros negativos": [4289, 4880],
    "Falsos negativos": [161, 199],
    "Alertas gerados": [2199, 1570]
})

# ============================================================
# 3. IDENTIDADE VISUAL
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #F3F6FA;
}

header[data-testid="stHeader"] {
    background-color: #F3F6FA;
}

[data-testid="stSidebar"] {
    background-color: #10243A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #DCE6F1;
}

.main-title {
    font-size: 43px;
    font-weight: 800;
    color: #10243A;
    letter-spacing: -1.2px;
    line-height: 1.15;
    margin-bottom: 5px;
}

.main-subtitle {
    font-size: 16px;
    color: #64748B;
    margin-bottom: 18px;
}

.section-title {
    color: #10243A;
    font-size: 23px;
    font-weight: 700;
    margin-top: 15px;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E1E8F0;
    padding: 17px;
    border-radius: 12px;
    box-shadow: 0 2px 5px rgba(16,36,58,0.04);
}

div[data-testid="stMetricLabel"] {
    color: #64748B;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #10243A;
    font-weight: 750;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #174A78;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background-color: #23669F;
    color: white;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# 4. CABEÇALHO
# ============================================================

st.markdown(
    '<div class="main-title">CENTRAL DE INTELIGÊNCIA DE SINISTROS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Prevenção de fraudes | Análise preditiva | Apoio à decisão'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# 5. CARREGAMENTO DOS MODELOS
# ============================================================

@st.cache_resource
def carregar_modelos():

    modelo_lr = mlflow.sklearn.load_model(
        str(MODEL_LR_PATH)
    )

    modelo_rf = mlflow.sklearn.load_model(
        str(MODEL_RF_PATH)
    )

    return modelo_lr, modelo_rf


# ============================================================
# 6. HISTÓRICO DA SESSÃO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico = []


# ============================================================
# 7. MENU LATERAL
# ============================================================

st.sidebar.markdown(
    """
    <div style="padding: 15px 0 20px 0;">
        <div style="font-size: 34px;">🛡️</div>
        <div style="font-size: 19px; font-weight: 800;">
            INTELIGÊNCIA
        </div>
        <div style="font-size: 12px; color: #B8C9D9;">
            PREVENÇÃO DE FRAUDES
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.markdown("### NAVEGAÇÃO")

pagina = st.sidebar.radio(
    "Selecione uma área:",
    [
        "Visão Geral",
        "Análise de Sinistros",
        "Comparação de Modelos",
        "Relatórios"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    **TECNOLOGIAS**

    Python  
    Scikit-learn  
    MLflow  
    Streamlit
    """
)

st.sidebar.divider()

st.sidebar.caption(
    "Projeto de inteligência analítica aplicada ao mercado segurador."
)


# ============================================================
# 8. VISÃO GERAL
# ============================================================

if pagina == "Visão Geral":

    st.markdown(
        '<div class="section-title">Painel Executivo</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Indicadores da base de dados e desempenho dos modelos "
        "de prevenção de fraudes."
    )

    # --------------------------------------------------------
    # INDICADORES PRINCIPAIS
    # --------------------------------------------------------

    st.markdown("### Indicadores da base")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Sinistros analisados",
            f"{TOTAL_SINISTROS:,}".replace(",", ".")
        )

    with c2:
        st.metric(
            "Sinistros fraudulentos",
            f"{TOTAL_FRAUDES:,}".replace(",", ".")
        )

    with c3:
        st.metric(
            "Taxa de fraude",
            f"{TAXA_FRAUDE:.2f}%"
        )

    with c4:
        st.metric(
            "Modelos desenvolvidos",
            "2"
        )

    st.divider()

    # --------------------------------------------------------
    # DISTRIBUIÇÃO DOS SINISTROS
    # --------------------------------------------------------

    st.markdown("### Distribuição dos sinistros")

    col1, col2 = st.columns([1, 1])

    with col1:

        distribuicao = pd.DataFrame({
            "Classificação": [
                "Não fraudulentos",
                "Fraudulentos"
            ],
            "Quantidade": [
                TOTAL_NAO_FRAUDES,
                TOTAL_FRAUDES
            ]
        })

        st.bar_chart(
            distribuicao.set_index("Classificação"),
            color="#23669F",
            horizontal=True
        )

    with col2:

        st.markdown("#### Composição da base")

        st.metric(
            "Sinistros não fraudulentos",
            "18.648",
            "93,24% da base"
        )

        st.metric(
            "Sinistros fraudulentos",
            "1.352",
            "6,76% da base"
        )

        st.caption(
            "Base experimental utilizada no desenvolvimento "
            "e avaliação dos modelos."
        )

    st.divider()

    # --------------------------------------------------------
    # DESEMPENHO DOS MODELOS
    # --------------------------------------------------------

    st.markdown("### Desempenho preditivo e apoio à decisão")

    st.write(
        "Avaliação dos modelos no conjunto de teste de 2025, "
        "considerando a capacidade de identificar fraudes, "
        "o volume de alertas e a exposição financeira."
    )

    # Indicadores operacionais dos modelos
    comparativo = pd.DataFrame({
        "Indicador": [
            "Taxa de acerto",
            "Fraudes identificadas",
            "Alertas para investigação",
            "Fraudes não identificadas",
            "Exposição não identificada"
        ],
        "Regressão Logística": [
            "69,24%",
            "315",
            "2.199",
            "161",
            "R$ 2,94 milhões"
        ],
        "Random Forest": [
            "77,56%",
            "277",
            "1.570",
            "199",
            "R$ 3,95 milhões"
        ]
    })

    st.markdown("#### Comparativo operacional")

    st.dataframe(
        comparativo,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### Capacidade de identificação de fraudes")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Regressão Logística",
            "315 fraudes",
            "66,18% das fraudes identificadas"
        )

    with col2:
        st.metric(
            "Random Forest",
            "277 fraudes",
            "58,19% das fraudes identificadas"
        )

    st.markdown("#### Volume de alertas para investigação")

    alertas = pd.DataFrame({
        "Modelo": ["Regressão Logística", "Random Forest"],
        "Alertas": [2199, 1570]
    }).set_index("Modelo")

    st.bar_chart(
        alertas,
        horizontal=True,
        color="#174A78"
    )

    st.markdown("#### Exposição financeira não identificada")

    exposicao = pd.DataFrame({
        "Modelo": ["Regressão Logística", "Random Forest"],
        "Exposição (R$ milhões)": [2.94, 3.95]
    }).set_index("Modelo")

    st.bar_chart(
        exposicao,
        horizontal=True,
        color="#D69E36"
    )

    st.info(
        "**Análise gerencial:** A Regressão Logística identificou "
        "38 fraudes a mais e apresentou aproximadamente R$ 1,02 milhão "
        "a menos de exposição financeira não identificada. "
        "Em contrapartida, gerou 629 alertas adicionais para investigação. "
        "O Random Forest apresentou maior taxa de acerto e menor volume "
        "de alertas."
    )

    st.markdown("#### Recomendação para tomada de decisão")

    st.write(
        "**Regressão Logística:** mais indicada quando a prioridade "
        "é ampliar a identificação de fraudes e reduzir a exposição "
        "financeira não identificada."
    )

    st.write(
        "**Random Forest:** pode ser considerado quando a prioridade "
        "é reduzir o volume de alertas e a demanda operacional de análise."
    )

    st.caption(
        "A taxa de acerto representa a acurácia geral. A exposição "
        "financeira é uma estimativa baseada nos valores dos sinistros "
        "não identificados, não uma perda efetivamente comprovada. "
        "Os resultados não representam garantia de prevenção de fraude."
    )

    st.divider()

    # --------------------------------------------------------
    # ALERTAS E DETECÇÃO
    # --------------------------------------------------------

    st.markdown("### Capacidade de detecção")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### Alertas gerados")

        grafico_alertas = resultados[
            ["Modelo", "Alertas gerados"]
        ].set_index("Modelo")

        st.bar_chart(
            grafico_alertas,
            color="#23669F",
            horizontal=True
        )

    with col2:

        st.markdown("#### Fraudes não detectadas")

        grafico_fraudes = resultados[
            ["Modelo", "Falsos negativos"]
        ].set_index("Modelo")

        st.bar_chart(
            grafico_fraudes,
            color="#C45B54",
            horizontal=True
        )

    st.info(
        "A Regressão Logística identificou 315 fraudes e deixou "
        "161 sem alerta. O Random Forest identificou 277 fraudes "
        "e deixou 199 sem alerta. A escolha depende do equilíbrio "
        "entre capacidade de detecção e volume de investigações."
    )

    st.divider()

    # --------------------------------------------------------
    # IMPACTO ECONÔMICO
    # --------------------------------------------------------

    st.markdown("### Exposição financeira potencial")

    st.write(
        "Estimativa do valor associado aos sinistros fraudulentos "
        "não detectados no conjunto de teste."
    )

    # A variável exposicao já foi criada acima.
    # Aqui usamos uma cópia para construir o gráfico.
    grafico_exposicao = exposicao.copy()

    st.bar_chart(
        grafico_exposicao,
        color="#D69E36",
        horizontal=True
    )

    col1, col2, col3 = st.columns(3)

    diferenca_exposicao = 3951496.83 - 2935123.43

    with col1:
        st.metric(
            "Exposição - Regressão Logística",
            "R$ 2,94 milhões"
        )

    with col2:
        st.metric(
            "Exposição - Random Forest",
            "R$ 3,95 milhões"
        )

    with col3:
        st.metric(
            "Diferença estimada",
            f"R$ {diferenca_exposicao:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

    st.caption(
        "A exposição financeira é uma estimativa baseada nos "
        "valores dos sinistros classificados como falsos negativos. "
        "Não representa perda efetiva, economia comprovada ou "
        "recuperação financeira."
    )

    st.divider()

    # --------------------------------------------------------
    # TABELA DE MÉTRICAS
    # --------------------------------------------------------

    st.markdown("### Resumo comparativo dos modelos")

    tabela_metricas = metricas.copy()

    colunas_percentuais = [
        "Acurácia",
        "Precisão",
        "Recall",
        "F1-score",
        "ROC-AUC",
        "PR-AUC"
    ]

    for coluna in colunas_percentuais:
        tabela_metricas[coluna] = (
            tabela_metricas[coluna] * 100
        ).round(2).astype(str) + "%"

    st.dataframe(
        tabela_metricas,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Fonte: avaliação experimental dos modelos no conjunto "
        "de teste de 2025."
    )


# ============================================================
# 9. ANÁLISE DE SINISTROS
# ============================================================

elif pagina == "Análise de Sinistros":

    st.markdown("## Análise individual de sinistros")

    st.write(
        "Informe as características do segurado, da apólice "
        "e do sinistro para obter uma estimativa de risco."
    )

    with st.form("formulario_sinistro"):

        st.markdown("### 1. Dados do segurado")

        c1, c2, c3 = st.columns(3)

        with c1:

            idade = st.number_input(
                "Idade",
                min_value=18,
                max_value=100,
                value=35
            )

            tempo_cliente = st.number_input(
                "Tempo como cliente (anos)",
                min_value=0.0,
                max_value=100.0,
                value=5.0
            )

        with c2:

            score_credito = st.number_input(
                "Score de crédito",
                min_value=0.0,
                max_value=1000.0,
                value=650.0
            )

            estado_civil = st.selectbox(
                "Estado civil",
                [
                    "Casado",
                    "Divorciado",
                    "Solteiro",
                    "Viúvo",
                    "não informado"
                ]
            )

        with c3:

            renda_mensal = st.number_input(
                "Renda mensal (R$)",
                min_value=0.0,
                value=5000.0
            )

        st.divider()

        st.markdown("### 2. Dados da apólice")

        c1, c2, c3 = st.columns(3)

        with c1:

            tipo_cobertura = st.selectbox(
                "Tipo de cobertura",
                [
                    "básica",
                    "colisão",
                    "compreensiva",
                    "roubo e furto"
                ]
            )

            valor_segurado = st.number_input(
                "Valor segurado (R$)",
                min_value=0.0,
                value=50000.0
            )

        with c2:

            franquia = st.number_input(
                "Franquia (R$)",
                min_value=0.0,
                value=3000.0
            )

            premio_anual = st.number_input(
                "Prêmio anual (R$)",
                min_value=0.0,
                value=3000.0
            )

        with c3:

            canal_venda = st.selectbox(
                "Canal de venda",
                [
                    "Agência",
                    "Corretor",
                    "Online",
                    "Telefone",
                    "não informado"
                ]
            )

            alteracoes = st.number_input(
                "Alterações na apólice nos últimos 90 dias",
                min_value=0,
                max_value=100,
                value=0
            )

        st.divider()

        st.markdown("### 3. Dados do sinistro")

        c1, c2, c3 = st.columns(3)

        with c1:

            tipo_sinistro = st.selectbox(
                "Tipo de sinistro",
                [
                    "colisão",
                    "danos naturais",
                    "furto",
                    "incêndio",
                    "roubo"
                ]
            )

            hora_sinistro = st.number_input(
                "Hora do sinistro",
                min_value=0,
                max_value=23,
                value=12
            )

            uf = st.selectbox(
                "UF",
                ["BA", "MG", "PE", "PR", "RJ", "RS", "SC", "SP"]
            )

        with c2:

            boletim = st.selectbox(
                "Boletim de ocorrência",
                ["Sim", "Não"]
            )

            testemunhas = st.number_input(
                "Quantidade de testemunhas",
                min_value=0,
                max_value=100,
                value=1
            )

            vitima = st.selectbox(
                "Houve vítima?",
                ["Sim", "Não"]
            )

        with c3:

            oficina = st.selectbox(
                "Oficina credenciada?",
                ["Sim", "Não", "não informado"]
            )

            valor_sinistro = st.number_input(
                "Valor do sinistro (R$)",
                min_value=0.0,
                value=15000.0
            )

        st.divider()

        st.markdown("### 4. Informações temporais")

        c1, c2, c3 = st.columns(3)

        with c1:

            dias_aviso = st.number_input(
                "Dias entre sinistro e aviso",
                min_value=0,
                max_value=365,
                value=2
            )

        with c2:

            mes_sinistro = st.selectbox(
                "Mês do sinistro",
                list(range(1, 13))
            )

        with c3:

            dia_semana = st.selectbox(
                "Dia da semana (0 a 6)",
                list(range(0, 7))
            )

        enviar = st.form_submit_button(
            "Analisar sinistro",
            type="primary",
            use_container_width=True
        )

    if enviar:

        dados = {
            "idade": idade,
            "tempo_cliente_anos": tempo_cliente,
            "score_credito": score_credito,
            "estado_civil": estado_civil,
            "renda_mensal": renda_mensal,
            "tipo_cobertura": tipo_cobertura,
            "valor_segurado": valor_segurado,
            "franquia": franquia,
            "premio_anual": premio_anual,
            "canal_venda": canal_venda,
            "alteracoes_apolice_90d": alteracoes,
            "tipo_sinistro": tipo_sinistro,
            "hora_sinistro": hora_sinistro,
            "uf": uf,
            "boletim_ocorrencia": boletim,
            "qtd_testemunhas": testemunhas,
            "houve_vitima": vitima,
            "oficina_credenciada": oficina,
            "valor_sinistro_num": valor_sinistro,
            "dias_ate_aviso": dias_aviso,
            "mes_sinistro": mes_sinistro,
            "dia_semana_sinistro": dia_semana
        }

        colunas = [
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

        entrada = pd.DataFrame(
            [dados],
            columns=colunas
        )

        try:

            with st.spinner(
                "Carregando modelos e analisando sinistro..."
            ):

                modelo_lr, modelo_rf = carregar_modelos()

                prob_lr = modelo_lr.predict_proba(
                    entrada
                )[0][1]

                prob_rf = modelo_rf.predict_proba(
                    entrada
                )[0][1]

                classe_lr = int(prob_lr >= THRESHOLD_LR)
                classe_rf = int(prob_rf >= THRESHOLD_RF)

            resultado = {
                "prob_lr": float(prob_lr),
                "prob_rf": float(prob_rf),
                "classe_lr": classe_lr,
                "classe_rf": classe_rf
            }

            st.session_state.historico.append(resultado)

            st.success("Análise concluída!")

            st.markdown("### Resultado da análise")

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Regressão Logística",
                    f"{prob_lr:.1%}",
                    "Alerta de fraude" if classe_lr else "Sem alerta"
                )

                st.caption("Limiar de classificação: 50%")

            with c2:

                st.metric(
                    "Random Forest",
                    f"{prob_rf:.1%}",
                    "Alerta de fraude" if classe_rf else "Sem alerta"
                )

                st.caption("Limiar de classificação: 25%")

            if classe_lr == 1 or classe_rf == 1:

                st.warning(
                    "Pelo menos um modelo identificou um alerta. "
                    "Recomenda-se análise humana complementar."
                )

            else:

                st.info(
                    "Nenhum dos modelos ultrapassou seu respectivo "
                    "limiar de classificação."
                )

            st.caption(
                "As probabilidades são estimativas dos modelos. "
                "Um alerta não confirma a ocorrência de fraude."
            )

        except Exception as erro:

            st.error(
                f"Erro durante a análise: {erro}"
            )


# ============================================================
# 10. COMPARAÇÃO DE MODELOS
# ============================================================

elif pagina == "Comparação de Modelos":

    st.markdown("## Comparação dos modelos")

    st.write(
        "Comparação dos resultados produzidos pelos dois modelos "
        "no conjunto de teste de 2025."
    )

    st.markdown("### Métricas de desempenho")

    st.dataframe(
        metricas,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Matriz de resultados")

    st.dataframe(
        resultados,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Exposição financeira estimada")

    st.dataframe(
        exposicao,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "A Regressão Logística apresentou maior recall, enquanto "
        "o Random Forest apresentou maior precisão e F1-score. "
        "A seleção do modelo deve considerar os custos de falsos "
        "positivos e falsos negativos."
    )

    if st.session_state.historico:

        st.divider()

        st.markdown("### Comparação das análises desta sessão")

        historico = pd.DataFrame(
            st.session_state.historico
        )

        st.dataframe(
            historico,
            use_container_width=True
        )

    else:

        st.info(
            "Realize uma análise individual para comparar "
            "as previsões produzidas nesta sessão."
        )


# ============================================================
# 11. RELATÓRIOS
# ============================================================

elif pagina == "Relatórios":

    st.markdown("## Relatórios de análise")

    if st.session_state.historico:

        relatorio = pd.DataFrame(
            st.session_state.historico
        )

        st.markdown("### Histórico de sinistros analisados")

        st.dataframe(
            relatorio,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Quantidade de análises nesta sessão",
            len(relatorio)
        )

        arquivo = relatorio.to_csv(
            index=False,
            sep=";",
            decimal=","
        ).encode("utf-8-sig")

        st.download_button(
            "Baixar relatório CSV",
            data=arquivo,
            file_name="relatorio_analises_fraudes.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        st.info(
            "Ainda não existem análises nesta sessão. "
            "Acesse Análise de Sinistros para iniciar."
        )


# ============================================================
# 12. RODAPÉ
# ============================================================

st.divider()

st.caption(
    "CENTRAL DE INTELIGÊNCIA DE SINISTROS | "
    "Machine Learning | Scikit-learn | MLflow | Streamlit"
)

st.caption(
    "Projeto experimental de apoio à decisão. "
    "As previsões não substituem a investigação humana."
)