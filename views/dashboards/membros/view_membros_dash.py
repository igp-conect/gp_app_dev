import streamlit as st
import pandas as pd
from datetime import date
import uuid
import unicodedata

def normalize_string(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ASCII", "ignore").decode("utf-8").lower()

def gerar_dados_ficticios():
    return pd.DataFrame([
        {
            "ID": str(uuid.uuid4()),
            "NOME": "Ana Paula Mendes",
            "IMAGEM_USUÁRIO": "https://i.pravatar.cc/150?img=1",
            "CPF": "123.456.789-00",
            "EMAIL": "ana.mendes@ifro.edu.br",
            "CONTATO": "(69) 99999-1234",
            "LATTES": "http://lattes.cnpq.br/ana123",
            "MATRÍCULA": "20211002001",
            "TAMANHO CAMISETA": "M",
            "DATA NASCIMENTO": date(2005, 8, 14),
            "EQUIPE DE PROJETO": "Robótica",
            "ORIENTADOR": "Prof. Carlos Lima",
            "SÉRIE": "3º Ano",
            "ANO": "2025",
            "NÍVEL ESCOLARIDADE": "Ensino Médio",
            "CURSO": "Informática",
            "STATUS CURSO": "Cursando",
            "ÁREAS DE INTERESSE": "IA, Robótica, WebDev",
            "TIPO MEMBRO": "Discente",
            "NÍVEL GP": "Avançado",
            "STATUS": "Ativo"
        },
        {
            "ID": str(uuid.uuid4()),
            "NOME": "João Victor Silva",
            "IMAGEM_USUÁRIO": "https://i.pravatar.cc/150?img=2",
            "CPF": "987.654.321-00",
            "EMAIL": "joao.silva@ifro.edu.br",
            "CONTATO": "(69) 99999-4321",
            "LATTES": "http://lattes.cnpq.br/joao321",
            "MATRÍCULA": "20211002005",
            "TAMANHO CAMISETA": "G",
            "DATA NASCIMENTO": date(2006, 3, 21),
            "EQUIPE DE PROJETO": "Automatização",
            "ORIENTADOR": "Profa. Juliana Torres",
            "SÉRIE": "2º Ano",
            "ANO": "2025",
            "NÍVEL ESCOLARIDADE": "Ensino Médio",
            "CURSO": "Mecatrônica",
            "STATUS CURSO": "Trancado",
            "ÁREAS DE INTERESSE": "Sistemas embarcados, IA",
            "TIPO MEMBRO": "Discente",
            "NÍVEL GP": "Intermediário",
            "STATUS": "Inativo"
        }
    ])

def mostrar_indicadores(df):
    st.markdown("### 📊 Indicadores Gerais")
    ativos = df[df["STATUS"] == "Ativo"].shape[0]
    inativos = df[df["STATUS"] == "Inativo"].shape[0]
    pendentes = df[df["STATUS"] == "Pendente"].shape[0]
    professores = df[df["TIPO MEMBRO"] == "Professor"].shape[0]
    orientadores = df["ORIENTADOR"].nunique()
    equipes = df["EQUIPE DE PROJETO"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Ativos", ativos, border=True)
    col2.metric("🔴 Inativos", inativos, border=True)
    col3.metric("🟡 Pendentes", pendentes, border=True)

    col4, col5, col6 = st.columns(3)
    col4.metric("👨‍🏫 Total Professores", professores, border=True)
    col5.metric("📘 Total Orientadores", orientadores, border=True)
    col6.metric("👥 Total Equipes", equipes, border=True)

def cadastrar_membro():
    @st.dialog("➕ Cadastro de Membro")
    def modal():
        with st.form("form_membro"):
            foto = st.file_uploader("Foto de Perfil", type=["jpg", "jpeg", "png"])
            nome = st.text_input("Nome Completo")
            cpf = st.text_input("CPF")
            email = st.text_input("Email")
            contato = st.text_input("Contato")
            lattes = st.text_input("Currículo Lattes")
            matricula = st.text_input("Matrícula")
            camiseta = st.selectbox("Tamanho Camiseta", ["P", "M", "G", "GG"])
            nascimento = st.date_input("Data de Nascimento")
            equipe = st.text_input("Equipe de Projeto")
            orientador = st.text_input("Orientador")
            serie = st.text_input("Série")
            ano = st.text_input("Ano")
            escolaridade = st.selectbox("Escolaridade", ["Ensino Médio", "Técnico", "Superior"])
            curso = st.text_input("Curso")
            status_curso = st.selectbox("Status do Curso", ["Cursando", "Trancado", "Concluído"])
            interesses = st.text_area("Áreas de Interesse")
            tipo_membro = st.selectbox("Tipo de Membro", ["Discente", "Professor"]) 
            nivel_gp = st.selectbox("Nível no GP", ["Iniciante", "Intermediário", "Avançado"])
            status = st.selectbox("Status", ["Ativo", "Inativo", "Pendente"])

            enviar = st.form_submit_button("Salvar Membro")
            if enviar:
                st.success("✅ Membro salvo (simulado, sem persistência por enquanto)!")
                st.rerun()

    modal()

def gestao_membros():
    st.markdown("# 🧑‍🤝‍🧑 Lista de Membros do GP Mecatrônica")

    try:
        df_original = gerar_dados_ficticios()
        df = df_original.copy()

        if st.button("➕ Cadastrar Novo Membro"):
            cadastrar_membro()

        # Filtros laterais
        st.sidebar.markdown("### 🔍 Filtros")
        ano = st.sidebar.selectbox("📅 Ano:", options=["Todos"] + sorted(df_original["ANO"].dropna().unique().tolist()))
        tipo = st.sidebar.selectbox("👤 Tipo de Membro:", options=["Todos"] + sorted(df_original["TIPO MEMBRO"].dropna().unique().tolist()))
        serie = st.sidebar.selectbox("📘 Série:", options=["Todas"] + sorted(df_original["SÉRIE"].dropna().unique().tolist()))
        curso = st.sidebar.selectbox("🎓 Curso:", options=["Todos"] + sorted(df_original["CURSO"].dropna().unique().tolist()))
        equipe = st.sidebar.selectbox("👥 Equipe de Projeto:", options=["Todas"] + sorted(df_original["EQUIPE DE PROJETO"].dropna().unique().tolist()))
        orientador = st.sidebar.selectbox("🧑‍🏫 Orientador:", options=["Todos"] + sorted(df_original["ORIENTADOR"].dropna().unique().tolist()))

        if ano != "Todos": df = df[df["ANO"] == ano]
        if tipo != "Todos": df = df[df["TIPO MEMBRO"] == tipo]
        if serie != "Todas": df = df[df["SÉRIE"] == serie]
        if curso != "Todos": df = df[df["CURSO"] == curso]
        if equipe != "Todas": df = df[df["EQUIPE DE PROJETO"] == equipe]
        if orientador != "Todos": df = df[df["ORIENTADOR"] == orientador]

        # Campo de busca
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
                        "IMAGEM_USUÁRIO": st.column_config.ImageColumn("Foto"),
                        "NOME": st.column_config.TextColumn("Nome Completo"),
                        "CPF": st.column_config.TextColumn("CPF", disabled=True),
                        "EMAIL": st.column_config.TextColumn("Email"),
                        "CONTATO": st.column_config.TextColumn("Telefone"),
                        "LATTES": st.column_config.LinkColumn("Currículo Lattes"),
                        "MATRÍCULA": st.column_config.TextColumn("Matrícula"),
                        "TAMANHO CAMISETA": st.column_config.SelectboxColumn("Camiseta", options=["P", "M", "G", "GG"]),
                        "DATA NASCIMENTO": st.column_config.DateColumn("Nascimento"),
                        "EQUIPE DE PROJETO": st.column_config.TextColumn("Equipe"),
                        "ORIENTADOR": st.column_config.TextColumn("Orientador"),
                        "SÉRIE": st.column_config.TextColumn("Série"),
                        "ANO": st.column_config.TextColumn("Ano"),
                        "STATUS": st.column_config.SelectboxColumn("Status", options=["Ativo", "Inativo", "Pendente"]),
                        "NÍVEL ESCOLARIDADE": st.column_config.SelectboxColumn("Escolaridade", options=["Ensino Médio", "Técnico", "Superior"]),
                        "CURSO": st.column_config.TextColumn("Curso"),
                        "STATUS CURSO": st.column_config.SelectboxColumn("Status Curso", options=["Cursando", "Trancado", "Concluído"]),
                        "ÁREAS DE INTERESSE": st.column_config.TextColumn("Interesses"),
                        "TIPO MEMBRO": st.column_config.SelectboxColumn("Tipo Membro", options=["Discente", "Professor"]),
                        "NÍVEL GP": st.column_config.SelectboxColumn("Nível GP", options=["Iniciante", "Intermediário", "Avançado"])
                    },
                    key=f"editor_{nome_tab}"
                )

        st.markdown("---")
        st.caption(f"📌 Desenvolvido por: GP Mecatrônica - IFRO Calama • {date.today().year}")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
