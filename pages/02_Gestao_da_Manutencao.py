import streamlit as st
import pandas as pd
import altair as alt
import datetime

# =========================================================================
# 1. BARREIRA DE SEGURANÇA E MAPEAMENTO MULTI-CLIENTE
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, realize o login primeiro.")
    st.stop()

cliente_logado = st.session_state.get("cliente_ativo", "Nenhum")

EMPREENDIMENTOS = {
    "Resort Boa Viagem": {
        "nome_exibicao": "Resort Boa Viagem - Complexo Hoteleiro",
        "arquivo_cmms": "CMMS_Export_RB - CMMS_RB.csv"
    },
    "Hospital Central": {
        "nome_exibicao": "Hospital Central - Centro Médico Operacional",
        "arquivo_cmms": "CMMS_Export_Hospital.csv - CMMS_RB.csv"
    }
}

if cliente_logado in EMPREENDIMENTOS:
    config = EMPREENDIMENTOS[cliente_logado]
    NOME_PROJETO = config["nome_exibicao"]
    CAMINHO_CSV = config["arquivo_cmms"]
else:
    st.warning(f"⚠️ {cliente_logado}, os dados estão em processamento.")
    st.stop()

# =========================================================================
# 2. DESIGN E TITULOS
# =========================================================================
st.markdown(f"## 🛠️ Gestão da Manutenção (PCM) — {NOME_PROJETO}")
st.markdown(f"**Sessão segura:** {st.session_state.get('user_email')}")

# =========================================================================
# 3. PAINEL DE CONTROLE LATERAL
# =========================================================================
st.sidebar.header("Painel de Controle de PCM")
filtro_tipo_manut = st.sidebar.selectbox("Filtrar por Tipo:", ["Todos", "Preventiva", "Corretiva"])

# --- NOVO FILTRO DE CUSTÓMIA POR GRUPO DE TEMPO (AGING) ---
opcoes_aging = ["Todas as Faixas", "01. 0 a 7 dias", "02. 7 a 15 dias", "03. 15 a 30 dias", "04. Mais de 30 dias (Crônico)"]
filtro_aging = st.sidebar.selectbox("Filtrar por Faixa de Aging:", opcoes_aging)

st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM operacionais", type=["csv", "xlsx"])

# =========================================================================
# 4. CARREGAMENTO DOS DADOS
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

