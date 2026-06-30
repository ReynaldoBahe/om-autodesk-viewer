import streamlit as st
import pandas as pd
import altair as alt

# =========================================================================
# 1. MAPEAMENTO MULTI-CLIENTE (Configurações Centrais da Página)
# =========================================================================
EMPREENDIMENTOS = {
    "Resort Boa Viagem": {
        "speckle_url": r"https://speckle.systems",
        "nome_exibicao": "Resort Boa Viagem - Complexo Hoteleiro",
        "arquivo_cmms": "CMMS_Export_RB - CMMS_RB.csv",
        "stream_id": "fe9477b83d"
    },
    "Hospital Central": {
        "speckle_url": r"https://speckle.systems",
        "nome_exibicao": "Hospital Central - Centro Médico Operacional",
        "arquivo_cmms": "CMMS_Export_Hospital.csv - CMMS_RB.csv",
        "stream_id": "a3b2c1d4e5"
    }
}

# =========================================================================
# 2. BARREIRA DE SEGURANÇA E MAPEAMENTO MULTI-CLIENTE
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, realize o login primeiro.")
    st.stop()

cliente_logado = st.session_state.get("cliente_ativo", "Nenhum")

if cliente_logado == "ADMIN":
    config = EMPREENDIMENTOS["Resort Boa Viagem"]
    NOME_PROJETO = f"Visão Geral Administrador ({config['nome_exibicao']})"
    CAMINHO_CSV = config["arquivo_cmms"]
elif cliente_logado in EMPREENDIMENTOS:
    config = EMPREENDIMENTOS[cliente_logado]
    NOME_PROJETO = config["nome_exibicao"]
    CAMINHO_CSV = config["arquivo_cmms"]
else:
    st.warning(f"⚠️ {cliente_logado}, os dados do seu empreendimento estão em processamento.")
    st.stop()

# =========================================================================
# 3. DESIGN E ESTILIZAÇÃO CUSTOMIZADA (CSS)
# =========================================================================
st.markdown("""
    <style>
        .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
        .sub-title { font-size: 14px; color: #4B5563; margin-bottom: 20px; }
        .card-home { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
        .card-home-title { font-size: 16px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-title">🏗️ Módulos de Engenharia — {NOME_PROJETO}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Usuário conectado: {st.session_state.get("user_email")}</div>', unsafe_allow_html=True)

# =========================================================================
# 4. PAINEL DE CONTROLE LATERAL
# =========================================================================
st.sidebar.header("Painel de Controle")
filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberto", "Em Execução", "Concluído"])
filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])
st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM", type=["csv", "xlsx"])

# =========================================================================
# 5. CARREGAMENTO E PARSING DE DADOS
# =========================================================================
if arquivo_upload is not None:
    try:
        df = pd.read_csv(arquivo_upload) if arquivo_upload.name.endswith('.csv') else pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro no arquivo enviado: {e}")
        df = pd.read_csv(CAMINHO_CSV)
else:
    try:
        df = pd.read_csv(CAMINHO_CSV)
    except Exception:
        df = pd.DataFrame()

# Processamento de filtros e colunas caso haja dados carregados
if not df.empty:
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    col_status_list = [c for c in df.columns if 'status' in c.lower() or 'situacao' in c.lower()]
    col_criticidade_list = [c for c in df.columns if 'crit' in c.lower()]
    
    if col_status_list:
        os_abertas = len(df[df[col_status_list[0]].astype(str).str.lower().str.contains('abert|andamento', na=False)])
    else:
        os_abertas = 0

    if col_status_list and filtro_status != "Todos":
        df = df[df[col_status_list[0]].astype(str).str.lower() == filtro_status.lower()]
        
    if col_criticidade_list and filtro_criticidade != "Todos":
        df = df[df[col_criticidade_list[0]].astype(str).str.lower() == filtro_criticidade.lower()]

# =========================================================================
# 6. VISUALIZADOR 3D INTEGRADO (SPECKLE EMBED) - LINHAS CORRIGIDAS E ALINHADAS
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">Visualizador Operacional de Ativos 3D</div></div>', unsafe_allow_html=True)

speckle_id = config.get("stream_id", "fe9477b83d")
speckle_base_url = f"https://speckle.systems{speckle_id}"

st.components.v1.html(f'<iframe src="{speckle_base_url}" width="100%" height="600" frameborder="0"></iframe>', height=602)

# =========================================================================
# 7. CENTRO DE DIAGNÓSTICO E ANALYTICS (TABELA DE DADOS CMMS)
# =========================================================================
if not df.empty:
    st.write("<br>", unsafe_allow_html=True)
    st.subheader("📋 Ordens de Serviço e Inventário Operacional")
    st.dataframe(df, use_container_width=True)
else:
    st.info("💡 Carregue uma planilha válida para visualizar a tabela consolidada de Ordens de Serviço.")
