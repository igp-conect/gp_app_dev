import streamlit as st
import pandas as pd
from datetime import date
import unicodedata

def normalize_string(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ASCII", "ignore").decode("utf-8").lower()

@st.cache_data
def carregar_dados_membros():
    df = pd.read_csv(
        "data/membros_gp/tratados/membros_gp_tratados_.csv",
        dtype={"MATRÍCULA": str, "ANO": str}
    )
    df["DATA NASCIMENTO"] = pd.to_datetime(df["DATA NASCIMENTO"], errors="coerce")  # 👈 Adiciona isso
    return df


def cadastrar_membro():
    @st.dialog("➕ Cadastro de Novo Membro")
    def modal():
        with st.form("form_membro"):
            col1, col2 = st.columns(2)

            with col1:
                nome = st.text_input("Nome Completo")
                cpf = st.text_input("CPF")
                email = st.text_input("Email")
                contato = st.text_input("Contato")
                nascimento = st.date_input("Data de Nascimento", format="DD/MM/YYYY", min_value=date(1900, 1, 1), max_value=date.today())
                equipe = st.text_input("Equipe de Projeto")
                orientador = st.text_input("Orientador")
                curso = st.text_input("Curso")

            with col2:
                lattes = st.text_input("Currículo Lattes")
                matricula = st.text_input("Matrícula")
                camiseta = st.selectbox("Tamanho Camiseta", ["P", "M", "G", "GG"])
                serie = st.text_input("Série")
                ano = st.text_input("Ano")
                escolaridade = st.selectbox("Escolaridade", ["Ensino Médio", "Técnico", "Superior", "Pós-Graduação"])
                status_curso = st.selectbox("Status do Curso", ["Cursando", "Trancado", "Concluído"])

            st.markdown("#### Áreas de Interesse")
            interesses_selecionados = []
            areas_predefinidas = [
                "Programação", "Robótica", "Inteligência Artificial", "Banco de Dados",
                "Desenvolvimento Web", "Redes de Computadores", "Manutenção de Computador",
                "Segurança da Informação", "Design Gráfico", "Análise de Dados",
                "Automação", "IoT (Internet das Coisas)", "Engenharia de Software",
                "Computação em Nuvem", "Eletrônica Digital"
            ]
            cols = st.columns(3)
            for i, area in enumerate(areas_predefinidas):
                if cols[i % 3].checkbox(area):
                    interesses_selecionados.append(area)

            interesses = ", ".join(interesses_selecionados)

            col4, col5, col6 = st.columns(3)
            with col4:
                rank_gp = st.selectbox("Rank GP", ["E", "D", "C", "B", "A", "S"])
            with col5:
                tipo_membro = st.selectbox("Tipo de Membro", ["Discente", "Professor"])
            with col6:
                status = st.selectbox("Status", ["Ativo", "Inativo", "Pendente"])

            enviar = st.form_submit_button("Salvar Membro")
            if enviar:
                st.success("✅ Membro salvo (simulado, sem persistência por enquanto)!")
                st.rerun()

    modal()


def mostrar_indicadores(df):
    st.markdown("### 📊 Indicadores Gerais")

    total_ativos = df[df["STATUS"] == "Ativo"].shape[0]
    total_inativos = df[df["STATUS"] == "Inativo"].shape[0]
    total_equipes = df["EQUIPE DE PROJETO"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Ativos", total_ativos, border=True)
    col2.metric("🔴 Inativos", total_inativos, border=True)
    col3.metric("👥 Total de Equipes", total_equipes, border=True)

def gestao_membros():
    st.markdown("# 🧑‍🤝‍🧑 Lista de Membros do GP Mecatrônica")

    if st.button("➕ Cadastrar Novo Membro"):
        cadastrar_membro()

    try:
        df_original = carregar_dados_membros()
        df = df_original.copy()

        st.sidebar.markdown("### 🔍 Filtros")
        ano = st.sidebar.selectbox("📅 Ano:", ["Todos"] + sorted(df["ANO"].dropna().unique().tolist()))
        tipo = st.sidebar.selectbox("👤 Tipo de Membro:", ["Todos"] + sorted(df["TIPO MEMBRO"].dropna().unique().tolist()))
        serie = st.sidebar.selectbox("📚 Série:", ["Todas"] + sorted(df["SÉRIE"].dropna().unique().tolist()))
        curso = st.sidebar.selectbox("🎓 Curso:", ["Todos"] + sorted(df["CURSO"].dropna().unique().tolist()))
        equipe = st.sidebar.selectbox("👥 Equipe de Projeto:", ["Todas"] + sorted(df["EQUIPE DE PROJETO"].dropna().unique().tolist()))
        orientador = st.sidebar.selectbox("🧑‍🏫 Orientador:", ["Todos"] + sorted(df["ORIENTADOR"].dropna().unique().tolist()))

        if ano != "Todos": df = df[df["ANO"] == ano]
        if tipo != "Todos": df = df[df["TIPO MEMBRO"] == tipo]
        if serie != "Todas": df = df[df["SÉRIE"] == serie]
        if curso != "Todos": df = df[df["CURSO"] == curso]
        if equipe != "Todas": df = df[df["EQUIPE DE PROJETO"] == equipe]
        if orientador != "Todos": df = df[df["ORIENTADOR"] == orientador]

        termo_busca = st.text_input("🔎 Buscar por nome, CPF, e-mail ou orientador:", "")
        if termo_busca:
            termo_busca_normalizado = normalize_string(termo_busca)
            df = df[df.apply(
                lambda row: any(termo_busca_normalizado in normalize_string(val) for val in [
                    row.get("NOME", ""),
                    row.get("CPF", ""),
                    row.get("EMAIL", ""),
                    row.get("ORIENTADOR", "")
                ]), axis=1
            )]

        mostrar_indicadores(df)

        abas = st.tabs(["Todos", "Ativo", "Inativo", "Pendente"])
        status_map = {
            "Todos": None,
            "Ativo": "Ativo",
            "Inativo": "Inativo",
            "Pendente": "Pendente"
        }

        for i, nome_tab in enumerate(status_map.keys()):
            with abas[i]:
                df_filtro = df
                status = status_map[nome_tab]
                if status:
                    df_filtro = df[df["STATUS"] == status]

                st.data_editor(
                    df_filtro,
                    use_container_width=True,
                    num_rows="fixed",
                    hide_index=True,
                    column_config={
                        #"DATA CADASTRO": st.column_config.DateColumn("Data Cadastro", format="DD/MM/YYYY HH:mm:ss"),
                        "NOME": st.column_config.TextColumn("Nome Completo"),
                        "CPF": st.column_config.TextColumn("CPF", disabled=True),
                        "EMAIL": st.column_config.TextColumn("Email"),
                        "CONTATO": st.column_config.TextColumn("Telefone"),
                        "LATTES": st.column_config.LinkColumn("Currículo Lattes"),
                        "MATRÍCULA": st.column_config.TextColumn("Matrícula"),
                        "TAMANHO CAMISETA": st.column_config.SelectboxColumn("Camiseta", options=["P", "M", "G", "GG"]),
                         "DATA NASCIMENTO": st.column_config.DateColumn("Nascimento", format="DD/MM/YYYY" ),
                        "EQUIPE DE PROJETO": st.column_config.TextColumn("Equipe"),
                        "ORIENTADOR": st.column_config.TextColumn("Orientador"),
                        "SÉRIE": st.column_config.TextColumn("Série"),
                        "ANO": st.column_config.TextColumn("Ano"),
                        "NÍVEL ESCOLARIDADE": st.column_config.SelectboxColumn("Escolaridade", options=["Ensino médio", "Graduação", "Pós-Graduação"]),
                        "CURSO": st.column_config.TextColumn("Curso"),
                        "STATUS CURSO": st.column_config.SelectboxColumn("Status Curso", options=["Cursando", "Trancado", "Concluído"]),
                        "ÁREAS DE INTERESSE": st.column_config.TextColumn("Interesses"),
                        "TIPO MEMBRO": st.column_config.SelectboxColumn("Tipo Membro", options=["Discente", "Professor"]),
                        "Rank GP": st.column_config.TextColumn("Rank GP"),
                        "STATUS": st.column_config.SelectboxColumn("Status", options=["Ativo", "Inativo", "Pendente"]),
                    },
                    key=f"editor_{nome_tab}"
                )

        st.markdown("---")
        st.caption(f"📌 Desenvolvido por: Equipe Vingadores --- GP Mecatrônica - IFRO Calama • {date.today().year}")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
