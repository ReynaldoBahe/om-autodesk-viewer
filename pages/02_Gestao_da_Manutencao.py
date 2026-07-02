import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(
    page_title="RB Consultoria - Gestão de Ativos",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔐 TRAVA DE SEGURANÇA
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Acesso negado. Por favor, faça o login na página inicial.")
    st.stop()

# Estilização CSS para o design do card de IA
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    .card-ia {
        background-color: #f0f7ff;
        border-left: 5px solid #0066cc;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Layout de Tela: Barra Lateral (Métricas Operacionais)
with st.sidebar:
    st.title("Painel de Controle")
    st.markdown("---")
    
    arquivo_upload = st.file_uploader("Carregar Planilha CMMS (.csv)", type=["csv"])
    st.markdown("---")
    
    df_exibicao = pd.DataFrame()
    lista_os_selecao = ["Nenhuma OS selecionada"]
    contagem_status = {"Aberta": 0, "Em Atendimento": 0, "Pausada": 0, "Fechado": 0}
    
    if arquivo_upload is not None:
        try:
            df_os = pd.read_csv(arquivo_upload)
            df_os.columns = df_os.columns.str.strip()
            
            df_os['Data_Abertura'] = pd.to_datetime(df_os['Data_Abertura'], errors='coerce')
            df_os['Status'] = df_os['Status'].astype(str).str.strip()
            df_os['Setor'] = df_os['Setor'].astype(str).str.strip()
            df_os['OS'] = df_os['OS'].astype(str).str.strip()
            
            df_mes = df_os[df_os['Data_Abertura'].dt.strftime('%Y-%m') == '2026-06']
            
            contagem_status["Aberta"] = len(df_mes[df_mes['Status'].str.lower() == 'aberta'])
            contagem_status["Em Atendimento"] = len(df_mes[df_mes['Status'].str.lower() == 'em atendimento'])
            contagem_status["Pausada"] = len(df_mes[df_mes['Status'].str.lower() == 'pausado'])
            contagem_status["Fechado"] = len(df_mes[df_mes['Status'].str.lower() == 'fechado'])
            
            st.subheader("Filtros de Visão")
            setores_validos = df_mes['Setor'].dropna().astype(str).unique()
            lista_setores = ["Todos"] + sorted(list(setores_validos))
            setor_selecionado = st.selectbox("Filtrar por Setor:", lista_setores)
            
            status_validos = df_mes['Status'].dropna().astype(str).unique()
            lista_status = ["Todos"] + sorted(list(status_validos))
            status_selecionado = st.selectbox("Filtrar por Status:", lista_status)
            
            df_exibicao = df_mes.copy()
            if setor_selecionado != "Todos":
                df_exibicao = df_exibicao[df_exibicao['Setor'] == setor_selecionado]
            if status_selecionado != "Todos":
                df_exibicao = df_exibicao[df_exibicao['Status'] == status_selecionado]
            
            lista_os_selecao = sorted(list(df_exibicao['OS'].unique()))
            
            st.markdown("---")
            st.subheader("Métricas de Manutenção")
            total_abertas_mes = len(df_mes)
            if total_abertas_mes > 0:
                total_fechadas_filtradas = len(df_mes[df_mes['Status'].str.lower() == 'fechado'])
                sla_calculado = round((total_fechadas_filtradas / total_abertas_mes) * 100, 1)
                st.metric(label="SLA de Atendimento", value=f"{sla_calculado}%")
        except Exception as e:
            st.error(f"Erro ao processar as colunas: {e}")
    else:
        st.warning("Aguardando upload da planilha...")

# 3. Layout Principal da Tela
st.title("Visualizador Operacional de Ativos")
st.markdown("---")

# 4. Volumetria das Ordens de Serviço (KPIs)
st.subheader("📊 Volumetria das Ordens de Serviço")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric(label="🟢 Aberta", value=contagem_status["Aberta"])
with col2: st.metric(label="🔵 Em Atendimento", value=contagem_status["Em Atendimento"])
with col3: st.metric(label="🟡 Pausada", value=contagem_status["Pausada"])
with col4: st.metric(label="🔴 Fechado", value=contagem_status["Fechado"])

st.markdown("---")

# 5. Centro de Diagnóstico Avançado (IA Preditiva)
st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")

if arquivo_upload is not None and not df_exibicao.empty:
    col_sel, col_diag = st.columns(2)
    
    with col_sel:
        st.markdown("**🔎 Seleção de Ativo para Auditoria**")
        os_selecionada = st.selectbox("Selecione a OS para análise da IA:", lista_os_selecao, key="seletor_ia_final_limpo")
        
        filtro_os = df_exibicao[df_exibicao['OS'] == os_selecionada]
        linha_os = filtro_os.iloc[0]
        
        id_coluna_b = str(linha_os.get('ID', '')).strip().lower()
        equipamento, fabricante, modelo = "Sistema de Climatização", "Fujitsu General", "ASYG18LFCA"
            
        data_abertura_formatada = "N/A" if pd.isna(linha_os.get('Data_Abertura')) else linha_os['Data_Abertura'].strftime('%d/%m/%Y')
        df_historico_ativo = df_os[(df_os['ID'].astype(str).str.strip().str.lower() == id_coluna_b) & (df_os['OS'] != os_selecionada)]
        
        texto_historico_ia = ""
        if not df_historico_ativo.empty:
            for _, row_hist in df_historico_ativo.iterrows():
                try:
                    data_hist = row_hist['Data_Abertura'].strftime('%d/%m/%Y') if not pd.isna(row_hist['Data_Abertura']) else "N/A"
                except:
                    data_hist = str(row_hist['Data_Abertura'])
                texto_historico_ia += f"- OS {row_hist['OS']} ({data_hist}): {row_hist['Descrição']} | Status: {row_hist['Status']}\n"
        else:
            texto_historico_ia = "Nenhuma ocorrência anterior registrada para este ativo nos últimos meses."

        st.info(f"""
        **📋 Ficha Técnica do Ativo (Parâmetros Speckle/BIM)**
        * **Equipamento:** {equipamento}
        * **Fabricante:** {fabricante}
        * **Modelo:** {modelo}
        * **Status Atual:** {linha_os.get('Status', 'Aberto')}
        * **Data de Abertura:** {data_abertura_formatada}
        * **ID do Objeto 3D:** `{id_coluna_b}`
        """)
        
        with st.expander("📊 Ver Histórico Completo do Ativo (Coluna B)"):
            if not df_historico_ativo.empty:
                st.dataframe(df_historico_ativo[['OS', 'Data_Abertura', 'Descrição', 'Status']], use_container_width=True)
            else:
                st.caption("Este ativo não possui ordens de serviço anteriores.")
        
    with col_diag:
        st.markdown("**⚡ Análise de Engenharia Operacional da IA**")
        status_normalizado = str(linha_os.get('Status', '')).strip().lower()
        
        if status_normalizado == 'aberta':
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            prompt_sistema = "Você é um Engenheiro de Manutenção especialista em análise de falhas. Emita um laudo prescritivo estruturado em HTML simples."
            prompt_usuario = f"""
            Analise a OS atual cruzando com o histórico anterior do ativo para identificar padrões de falhas.
            DADOS DA OS ATUAL:
            - Ordem de Serviço: {linha_os.get('OS')}
            - Descrição da Falha Atual: {linha_os.get('Descrição')}
            - Setor Responsável: {linha_os.get('Setor')}
            HISTÓRICO COMPLETO REINCIDÊNCIAS:
            {texto_historico_ia}
            INSTRUÇÕES: Envolva a resposta em uma tag <div class='card-ia'> contendo título h4, Causa Raiz, e uma lista ordenada <ol> de até 3 passos práticos de plano de ação técnico.
            """
            
            with st.spinner("Gemini analisando histórico e gerando diagnóstico preditivo..."):
                try:
                    model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=prompt_sistema)
                    resposta_ia = model.generate_content(prompt_usuario)
                    
                    if resposta_ia and resposta_ia.text:
                        conteudo_html = str(resposta_ia.text).strip()
                        conteudo_html = conteudo_html.replace("```html", "").replace("```", "").strip()
                        st.markdown(conteudo_html, unsafe_allow_html=True)
                    else:
                        st.error("A IA processou o pedido, mas o retorno veio em formato inválido.")
                except Exception as erro:
                    st.error(f"Erro na comunicação com a API do Gemini: {erro}")
            
        elif status_normalizado == 'em atendimento':
            st.markdown('<div class="card-ia"><h4>⏳ Manutenção em Andamento</h4><p>O ativo encontra-se sob intervenção técnica.</p></div>', unsafe_allow_html=True)
        elif status_normalizado in ['pausado', 'pausada']:
            st.markdown('<div class="card-ia"><h4>⏸️ Ordem Suspensa</h4><p>A atividade está congelada aguardando insumos.</p></div>', unsafe_allow_html=True)
        elif status_normalizado in ['fechado', 'fechada']:
            st.markdown('<div class="card-ia"><h4>✅ Ordem Encerrada</h4><p>A OS foi finalizada com sucesso.</p></div>', unsafe_allow_html=True)
        else:
            st.warning(f"Status '{linha_os.get('Status')}' mapeado.")
else:
    st.info("Aguardando carregamento de dados para diagnóstico da IA.")
