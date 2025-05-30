import streamlit as st
from views.dashboards.view_home_dash import dash_home

###################### CONFIGURAÇÃO DA PÁGINA ######################
st.set_page_config(
    page_title="GP MECATRÔNICA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

###################### LOGO ######################
st.logo(
    image="assets/images/logo_gp/gp_ico.png",
    size="large",
    link=None,
    icon_image=None,
)

###################### TÍTULO ######################
st.title("📋 Gestão Interna GP MECATRÔNICA")

###################### MENU LATERAL ######################
menu = st.sidebar.selectbox(
    "📋 Navegação",
    options=[
        "🏠 Dashboard",
        "🪪 Gestão de Membros",
        "👩‍💻 Gestão de Projetos",
        "🙏🏻 Gestão de Equipes",
        "📦 Gestão de patrimônios",
        "🥳 Gestão Aniversariantes",
        "👩‍🚀 Usuários Sistema",
        "⚡ APIS",
        "🔐 Segurança",
        "📊 Relatórios",
        "📚 Documentação",
        "⚙️ Gerenciar"
    ]
)

###################### ROTEAMENTO ######################
if menu == "🏠 Dashboard":
    dash_home()

