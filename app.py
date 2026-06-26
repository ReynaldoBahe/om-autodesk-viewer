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

# URL base do Speckle original aprovado
speckle_base_url = "https://speckle.systems"

# ==========================================
# 3. INTERAÇÃO INTELIGENTE DA BARRA LATERAL
# ==========================================
# Armazena os dados da planilha de forma persistente na sessão do usuário
if 'df_persistido' not in st.session_state:
    st.session_state.df_persistido = pd.DataFrame()

# Cria as variáveis padrão de filtros vazias caso o usuário esteja na Aba 1
filtro_status = "Todos"
filtro_criticidade = "Todos"
filtro_tempo = "Todos"
arquivo_upload = None

# Captura qual aba está selecionada usando o controle nativo de Abas do Streamlit
if 'aba_selecionada_key' not in st.session_state:
    st.session_state.aba_selecionada_key = 0

# Renderiza a barra lateral condicionalmente (Fica limpa na Aba 1 e com menu nas Abas 2 e 3)
st.sidebar.header("Filtros de Visão")

if st.session_state.aba_selecionada_key == 0:
    # ABA 1 selecionada: Deixa a faixa lateral cinza completamente limpa de widgets
    st.sidebar.caption("Visualização de Engenharia Ativa")
else:
    # ABAS 2 ou 3 selecionadas: Volta com o menu completo exatamente como estava aprovado
    filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
    filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])
    filtro_tempo = st.sidebar.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"])
    st.sidebar.write("---")
    arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

# Processa de forma invisível o upload do arquivo se ele for carregado nas Abas 2 ou 3
if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            st.session_state.df_persistido = pd.read_csv(arquivo_upload)
        else:
            st.session_state.df_persistido = pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

df = st.session_state.df_persistido

# Mapeia dinamicamente a lista de OS disponíveis com base na planilha ativa
if not df.empty and 'OS' in df.columns:
    lista_os = sorted(list(df['OS'].dropna().unique()))
else:
    lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]

# Configuração estável do estado da Ordem de Serviço selecionada
if 'os_selecionada' not in st.session_state or st.session_state.os_selecionada not in lista_os:
    if lista_os:
        st.session_state.os_selecionada = lista_os[0]

# Cálculo preventivo do ID BIM Alvo para evitar NameError nas renderizações entre abas
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
# 4. CRIAÇÃO ÚNICA DAS ABAS (MÓDULOS DO PORTAL)
# ==========================================
# O parâmetro do_index atualiza o session_state sempre que o usuário clica em outra aba
aba_modelo, aba_produtividade, aba_diagnostico = st.tabs([
    "📦 Modelo 3D (Speckle)", 
    "📊 Produtividade da Equipe", 
    "🧠 Centro de Diagnóstico (IA)"
])

# Força o Streamlit a monitorar cliques para redesenhar a barra lateral se houver troca de aba
if 'aba_anterior' not in st.session_state:
    st.session_state.aba_anterior = 0

# Detecta em qual aba o usuário está navegando no momento
with aba_modelo:
    if st.session_state.aba_anterior != 0:
        st.session_state.aba_selecionada_key = 0
        st.session_state.aba_anterior = 0
        st.rerun()
        
    st.subheader("Visualizador Operacional de Ativos 3D")
    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecione outra OS na aba Centro de Diagnóstico para focar)")
    st.components.v1.iframe(speckle_base_url, height=600, scrolling=False)

# ==========================================
# ABA 2: PRODUTIVIDADE E RELATÓRIO (CÓDIGO ORIGINAL APROVADO)
# ==========================================
with aba_produtividade:
    if st.session_state.aba_anterior != 1:
        st.session_state.aba_selecionada_key = 1
        st.session_state.aba_anterior = 1
        st.rerun()

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
        st.info("💡 Por favor, certifique-se de que a planilha está carregada na barra lateral das abas operacionais.")

# ==========================================
# ABA 3: CENTRO DE DIAGNÓSTICO AVANÇADO (CÓDIGO ORIGINAL APROVADO)
# ==========================================
with aba_diagnostico:
    if st.session_state.aba_anterior != 2:
        st.session_state.aba_selecionada_key = 2
        st.session_state.aba_anterior = 2
        st.rerun()

    st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.markdown("🔎 **Seleção de Ativo para Auditoria**")
        
        st.session_state.os_selecionada = st.selectbox(
            "Selecione a OS para análise da IA:", 
            lista_os, 
            index=lista_os.index(st.session_state.os_selecionada) if st.session_state.os_selecionada in lista_os else 0
        )
        
        resp, setor, status, data_ab = "Pedro", "Climatização", "Fechado", "20/06/2026"
        if not df.empty and 'OS' in df.columns:
            dados_os = df[df['OS'] == st.session_state.os_selecionada]
            if not dados_os.empty:
                col_t = next((c for c in df.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel']), None)
                resp = str(dados_os[col_t].values[0]) if col_t else "Pedro"
                setor = str(dados_os['Setor'].values[0]) if 'Setor' in df.columns else "Climatização"