# =========================================================================
# 5. PROCESSAMENTO E INDICADORES
# =========================================================================
if not df.empty:
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    col_status = [c for c in df.columns if 'status' in c.lower()]
    col_tipo = [c for c in df.columns if 'tipo' in c.lower()]
    col_setor = [c for c in df.columns if 'setor' in c.lower() or 'sistema' in c.lower()]
    col_abertura = [c for c in df.columns if 'abertura' in c.lower() or 'inicio' in c.lower()]
    col_fechamento = [c for c in df.columns if 'fechamento' in c.lower() or 'fim' in c.lower() or 'conclusao' in c.lower()]
    
    c_status = col_status[0] if col_status else ""
    c_tipo = col_tipo[0] if col_tipo else ""
    c_setor = col_setor[0] if col_setor else ""
    c_abertura = col_abertura[0] if col_abertura else ""
    c_fechamento = col_fechamento[0] if col_fechamento else ""

    # Criação da base de análise
    df_pcm = df.copy()

    # --- CÁLCULO SEGURO E LINEAR DE AGING (GERAL) ---
    if c_abertura:
        df_pcm['Data_Abertura_Conv'] = pd.to_datetime(df_pcm[c_abertura], errors='coerce')
        
        if c_fechamento:
            df_pcm['Data_Fechamento_Conv'] = pd.to_datetime(df_pcm[c_fechamento], errors='coerce')
            df_pcm['Data_Final_Calculo'] = df_pcm['Data_Fechamento_Conv'].fillna(pd.Timestamp(datetime.date.today()))
        else:
            df_pcm['Data_Final_Calculo'] = pd.Timestamp(datetime.date.today())
            
        df_pcm['Dias_No_Backlog'] = (df_pcm['Data_Final_Calculo'] - df_pcm['Data_Abertura_Conv']).dt.total_seconds() / 86400.0
        df_pcm['Dias_No_Backlog'] = df_pcm['Dias_No_Backlog'].fillna(0.0).clip(lower=0.0)

        # Categorização direta via condições lógicas do Pandas
        df_pcm['Faixa_Aging'] = "01. 0 a 7 dias"
        df_pcm.loc[df_pcm['Dias_No_Backlog'] > 7, 'Faixa_Aging'] = "02. 7 a 15 dias"
        df_pcm.loc[df_pcm['Dias_No_Backlog'] > 15, 'Faixa_Aging'] = "03. 15 a 30 dias"
        df_pcm.loc[df_pcm['Dias_No_Backlog'] > 30, 'Faixa_Aging'] = "04. Mais de 30 dias (Crônico)"
        
        df_pcm['Mes_Ano'] = df_pcm['Data_Abertura_Conv'].dt.to_period('M').astype(str)

    # --- APLICAÇÃO DOS FILTROS INTERATIVOS DA SIDEBAR ---
    if c_tipo and filtro_tipo_manut != "Todos":
        df_pcm = df_pcm[df_pcm[c_tipo].astype(str).str.lower().str.contains(filtro_tipo_manut.lower()[:4], na=False)]

    if 'Faixa_Aging' in df_pcm.columns and filtro_aging != "Todas as Faixas":
        df_pcm = df_pcm[df_pcm['Faixa_Aging'] == filtro_aging]

    # Contagens básicas e taxas de preventivas calculadas após os filtros
    total_om = len(df_pcm)
    om_abertas = 0
    taxa_prev = 100.0
    tempo_medio_backlog_dias = float(df_pcm['Dias_No_Backlog'].mean()) if not df_pcm.empty and 'Dias_No_Backlog' in df_pcm.columns else 0.0
    
    if c_status:
        om_abertas = len(df_pcm[df_pcm[c_status].astype(str).str.lower().str.contains('aberta|em andamento|andamento', na=False)])
    
    if c_tipo and c_status:
        tot_p = len(df_pcm[df_pcm[c_tipo].astype(str).str.lower().str.contains('prev', na=False)])
        concl_p = len(df_pcm[(df_pcm[c_tipo].astype(str).str.lower().str.contains('prev', na=False)) & (df_pcm[c_status].astype(str).str.lower().str.contains('fechado|concluido|encerrado', na=False))])
        taxa_prev = (concl_p / tot_p * 100) if tot_p > 0 else 100.0

    # Quatro Cartões de Métricas Alinhados no Topo
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="📋 Volume de Ordens", value=total_om)
    with m2:
        st.metric(label="⏳ Backlog Ativo (Abertas)", value=om_abertas)
    with m3:
        st.metric(label="🎯 Cumprimento Preventivas", value=f"{taxa_prev:.1f} %")
    with m4:
        st.metric(label="⏱ Vinculo de Tempo Médio", value=f"{tempo_medio_backlog_dias:.1f} dias")

    st.write("---")
    
    col_grafico, col_dados = st.columns([1.2, 1.0])
    
    with col_grafico:
        tab_setor, tab_tendencia, tab_aging = st.tabs(["📊 Carga por Setor", "📈 Linha de Tendência", "⏳ Tempo de Residência (Aging)"])
        
        with tab_setor:
            if c_setor and c_status:
                chart = alt.Chart(df_pcm).mark_bar().encode(
                    x=alt.X('count():Q', title='Quantidade de Ordens'),
                    y=alt.Y(f'{c_setor}:N', title='Setor / Sistema', sort='-x'),
                    color=alt.Color(f'{c_status}:N', title='Status')
                ).properties(height=250)
                st.altair_chart(chart, use_container_width=True)
                
        with tab_tendencia:
            if c_abertura and 'Mes_Ano' in df_pcm.columns and not df_pcm.empty:
                df_trend = df_pcm.groupby('Mes_Ano').size().reset_index(name='Volume')
                chart_line = alt.Chart(df_trend).mark_line(color='#1E3A8A', point=True).encode(
                    x=alt.X('Mes_Ano:N', title='Mês/Ano', sort='x'),
                    y=alt.Y('Volume:Q', title='Novas Ordens'),
                    tooltip=['Mes_Ano', 'Volume']
                ).properties(height=250)
                st.altair_chart(chart_line, use_container_width=True)

        with tab_aging:
            st.markdown("**Distribuição de Ordens por Tempo de Espera (Aging)**")
            if 'Faixa_Aging' in df_pcm.columns and not df_pcm.empty:
                chart_aging = alt.Chart(df_pcm).mark_bar(color='#EAB308').encode(
                    x=alt.X('Faixa_Aging:N', title='Tempo de Permanência no Backlog'),
                    y=alt.Y('count():Q', title='Quantidade de OS'),
                    tooltip=['Faixa_Aging', 'count()']
                ).properties(height=250)
                st.altair_chart(chart_aging, use_container_width=True)

    with col_dados:
        st.markdown(f"**Parecer do Gemini sobre o Plano de PCM — {NOME_PROJETO}**")
        
        sistema_gargalo = "Não identificado"
        if c_setor and not df_pcm[c_setor].empty:
            v_counts = df_pcm[c_setor].value_counts()
            if not v_counts.empty:
                sistema_gargalo = str(v_counts.idxmax())

        # Relatório Inteligente Dinâmico
        if filtro_aging != "Todas as Faixas":
            st.info(f"""
            ### 🎯 AUDITORIA DETALHADA DE AGING
            Você isolou o painel para analisar a faixa: **{filtro_aging}**.
            
            * **Foco:** A tabela abaixo e os gráficos acima agora refletem **apenas as {total_om} ordens** que pertencem a esta janela temporal de atraso.
            * **Gargalo Local:** O sistema com mais ocorrências retidas neste grupo é **{sistema_gargalo}**.
            """)
        else:
            if tempo_medio_backlog_dias > 15.0:
                st.error(f"""
                ### ❌ ALERTA DE ENVELHECIMENTO CRÔNICO
                As ordens estão retidas por muito tempo na fila de espera.
                
                * **Diagnóstico:** O tempo de backlog médio de **{tempo_medio_backlog_dias:.1f} dias** indica lentidão no fluxo de liquidação.
                * **Gargalo:** O setor de **{sistema_gargalo}** concentra o maior volume.
                """)
            else:
                st.success(f"""
