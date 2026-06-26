import streamlit as st
import pandas as pd
import altair as alt

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Portal de Engenharia & Produtividade",
    page_icon="🏗️",
    layout="wide"
)

# ==========================================
# 2. DESIGN E ESTILIZAÇÃO CUSTOMIZADA (CSS)
# ==========================================
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; margin-bottom: 20px; }
    .ficha-tecnica { background-color: #EFF6FF; padding: 20px; border-radius: 8px; border: 1px solid #BFDBFE; }
    .vol-title { font-size: 20px; font-weight: bold; margin-top: 15px; }
    .status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
    .dot-aberta { background-color: #22C55E; }
    .dot-atendimento { background-color: #3B82F6; }
    .dot-pausada { background-color: #EAB308; }
    .dot-fechado { background-color: #EF4444; }
    .vol-number { font-size: 36px; font-weight: bold; margin-top: 5px; }
    div.stButton > button { width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Projetos</div>', unsafe_allow_html=True)

# URL base do Speckle original aprovado
speckle_base_url = "https://speckle.systems"

# ==========================================
# 3. CONTROLE DE NAVEGAÇÃO DE ABAS ATIVAS
# ==========================================
if 'aba_ativa' not in st.session_state:
    st.session_state.aba_ativa = "M1"

# Renderização visual dos seletores de abas no topo da tela
nav_c1, nav_c2, nav_c3 = st.columns(3)
with nav_c1:
    if st.button("📦 Modelo 3D (Speckle)", type="primary" if st.session_state.aba_ativa == "M1" else "secondary"):
        st.session_state.aba_ativa = "M1"
with nav_c2:
    if st.button("📊 Produtividade da Equipe", type="primary" if st.session_state.aba_ativa == "M2" else "secondary"):
        st.session_state.aba_ativa = "M2"
with nav_c3:
    if st.button("🧠 Centro de Diagnóstico (IA)", type="primary" if st.session_state.aba_ativa == "M3" else "secondary"):
        st.session_state.aba_ativa = "M3"

st.write("---")

# ==========================================
# 4. BARRA LATERAL OPERACIONAL (REATIVA POR PÁGINA)
# ==========================================
st.sidebar.header("Filtros de Visão")

# Lógica chave: Se estiver na Aba 1, a barra cinza permanece na tela, mas vazia e limpa.
if st.session_state.aba_ativa == "M1":
    st.sidebar.caption("Visualização de Engenharia Ativa")
    filtro_status = "Todos"
    filtro_criticidade = "Todos"
    filtro_tempo = "Todos"
    arquivo_upload = None
else:
    # Se estiver nas Abas 2 ou 3, o menu completo aprovado é renderizado normalmente
    filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
    filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])
    filtro_tempo = st.sidebar.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"])
    st.sidebar.write("---")
    arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

# Lógica de persistência dos dados carregados
if 'df_global' not in st.session_state:
    st.session_state.df_global = pd.DataFrame()

if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            st.session_state.df_global = pd.read_csv(arquivo_upload)
        else:
            st.session_state.df_global = pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

df = st.session_state.df_global

# Mapeia a lista de OS disponíveis
if not df.empty and 'OS' in df.columns:
    lista_os = sorted(list(df['OS'].dropna().astype(str).unique()))
else:
    lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]

if 'os_selecionada' not in st.session_state or st.session_state.os_selecionada not in lista_os:
    if lista_os:
        st.session_state.os_selecionada = lista_os[0]

# Extração dinâmica de dados técnicos baseados na OS ativa
id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"
resp, setor, status, data_ab = "Pedro", "Climatização", "Fechado", "20/06/2026"
descricao_falha = "Aguardando carregamento dos dados."
criticidade_ativo = "Média"

if not df.empty and 'OS' in df.columns:
    dados_os = df[df['OS'].astype(str) == str(st.session_state.os_selecionada)]
    if not dados_os.empty:
        col_id = next((c for c in df.columns if c.upper() == 'ID'), None)
        if col_id:
            id_bim_alvo = str(dados_os[col_id].values[0]).strip()
        col_t = next((c for c in df.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel']), None)
        resp = str(dados_os[col_t].values[0]) if col_t else "Pedro"
        setor = str(dados_os['Setor'].values[0]) if 'Setor' in df.columns else "Climatização"
        status = str(dados_os['Status'].values[0]) if 'Status' in df.columns else "Fechado"
        data_ab = str(dados_os['Data_Abertura'].values[0]) if 'Data_Abertura' in df.columns else "20/06/2026"
        descricao_falha = str(dados_os['Descrição'].values[0]) if 'Descrição' in df.columns else "Sem descrição."
        criticidade_ativo = str(dados_os['Criticidade'].values[0]) if 'Criticidade' in df.columns else "Média"

if not id_bim_alvo or id_bim_alvo == "nan":
    id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

# ==========================================
# REGRAS DE RENDERIZAÇÃO DAS TELAS
# ==========================================

# MÓDULO 1: MODELO 3D
if st.session_state.aba_active if 'aba_active' in locals() else st.session_state.aba_ativa == "M1":
    st.subheader("Visualizador Operacional de Ativos 3D")
    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecione outra OS na aba Centro de Diagnóstico para focar)")
    st.components.v1.iframe(speckle_base_url, height=600, scrolling=False)

# MÓDULO 2: PRODUTIVIDADE DA EQUIPE
elif st.session_state.aba_ativa == "M2":
    if not df.empty:
        df_filtrado = df.copy()
        if filtro_status != "Todos" and 'Status' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
            
        st.markdown('<div class="vol-title">📊 Volumetria das Ordens de Serviço</div>', unsafe_allow_html=True)
        col_status_name = next((c for c in df.columns if c.lower() == 'status'), None)
        status_counts = df[col_status_name].value_counts() if col_status_name else {}
        
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        with v_col1:
            st.markdown('<div><span class="status-dot dot-aberta"></span>Aberta</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{int(status_counts.get("Aberta", 0))}</div>', unsafe_allow_html=True)
        with v_col2:
            st.markdown('<div><span class="status-dot dot-atendimento"></span>Em Atendimento</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{int(status_counts.get("Em Andamento", 0))}</div>', unsafe_allow_html=True)
        with v_col3:
            st.markdown('<div><span class="status-dot dot-pausada"></span>Pausada</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{int(status_counts.get("Pausada", 0))}</div>', unsafe_allow_html=True)
        with v_col4:
            st.markdown('<div><span class="status-dot dot-fechado"></span>Fechado</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{int(status_counts.get("Fechado", 0))}</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("Controle de Ordens de Serviço por Técnico")
        col_tecnico = next((c for c in df_filtrado.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel', 'técnico responsável']), df_filtrado.columns)
        df_produtividade = df_filtrado.groupby(col_tecnico).size().reset_index(name='Ordens')
        df_produtividade.columns = ['Técnico', 'Ordens']
        
        grafico_altair = alt.Chart(df_produtividade).mark_bar(color='#1f77b4').encode(
            x=alt.X('Técnico:N', title='Profissional Técnico', sort='-y'),
            y=alt.Y('Ordens:Q', title='Total de Ordens de Serviço'),
            tooltip=['Técnico', 'Ordens']
        ).properties(width='container', height=350)
        st.altair_chart(grafico_altair, use_container_width=True)
        
        st.markdown("---")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.info("💡 Por favor, certifique-se de que a planilha está carregada na barra lateral.")

# MÓDULO 3: CENTRO DE DIAGNÓSTICO AVANÇADO
elif st.session_state.aba_ativa == "M3":
    st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.markdown("🔎 **Seleção de Ativo para Auditoria**")
        st.session_state.os_selecionada = st.selectbox(
            "Selecione a OS para análise da IA:", 
            lista_os, 
            index=lista_os.index(st.session_state.os_selecionada) if st.session_state.os_selecionada in lista_os else 0
        )
        
        html_ficha = "<div class='ficha-tecnica'>"
        html_ficha += "<h4 style='margin-top:0; color:#1E3A8A;'>📋 Ficha Técnica do Ativo</h4>"
        html_ficha += "<ul>"
        html_ficha += f"<li><b>Ordem de Serviço:</b> {st.session_state.os_selecionada}</li>"
        html_ficha += f"<li><b>ID BIM:</b> {id_bim_alvo}</li>"
        html_ficha += f"<li><b>Responsável Técnico:</b> {resp}</li>"
        html_ficha += f"<li><b>Setor / Subsistema:</b> {setor}</li>"
