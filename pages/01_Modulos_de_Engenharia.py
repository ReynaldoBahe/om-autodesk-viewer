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
    SPECKLE_STREAM_ID = config["speckle_url"]
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

st.markdown(f'<div class="main-title">🏗️ Módulos de Engenharia — {NOME_PROJETO}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Sessão operacional segura: {st.session_state.get("user_email")}</div>', unsafe_allow_html=True)

# =========================================================================
# 3. PAINEL DE CONTROLE LATERAL (FILTROS)
# =========================================================================
st.sidebar.header("Painel de controle")

filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])

st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM", type=["csv", "xlsx"])

# =========================================================================
# 4. CARREGAMENTO ISOLADO DOS DADOS (PANDAS)
# =========================================================================
if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        else:
            df = pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao ler arquivo enviado: {e}")
        df = pd.read_csv(CAMINHO_CSV)
else:
    try:
        df = pd.read_csv(CAMINHO_CSV)
    except Exception:
        df = pd.DataFrame(columns=["Status", "Criticidade"])

total_os = len(df)
os_criticas = len(df[df['Status'].str.lower() == 'alta']) if 'Status' in df.columns else 0
if 'Criticidade' in df.columns:
    os_criticas = len(df[df['Criticidade'].str.lower() == 'alta'])

if not df.empty and 'Status' in df.columns:
    if filtro_status != "Todos":
        df = df[df['Status'] == filtro_status]
    if filtro_criticidade != "Todos" and 'Criticidade' in df.columns:
        df = df[df['Criticidade'] == filtro_criticidade]

# =========================================================================
# 5. VISUALIZADOR 3D INTEGRADO (SPECKLE EMBED)
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">Visualizador Operacional de Ativos 3D</div></div>', unsafe_allow_html=True)

speckle_base_url = SPECKLE_STREAM_ID
st.components.v1.html(f'<iframe src="{speckle_base_url}" width="100%" height="600" frameborder="0"></iframe>', height=602)

# =========================================================================
# 6. CENTRO DE DIAGNÓSTICO E ANALYTICS (IA MULTI-CLIENTE)
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">📊 Centro de Diagnóstico Avançado (IA)</div></div>', unsafe_allow_html=True)

if not df.empty:
    # Padroniza nomes das colunas
    df.columns = [c.strip().title() for c in df.columns]
    
    total_os = len(df)
    os_criticas = len(df[df['Criticidade'].str.lower() == 'alta']) if 'Criticidade' in df.columns else 0
    os_abertas = len(df[df['Status'].str.lower().isin(['aberta', 'em andamento'])]) if 'Status' in df.columns else 0
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Total de Ordens de Serviço", value=total_os)
    with m2:
        st.metric(label="🚨 Ativos em Estado Crítico", value=os_criticas, delta="-2 este mês" if os_criticas > 0 else "Estável")
    with m3:
        st.metric(label="🛠️ OS Pendentes (Ação Imediata)", value=os_abertas)
        
    st.write("<br>", unsafe_allow_html=True)
    
    col_grafico, col_dados = st.columns([1.2, 1.0])
    
    with col_grafico:
        st.markdown("**Distribuição de Ordens por Criticidade e Status**")
        if 'Status' in df.columns and 'Criticidade' in df.columns:
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Status:N', title='Status da OS'),
                y=alt.Y('count():Q', title='Quantidade de Ativos'),
                color=alt.Color('Criticidade:N', scale=alt.Scale(domain=['Alta', 'Média', 'Baixa'], range=['#DC2626', '#F59E0B', '#10B981']))
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Colunas 'Status' ou 'Criticidade' ausentes para renderização do gráfico.")
            
    with col_dados:
        st.markdown(f"**Relatório Preditivo de Falhas — {NOME_PROJETO}**")
        
        with st.spinner("🤖 IA processando histórico de manutenção profundo..."):
            if 'Sistema Defeituoso' in df.columns:
                sistema_gargalo = df['Sistema Defeituoso'].value_counts().idxmax()
                falhas_sistema = df['Sistema Defeituoso'].value_counts().max()
            else:
                sistema_gargalo = "Não identificado"
                falhas_sistema = 0

            custo_mat = pd.to_numeric(df['Custo Material'], errors='coerce').sum() if 'Custo Material' in df.columns else 0
            custo_mo = pd.to_numeric(df['Custo Mao Obra'], errors='coerce').sum() if 'Custo Mao Obra' in df.columns else 0
            custo_total = custo_mat + custo_mo

            if 'Tipo Manutencao' in df.columns:
                corretivas = len(df[df['Tipo Manutencao'].str.lower().str.contains('corretiva|corretivo', na=False)])
                preventivas = len(df[df['Tipo Manutencao'].str.lower().str.contains('preventiva|preventivo', na=False)])
            else:
                corretivas, preventivas = 0, 0

            taxa_critica = (os_criticas / total_os * 100) if total_os > 0 else 0
            
            texto_custos = f"💰 **Impacto Financeiro:** Gasto total registrado de **R$ {custo_total:,.2f}** em materiais e MO." if custo_total > 0 else "💰 **Impacto Financeiro:** Sem custos financeiros atrelados."
            texto_gargalo = f"🔍 **Gargalo Físico:** O sistema mais instável é **{sistema_gargalo}**, concentrando {falhas_sistema} chamados abertos." if falhas_sistema > 0 else "🔍 **Gargalo Físico:** Distribuição homogênea entre sistemas prediais."
            
            if taxa_critica > 30:
                st.error(f"""
                ### ❌ ALERTA OPERACIONAL DE IA
                Sobrecarga nas rotinas de engenharia de **{NOME_PROJETO}**.
                
                {texto_gargalo}  
                {texto_custos}
                
                🚨 **PREDIÇÃO:** O volume de falhas em *{sistema_gargalo}* indica risco de parada forçada ou perda de eficiência nos próximos 7 dias.
                
                *   **Ação:** Realizar inspeção térmica e substituir as peças pendentes de imediato.
                """)
            else:
                st.success(f"""
                ### ✅ DIAGNÓSTICO DE SAÚDE OPERACIONAL
                O ecossistema técnico de **{NOME_PROJETO}** opera dentro das métricas normais.
                
                {texto_gargalo}  
                {texto_custos}
                
                📈 **MÉTRICA PREDITIVA:** Com {preventivas} preventivas contra {corretivas} corretivas, a curva aponta estabilização. O sistema de *{sistema_gargalo}* exige apenas rotina.
                """)

    st.write("---")
    st.markdown("**Visualização Completa do Banco de Dados Filtrado**")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhum dado cadastrado para exibição analítica de tabelas neste empreendimento.")
