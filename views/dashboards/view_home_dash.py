import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.firebase_utils import init_firestore

db = init_firestore()

def dash_home():
    # ---------- Estilo CSS ----------
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

    # ---------- Sidebar ----------
    st.sidebar.image("assets/images/logo_gtd.png", use_container_width=True)
    st.sidebar.header("Teste:")
    st.sidebar.multiselect("Região", ["Norte", "Sul", "Centro-Oeste", "Sudeste", "Nordeste"], default=["Norte"])
    st.sidebar.selectbox("Ano", ["2022", "2023", "2024"])
    st.sidebar.selectbox("Tipo de Investimento", ["Privado", "Público", "Misto"])
    st.sidebar.markdown("---")
    st.sidebar.button("Main Menu")
    st.sidebar.button("Home", use_container_width=True)

    # ---------- Header ----------
    st.markdown("**📁 Base de Dados: Atualizada ✅**")
    st.markdown("### 📊 Indicadores Gerais")
    st.markdown("---")

    # ---------- Cards ----------
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💰 Projetos", "R$ 2.482 Bi", border=True)
    col2.metric("📌 Tarefas Diversas", "847.300", border=True)
    col3.metric("📈 Processos Sei", "R$ 4.96 Mi", border=True)
    col4.metric("🏦 Demandas Portal Cidadão", "R$ 2.59 Mi", border=True)
    col5.metric("⭐ Demandas Alpha", "3.5K", border=True)

    st.markdown("---")

    # ---------- Gráficos (dados fictícios) ----------
    df_estado = pd.DataFrame({
        'Estado': ['AC', 'AM', 'RO', 'PA', 'RR', 'TO', 'AP'],
        'Investimento': [150, 300, 220, 500, 120, 80, 60]
    })

    df_tipo = pd.DataFrame({
        'Tipo': ['Indústria', 'Agronegócio', 'Tecnologia', 'Energia', 'Comércio'],
        'Valor': [210, 180, 160, 120, 100]
    })

    df_pizza = pd.DataFrame({
        'Região': ['Norte', 'Nordeste', 'Sul', 'Sudeste', 'Centro-Oeste'],
        'Percentual': [25, 20, 18, 22, 15]
    })

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 Investimento por Estado")
        fig1 = px.line(df_estado, x='Estado', y='Investimento', markers=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🏭 Investimento por Tipo de Negócio")
        fig2 = px.bar(df_tipo, x='Valor', y='Tipo', orientation='h')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🌎 Distribuição por Região")
    fig3 = px.pie(df_pizza, values='Percentual', names='Região', hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

    # ---------- Rodapé ----------
    st.markdown("---")
    ano_atual = datetime.now().year
    st.caption(f"📌 Desenvolvido por: Gerência de Transformação Digital GTD-Setic • {ano_atual} | Todos os direitos reservados")