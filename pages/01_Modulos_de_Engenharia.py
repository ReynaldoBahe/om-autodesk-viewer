import streamlit as st
import pandas as pd

# =========================================================================
# 1. MAPEAMENTO MULTI-CLIENTE (Centralizado por página)
# =========================================================================
EMPREENDIMENTOS = {
    "Resort Boa Viagem": {
        "speckle_url": r"https://speckle.systems",
        "nome_exibicao": "Resort Boa Viagem - Complexo Hoteleiro",
        "arquivo_cmms": "CMMS_Export_RB - CMMS_RB.csv",
        "stream_id": "fe9477b83d" # Substitua pelo ID real do seu modelo se houver
    },
    "Hospital Central": {
        "speckle_url": r"https://speckle.systems",
        "nome_exibicao": "Hospital Central - Centro Médico Operacional",
        "arquivo_cmms": "CMMS_Export_Hospital.csv - CMMS_RB.csv",
        "stream_id": "a3b2c1d4e5" # Substitua pelo ID real do seu modelo se houver
    }
}

# =========================================================================
# 2. BARREIRA DE SEGURANÇA E VERIFICAÇÃO DE LOGIN
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, realize o login primeiro.")
    st.stop()

cliente_logado = st.session_state.get("cliente_ativo", "Nenhum")

# Tratamento dinâmico para usuário administrador do sistema
if cliente_logado == "ADMIN":
    config = EMPREENDIMENTOS["Resort Boa Viagem"] # Define o empreendimento padrão para o Admin
    NOME_PROJETO = f"{config['nome_exibicao']}"
    CAMINHO_CSV = config["arquivo_cmms"]
elif cliente_logado in EMPREENDIMENTOS:
    config = EMPREENDIMENTOS[cliente_logado]
    NOME_PROJETO = config["nome_exibicao"]
    CAMINHO_CSV = config["arquivo_cmms"]
else:
    st.warning(f"⚠️ {cliente_logado}, os dados do seu empreendimento estão em processamento.")
    st.stop()

# =========================================================================
# 3. INTERFACE E CABEÇALHO DA PÁGINA
# =========================================================================
st.title(f"🏗️ Módulos de Engenharia — {NOME_PROJETO}")
st.caption(f"Sessão operacional segura: {st.session_state.get('user_email', 'Admin Master')}")

# CORREÇÃO DO NAMEERROR: Atribuição correta usando o dicionário config
speckle_base_url = config.get("speckle_url", "https://speckle.systems")
speckle_stream_id = config.get("stream_id", "")

# =========================================================================
# 4. PAINEL DE CONTROLE LATERAL (FILTROS)
# =========================================================================
st.sidebar.header("Painel de controle")
filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberto", "Em Execução", "Concluído"])
filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])

st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM", type=["csv", "xlsx"])

# =========================================================================
# 5. INTEGRALIZAÇÃO DO VISUALIZADOR OPERACIONAL 3D (SPECKLE)
# =========================================================================
st.subheader("Visualizador Operacional de Ativos 3D")

# Se houver um stream_id configurado, renderiza o iframe do Speckle
if speckle_stream_id:
    # URL típica de incorporação (embed) do Speckle Viewer
    embed_url = f"{speckle_base_url}/embed?stream={speckle_stream_id}"
    st.components.v1.iframe(embed_url, height=500, scrolling=True)
else:
    st.info("💡 Modelo 3D não vinculado ou link direto do Speckle carregado em segundo plano.")

# =========================================================================
# 6. PROCESSAMENTO E CARREGAMENTO DE DADOS CMMS
# =========================================================================
if arquivo_upload is not None:
    try:
        df = pd.read_csv(arquivo_upload) if arquivo_upload.name.endswith('.csv') else pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
        df = pd.read_csv(CAMINHO_CSV)
else:
    try:
        df = pd.read_csv(CAMINHO_CSV)
    except Exception:
        df = pd.DataFrame()

# Renderização dos dados caso a planilha exista
if not df.empty:
    st.write("---")
    st.subheader("📋 Inventário e Ativos do Módulo de Engenharia")
    
    # Padroniza nomes de colunas para exibição amigável
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    # Exibe a tabela interativa
    st.dataframe(df, use_container_width=True)
