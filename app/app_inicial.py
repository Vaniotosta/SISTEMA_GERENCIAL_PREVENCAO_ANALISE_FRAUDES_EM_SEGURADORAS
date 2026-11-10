import streamlit as st
import pandas as pd
import mlflow.sklearn
from pathlib import Path

# =====================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# =====================================================

st.set_page_config(
    page_title="Prevenção de Fraudes em Sinistros",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CAMINHOS DOS MODELOS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_LR_PATH = BASE_DIR / "models" / "regressao_logistica"
MODEL_RF_PATH = BASE_DIR / "models" / "random_forest"

# Limiares definidos durante a validação
THRESHOLD_LR = 0.50
THRESHOLD_RF = 0.25

# =====================================================
# IDENTIDADE VISUAL
# =====================================================

st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FB;
    }

    [data-testid="stSidebar"] {
        background-color: #10243A;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .main-title {
        color: #10243A;
        font-size: 32px;
        font-weight: 700;
    }

    .subtitle {
        color: #64748B;
        font-size: 15px;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# CABEÇALHO
# =====================================================

st.markdown(
    '<p class="main-title">🛡️ Prevenção de Fraudes em Sinistros</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Plataforma de análise preditiva e apoio à decisão em seguros</p>',
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# MENU LATERAL
# =====================================================

st.sidebar.title("NAVEGAÇÃO")

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

st.sidebar.caption("Modelos desenvolvidos com Scikit-learn e MLflow")

# =====================================================
# CARREGAMENTO DOS MODELOS
# =====================================================

@st.cache_resource
def carregar_modelos():

    modelo_lr = mlflow.sklearn.load_model(str(MODEL_LR_PATH))
    modelo_rf = mlflow.sklearn.load_model(str(MODEL_RF_PATH))

    return modelo_lr, modelo_rf


# =====================================================
# PÁGINAS
# =====================================================

if pagina == "Visão Geral":

    st.subheader("Visão Geral")

    st.info(
        "Bem-vindo à plataforma de prevenção de fraudes. "
        "Utilize o menu lateral para acessar as funcionalidades."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Modelos disponíveis", "2")

    with col2:
        st.metric("Regressão Logística", "Ativo")

    with col3:
        st.metric("Random Forest", "Ativo")


elif pagina == "Análise de Sinistros":

    st.subheader("Análise individual de sinistros")

    st.info(
        "Nesta área será possível informar os dados de um sinistro "
        "e obter as previsões dos dois modelos."
    )


elif pagina == "Comparação de Modelos":

    st.subheader("Comparação dos modelos")

    st.info(
        "Nesta área serão apresentadas as probabilidades, "
        "classificações e diferenças entre os modelos."
    )


elif pagina == "Relatórios":

    st.subheader("Relatórios")

    st.info(
        "Nesta área será disponibilizado o histórico de análises "
        "e a exportação dos resultados."
    )

# =====================================================
# RODAPÉ
# =====================================================

st.divider()

st.caption(
    "Projeto de Ciência de Dados | Modelos de Machine Learning "
    "| MLflow | Streamlit"
)