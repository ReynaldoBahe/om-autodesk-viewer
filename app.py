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
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Projetos</div>', unsafe_allow_html=True)

# ==========================================
# 3. RESERVA DE ESPAÇO NA BARRA LATERAL (MENU COMPLETO)
# ==========================================
# Definimos os placeholders globais para gerenciar o conteúdo da faixa cinza lateral
st.sidebar.header("Filtros de Visão")
espaco_filtros_laterais = st.sidebar.empty()
espaco_divisor_lateral = st.sidebar.empty()
espaco_upload_lateral = st.sidebar.empty()

# URL base do Speckle em modo embed limpo original aprovado
speckle_base_url = "https://speckle.systems"

# Inicializa o estado interno para guardar a planilha entre as trocas de abas
if 'dados_planilha_persistidos' not in st.session_state:
    st.session_state.dados_planilha_persistidos = pd.DataFrame()

df = st.session_state.dados_planilha_persistidos

# Mapeia dinamicamente a lista de OS disponíveis
if not df.empty and 'OS' in df.columns:
    lista_os = sorted(list(df['OS'].dropna().unique()))
else:
    lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]

# ==========================================
# 4. CONFIGURAÇÃO DO ESTADO DA SESSÃO (SESSION STATE)
# ==========================================
if 'os_selecionada' not in st.session_state or st.session_state.os_selecionada not in lista_os:
    if lista_os:
        st.session_state.os_selecionada = lista_os[0]

# ==========================================
# 5. CRIAÇÃO DAS ABAS ORIGINAIS (ESTRUTURA INTEGRAL APROVADA)
# ==========================================
aba_modelo, aba_produtividade, aba_diagnostico = st.tabs([
    "📦 Modelo 3D (Speckle)", 
    "📊 Produtividade da Equipe", 
    "🧠 Centro de Diagnóstico (IA)"
])

# Cálculo seguro do ID BIM para todas as abas
id_bim_alvo = ""
if not df.empty and 'OS' in df.columns:
    col_id = next((c for c in df.columns if c.upper() == 'ID'), None)
    if col_id:
        linha_ativo = df[df['OS'] == st.session_state.os_selecionada]
        if not linha_ativo.empty:
            id_bim_alvo = str(linha_ativo[col_id].values[0]).strip()

if not id_bim_alvo or id_bim_alvo == "nan":
    id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

# ==========================================
# ABA 1: MODELO 3D (FAIXA CINZA PRESERVADA E LIMPA)
# ==========================================
with aba_modelo:
    # Esvazia explicitamente os componentes de dentro da barra cinza, mantendo o seu tamanho e menu estruturado
    espaco_filtros_laterais.empty()
    espaco_divisor_lateral.empty()
    espaco_upload_lateral.empty()

    st.subheader("Visualizador Operacional de Ativos 3D")
    
    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecione outra OS na aba Centro de Diagnóstico para focar)")
    
    st.components.v1.iframe(speckle_base_url, height=600, scrolling=False)

# ==========================================
# ABA 2: PRODUTIVIDADE E RELATÓRIO (CÓDIGO ORIGINAL INTOCADO E APROVADO)
# ==========================================
with aba_produtividade:
    # Injeta os seletores clássicos aprovados para preencher a faixa lateral esquerda nesta aba
    with espaco_filtros_laterais.container():
        filtro_status = st.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"], key="sb_status_aba2")
        filtro_criticidade = st.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"], key="sb_crit_aba2")
        filtro_tempo = st.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"], key="sb_tempo_aba2")
    
    espaco_divisor_lateral.write("---")
    
    with espaco_upload_lateral.container():
        arquivo_upload = st.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"], key="up_aba2")
        if arquivo_upload is not None:
            try:
                if arquivo_upload.name.endswith('.csv'):
                    st.session_state.dados_planilha_persistidos = pd.read_csv(arquivo_upload)
                else:
                    st.session_state.dados_planilha_persistidos = pd.read_excel(arquivo_upload)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")

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
        st.markdown('📋 **Relatório Sincronizado de Ordens de Serviço**')
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.info("💡 Por favor, certifique-se de que a planilha está carregada na barra lateral.")

# ==========================================
# ABA 3: CENTRO DE DIAGNÓSTICO AVANÇADO (CÓDIGO ORIGINAL INTOCADO E APROVADO COM SIDEBAR)
# ==========================================
with aba_diagnostico:
    # Replica exatamente os mesmos seletores e uploader na faixa lateral ao acessar a Aba 3
    with espaco_filtros_laterais.container():
        filtro_status_3 = st.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"], key="sb_status_aba3")
        filtro_criticidade_3 = st.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"], key="sb_crit_aba3")
        filtro_tempo_3 = st.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"], key="sb_tempo_aba3")
    
    espaco_divisor_lateral.write("---")
    
    with espaco_upload_lateral.container():
        arquivo_upload_3 = st.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"], key="up_aba3")
        if arquivo_upload_3 is not None:
            try:
                if arquivo_upload_3.name.endswith('.csv'):
                    st.session_state.dados_planilha_persistidos = pd.read_csv(arquivo_upload_3)
                else:
                    st.session_state.dados_planilha_persistidos = pd.read_excel(arquivo_upload_3)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")

    st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.markdown("🔎 **Seleção de Ativo para Auditoria**")
        
        st.session_state.os_selecionada = st.selectbox(
            "Selecione a OS para análise da IA:", 
            lista_os, 
