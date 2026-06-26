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
# ABA 1: MODELO 3D (INTERAÇÃO COM FILTROS LATERAIS)
# ==========================================
with aba_modelo:
    st.subheader("Visualizador Operacional de Ativos 3D")
    
    # 1. Recupera o ID do Ativo correspondente à OS selecionada
    id_bim_alvo = ""
    if not df.empty and 'OS' in df.columns:
        col_id = next((c for c in df.columns if c.upper() == 'ID'), None)
        if col_id:
            linha_ativo = df[df['OS'] == st.session_state.os_selecionada]
            if not linha_ativo.empty:
                id_bim_alvo = str(linha_ativo[col_id].values[0]).strip()

    if not id_bim_alvo or id_bim_alvo == "nan":
        id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecionado no Centro de Diagnóstico)")
    
    # 2. CONSTRUÇÃO DA URL DINÂMICA COM REGRAS DE FILTRAGEM
    speckle_url_interativa = speckle_base_url
    
    # Regra 1: Filtragem por Status da Barra Lateral (Isola os objetos no canvas)
    if filtro_status != "Todos":
        speckle_url_interativa += f'&filter=[{{"property":"status","operator":"=","value":"{filtro_status}"}}]'
    
    # Regra 2: Realce por Criticidade da Barra Lateral (Aplica mapeamento de cores)
    if filtro_criticidade != "Todos":
        speckle_url_interativa += f'&cby=criticidade'
    
    # Regra 3: Foca e destaca a câmera do visualizador diretamente no ativo em auditoria
    if id_bim_alvo:
        speckle_url_interativa += f'&overlayObjIds={id_bim_alvo}'
    
    # Renderiza o visualizador com a URL interativa criada
    st.components.v1.iframe(speckle_url_interativa, height=600, scrolling=False)

# ==========================================
# 4. CONFIGURAÇÃO DO ESTADO DA SESSÃO (SESSION STATE)
# ==========================================
if 'os_selecionada' not in st.session_state or st.session_state.os_selecionada not in lista_os:
    if lista_os:
        st.session_state.os_selecionada = lista_os[0]

# ==========================================
# 5. CRIAÇÃO ÚNICA DAS ABAS DO PORTAL
# ==========================================
aba_modelo, aba_produtividade, aba_diagnostico = st.tabs([
    "📦 Modelo 3D (Speckle)", 
    "📊 Produtividade da Equipe", 
    "🧠 Centro de Diagnóstico (IA)"
])

# ==========================================
# ABA 1: MODELO 3D (INTEGRAL DA DIREITA)
# ==========================================
with aba_modelo:
    st.subheader("📦 Visualizador Operacional de Ativos 3D")
    
    id_bim_alvo = ""
    if not df.empty and mapeamento_colunas["OS"] in df.columns:
        col_id = mapeamento_colunas["ID"]
        if col_id in df.columns:
            linha_ativo = df[df[mapeamento_colunas["OS"]] == st.session_state.os_selecionada]
            if not linha_ativo.empty:
                id_bim_alvo = str(linha_ativo[col_id].values[0]).strip()

    if not id_bim_alvo or id_bim_alvo == "nan":
        id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

    c1, c2 = st.columns(2)
    with c1:
        st.info(f"🎯 **Ativo em Foco:** `{id_bim_alvo}` (Sincronizado com o Centro de Diagnóstico)")
    with c2:
        st.success("💡 **Dica de Engenharia:** Use os painéis laterais nativos do modelo para auditar parâmetros de instância do Revit.")

    speckle_url_interativa = speckle_base_url
    
    if sistema_mapeado != "Completo":
        speckle_url_interativa += f'&filter=[{{"property":"{mapeamento_colunas["Setor"]}","operator":"=","value":"{sistema_mapeado}"}}]'
        speckle_url_interativa += f'&cby={mapeamento_colunas["Setor"]}'
        
    if filtro_status != "Todos":
        speckle_url_interativa += f'&filter=[{{"property":"{mapeamento_colunas["Status"]}","operator":"=","value":"{filtro_status}"}}]'
        
    if id_bim_alvo:
        speckle_url_interativa += f'&overlayObjIds={id_bim_alvo}&selection={id_bim_alvo}'
        
    st.components.v1.iframe(speckle_url_interativa, height=650, scrolling=False)

# ==========================================
# ABA 2: PRODUTIVIDADE E RELATÓRIO
# ==========================================
with aba_produtividade:
    if not df.empty:
        df_filtrado = df.copy()
        col_status = mapeamento_colunas["Status"]
        
        if filtro_status != "Todos" and col_status in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado[col_status] == filtro_status]
            
        st.markdown('<div class="vol-title">📊 Volumetria das Ordens de Serviço</div>', unsafe_allow_html=True)
        status_counts = df[col_status].value_counts() if col_status in df.columns else {}
        
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
        col_tecnico = mapeamento_colunas["Tecnico"]
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
# ABA 1: MODELO 3D (RASTREABILIDADE BIM)
# ==========================================
with aba_modelo:
    st.subheader("Visualizador Operacional de Ativos 3D")
    
    id_bim_alvo = ""
    if not df.empty and 'OS' in df.columns:
        col_id = next((c for c in df.columns if c.upper() == 'ID'), None)
        if col_id:
            linha_ativo = df[df['OS'] == st.session_state.os_selecionada]
            if not linha_ativo.empty:
                id_bim_alvo = str(linha_ativo[col_id].values[0]).strip()

    if not id_bim_alvo or id_bim_alvo == "nan":
        id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

    # Exibição elegante da inteligência de cruzamento de dados (Sem botões que não funcionam)
    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecionado no Centro de Diagnóstico)")
    
    st.components.v1.iframe(speckle_base_url, height=600, scrolling=False)
