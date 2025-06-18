import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def dash_home():
    st.markdown("""
        <style>
            .main {
                background-color: #111111;
                color: #FFFFFF;
            }
            .css-18e3th9 {
                background-color: #1e1e2f;
            }
            .stButton>button {
                background-color: #fc3c3c;
                color: white;
            }
            .css-1d391kg {
                background-color: #000;
            }
        </style>
    """, unsafe_allow_html=True)

    # ---------- Sidebar com filtros fictícios ----------
    st.sidebar.image("assets/images/logo_gp/gpmecatrônica.png", use_container_width=True)
    st.sidebar.header("Filtros Temporários:")
    st.sidebar.selectbox("Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    st.sidebar.selectbox("Ano", ["2025", "2024", "2023", "2022"], index=2),
                                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], index=2)
    st.sidebar.multiselect("Departamento", ["Pesquisa", "Extensão", "Ensino", "TI"], default=["Pesquisa"])
    st.sidebar.slider("% de Conclusão dos Projetos", 0, 100, (30, 80))
    st.sidebar.markdown("---")
    

    

    # ---------- Título ----------
    st.markdown("### 📊 Painel Geral de Indicadores - GP Mecatrônica")
    st.markdown("---")
    

    # ---------- Cards de Indicadores ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("📅 Membros Ativos", "39", border=True)
    col2.metric("📆 Projetos em Andamento", "9", border=True)
    col3.metric("📄 Itens Patrimoniais", "215", border=True)

    col4, col5, col6 = st.columns(3)
    col4.metric("🎈 Aniversariantes do Mês", "4", border=True)
    col5.metric("🔒 Acessos não autorizados", "1", border=True)
    col6.metric("⬇️ Backups Realizados", "4", border=True)

    st.markdown("---")

    # ---------- Gráficos Fictícios ----------
    df_projetos = pd.DataFrame({
        "Status": ["Em Andamento", "Concluídos", "Atrasados"],
        "Quantidade": [9, 5, 1]
    })

    df_usuarios = pd.DataFrame({
        "Perfil": ["Administrador", "Padrão", "Convidado"],
        "Quantidade": [3, 12, 5]
    })

    df_membros = pd.DataFrame({
        "Status": ["Ativos", "Inativos"],
        "Total": [39, 9]
    })

    col7, col8 = st.columns(2)
    with col7:
        st.subheader("📈 Projetos por Status")
        fig_proj = px.bar(df_projetos, x="Status", y="Quantidade", color="Status")
        st.plotly_chart(fig_proj, use_container_width=True)

    with col8:
        st.subheader("🧑‍💻 Perfis de Usuários")
        fig_user = px.pie(df_usuarios, names="Perfil", values="Quantidade", hole=0.4)
        st.plotly_chart(fig_user, use_container_width=True)

    st.subheader("🤺 Membros Ativos vs Inativos")
    fig_membros = px.pie(df_membros, names="Status", values="Total", hole=0.3)
    st.plotly_chart(fig_membros, use_container_width=True)

    st.markdown("---")
    
    # ---------- Widgets Nativos para Interação Futura ----------
    with st.expander("🔍 Ver Detalhes Técnicos do Sistema"):
        st.text("Versão: 1.0.0-dev\nBackend: Firebase\nFrontend: Streamlit")
        st.checkbox("Ativar modo desenvolvedor")
        st.select_slider("Nível de acesso", options=["Visitante", "Padrão", "Administrador"])
        st.date_input("Data da última atualização")

    # ---------- Rodapé ----------
    st.markdown("---")
    ano_atual = datetime.now().year
    st.caption(f"📌 Desenvolvido por: GP Mecatrônica - IFRO Calama • {ano_atual} ")
