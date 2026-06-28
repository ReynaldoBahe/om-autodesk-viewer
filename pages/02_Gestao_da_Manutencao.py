import streamlit as st
import pandas as pd
import altair as alt

# =========================================================================
# 1. BARREIRA DE SEGURANÇA E MAPEAMENTO MULTI-CLIENTE
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, realize o login primeiro.")
    st.stop()

cliente_logado = st.session_state.get("cliente_ativo", "Nenhum")

EMPREENDIMENTOS = {
    "Resort Boa Viagem": {
        "speckle_url": r"https://speckle.systems",
        "nome_exibicao": "Resort Boa Viagem - Complexo Hoteleiro",
        "arquivo_cmms": "CMMS_Export_RB - CMMS_RB.csv"
    },
    "Hospital Central": {
        "speckle_url": r"https://speckle.systems",
        "nome_exibicao": "Hospital Central - Centro Médico Operacional",
        "arquivo_cmms": "CMMS_Export_Hospital.csv - CMMS_RB.csv"
    }
}

if cliente_logado in EMPREENDIMENTOS:
    config = EMPREENDIMENTOS[cliente_logado]
    NOME_PROJETO = config["nome_exibicao"]
    CAMINHO_CSV = config["arquivo_cmms"]
else:
    st.warning(f"⚠️ {cliente_logado}, os dados do seu empreendimento estão em processamento.")
    st.stop()

# =========================================================================
# 2. DESIGN E ESTILIZAÇÃO CUSTOMIZADA (CSS)
# =========================================================================
st.markdown("""
    <style>
        .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
        .sub-title { font-size: 14px; color: #4B5563; margin-bottom: 20px; }
        .card-home { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
        .card-home-title { font-size: 16px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-title">🛠️ Gestão da Manutenção (PCM) — {NOME_PROJETO}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Planejamento, Controle e Indicadores de Backlog: {st.session_state.get("user_email")}</div>', unsafe_allow_html=True)

# =========================================================================
# 3. PAINEL DE CONTROLE LATERAL (FILTROS DE PCM)
# =========================================================================
st.sidebar.header("Painel de Controle de PCM")
filtro_tipo_manut = st.sidebar.selectbox("Filtrar por Tipo:", ["Todos", "Preventiva", "Corretiva"])
st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM operacionais", type=["csv", "xlsx"])

# =========================================================================
# 4. CARREGAMENTO ISOLADO DOS DADOS (PANDAS)
# =========================================================================
if arquivo_upload is not None:
    try:
        df = pd.read_csv(arquivo_upload) if arquivo_upload.name.endswith('.csv') else pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao ler arquivo enviado: {e}")
        df = pd.read_csv(CAMINHO_CSV)
else:
    try:
        df = pd.read_csv(CAMINHO_CSV)
    except Exception:
        df = pd.DataFrame()

# Inicialização padrão das variáveis para evitar quebras visuais
total_om = 0
om_abertas_backlog = 0
taxa_cumprimento_prev = 100.0
df_pcm = df.copy() if not df.empty else pd.DataFrame()

col_status = []
col_tipo = []
col_setor = []

if not df.empty:
    # Padronização limpa das colunas
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    # Identificação dinâmica de colunas chave
    col_status = [c for c in df.columns if 'status' in c.lower()]
    col_tipo = [c for c in df.columns if 'tipo' in c.lower()]
    col_setor = [c for c in df.columns if 'setor' in c.lower() or 'sistema' in c.lower()]
    col_id_os = [c for c in df.columns if c.lower() == 'os' or 'numero' in c.lower()]

    # Aplica filtro interativo por tipo se selecionado na sidebar
    if col_tipo and filtro_tipo_manut != "Todos":
        df_pcm = df[df[col_tipo].astype(str).str.lower().str.contains(filtro_tipo_manut.lower()[:4], na=False)].copy()
    else:
        df_pcm = df.copy()

    # --- MÉTRICAS DE PCM ---
    total_om = len(df_pcm)
    
    if col_status:
        om_abertas_backlog = len(df_pcm[df_pcm[col_status].astype(str).str.lower().str.contains('aberta|em andamento|andamento', na=False)])
    
    if col_tipo and col_status:
        total_preventivas = len(df_pcm[df_pcm[col_tipo].astype(str).str.lower().str.contains('prev', na=False)])
        preventivas_concluidas = len(df_pcm[
            (df_pcm[col_tipo].astype(str).str.lower().str.contains('prev', na=False)) & 
            (df_pcm[col_status].astype(str).str.lower().str.contains('fechado|concluido|encerrado', na=False))
        ])
        taxa_cumprimento_prev = (preventivas_concluidas / total_preventivas * 100) if total_preventivas > 0 else 100.0

# =========================================================================
# 5. INTERFACE PRINCIPAL DO PCM
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">📋 Painel de Controle de Ordens e Backlog</div></div>', unsafe_allow_html=True)

if not df_pcm.empty:
    # Cartões de Métricas Operacionais de PCM
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="📋 Volume de Ordens no Escopo", value=total_om)
    with m2:
        st.metric(label="⏳ Backlog Ativo (Ordens Abertas)", value=om_abertas_backlog, delta="Ação Requerida" if om_abertas_backlog > 0 else "Zerado", delta_color="inverse" if om_abertas_backlog > 0 else "normal")
    with m3:
        st.metric(label="🎯 Cumprimento de Preventivas", value=f"{taxa_cumprimento_prev:.1f} %", delta="Conforme" if taxa_cumprimento_prev >= 90 else "Abaixo da Meta", delta_color="normal" if taxa_cumprimento_prev >= 90 else "inverse")

    st.write("<br>", unsafe_allow_html=True)
    col_grafico, col_dados = st.columns([1.2, 1.0])
    
    with col_grafico:
        tab_setor, tab_tipo = st.tabs(["📊 Carga por Setor", "🔄 Mix de Manutenção"])
        
        with tab_setor:
            st.markdown("**Ordens de Serviço por Setor Técnico**")
            if col_setor and col_status:
                chart_setor = alt.Chart(df_pcm).mark_bar().encode(
                    x=alt.X('count():Q', title='Quantidade de Ordens'),
                    y=alt.Y(f'{col_setor}:N', title='Setor / Sistema', sort='-x'),
                    color=alt.Color(f'{col_status}:N', title='Status')
                ).properties(height=250)
                st.altair_chart(chart_setor, use_container_width=True)
            else:
                st.info("Dados de setor indisponíveis para o gráfico.")
                
        with tab_tipo:
            st.markdown("**Proporção de Atividades no Período (Mix de O&M)**")
            if col_tipo:
                chart_mix = alt.Chart(df_pcm).mark_bar(color='#10B981').encode(
                    x=alt.X(f'{col_tipo}:N', title='Estratégia Técnico-Operacional'),
                    y=alt.Y('count():Q', title='Volume de Chamados')
                ).properties(height=250)
                st.altair_chart(chart_mix, use_container_width=True)
            else:
                st.info("Dados de estratégia de manutenção indisponíveis.")
            
    with col_dados:
        st.markdown(f"**Parecer da IA sobre o Plano de PCM — {NOME_PROJETO}**")
        
        # Extração de gargalos operacionais para laudo preditivo
        sistema_gargalo = "Não identificado"
        if col_setor and not df_pcm[col_setor].empty:
            v_counts = df_pcm[col_setor].value_counts()
            if not v_counts.empty:
                sistema_gargalo = str(v_counts.idxmax())

        # Análise lógica do mix operacional
        if taxa_cumprimento_prev < 90.0:
            st.error(f"""
            ### ❌ ALERTA DE FLUXO DE PCM
            Plano de manutenção preventiva comprometido em **{NOME_PROJETO}**.
            
            *   **Diagnóstico:** A taxa de execução de preventivas está em **{taxa_cumprimento_prev:.1f}%**, ficando abaixo da meta de conformidade regulatória (Meta >= 90%). 
            *   **Impacto Real:** A equipe está consumindo energia resolvendo quebras no setor de **{sistema_gargalo}** e deixando o plano de vistorias preventivas acumular no Backlog.
            
            🚨 **Ação Sugerida:** Pausar novas ordens de melhoria estética e priorizar o fechamento do lote de preventivas em atraso na próxima semana.
            """)
        else:
            st.success(f"""
            ### ✅ CONTROLE DE FLUXO EFICIENTE
            A rotina de PCM demonstra alto índice de maturidade operacional.
            
            *   **Diagnóstico:** Execução estável com **{taxa_cumprimento_prev:.1f}%** das preventivas cumpridas dentro do prazo de O&M.
            *   **Gestão de Carga:** O volume de **{om_abertas_backlog} ordens em aberto** está pulverizado de forma saudável e o sistema **{sistema_gargalo}** segue com monitoramento sob controle.
            
            👍 **Orientação:** Manter o balanceamento atual de homens-hora sem necessidade de horas extras na equipe.
            """)

    st.write("---")
    st.markdown("### Quadro de Ordens Filtrado por Escopo de PCM")
    st.dataframe(df_pcm, use_container_width=True)
else:
    st.info("Nenhum dado cadastrado para exibição de PCM neste empreendimento.")
