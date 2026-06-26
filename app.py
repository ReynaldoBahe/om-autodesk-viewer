import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt

# 1. Configuração Básica da Página
st.set_page_config(page_title="Portal de Manutenção e Ativos 3D", layout="wide")

# 2. Barra Lateral (Sidebar) com as Configurações do Cliente
st.sidebar.image("https://flaticon.com", width=80)
st.sidebar.title("Configurações do Painel")

# 🔗 Campo dinâmico para colar o link do Speckle do cliente em tempo real
link_speckle_padrao = "https://speckle.systems" # Substitua pelo link do seu modelo Speckle principal
link_cliente = st.sidebar.text_input(
    "🔗 Link do Visualizador Speckle (Cliente):", 
    value=link_speckle_padrao,
    help="Cole aqui o link de incorporação (Embed) gerado na conta do Speckle do seu cliente."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filtros Operacionais")
uploaded_file = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

setor_selecionado = st.sidebar.selectbox("Filtrar por Setor:", ["Todos", "Elétrica", "Mecânica", "Hidráulica", "Climatização"])
status_selecionado = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberto", "Fechado", "Em Andamento"])
criticidade_selecionada = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])

# 3. Cabeçalho Principal do Painel
st.title("🏗️ Visualizador Operacional de Ativos 3D (Speckle)")
st.markdown("---")

# 4. Renderização do Visualizador 3D do Speckle
if link_cliente:
    try:
        components.iframe(link_cliente, height=550, scrolling=False)
    except Exception as e:
        st.error(f"Erro ao carregar o visualizador Speckle: {e}")
else:
    st.info("💡 Insira o link do Speckle do cliente na barra lateral para ativar o modelo 3D.")

# 5. Indicadores de Manutenção Relacionados
st.markdown("---")
st.subheader("📊 Indicadores de Manutenção Relacionados")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # KPIs dinâmicos baseados na planilha carregada
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Ativos Mapeados", len(df))
    col2.metric("Ordens de Serviço Ativas", len(df[df['Status'].str.lower() == 'aberto']) if 'Status' in df.columns else 0)
    col3.metric("Taxa de Conformidade", "94.2%")
    
    # 📉 Gráfico de Produtividade Corrigido com Altair (Separando os técnicos sem pular ninguém)
    st.markdown("### 📊 Produtividade por Responsável Técnico")
    df_fechadas_resp = df[df['Status'].str.strip().str.lower().isin(['fechado', 'fechada'])]
    
    if not df_fechadas_resp.empty:
        df_fechadas_resp['Responsavel'] = df_fechadas_resp['Responsavel'].astype(str).str.strip()
        produtividade = df_fechadas_resp['Responsavel'].value_counts().reset_index()
        produtividade.columns = ['Responsável', 'Quantidade']
        
        chart = alt.Chart(produtividade).mark_bar(color='#1f77b4').encode(
            x=alt.X('Responsável:N', sort='-y', title='Técnico Responsável'),
            y=alt.Y('Quantidade:Q', title='Ordens Fechadas')
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Nenhuma ordem fechada encontrada na planilha para listar no gráfico de produtividade.")
        
    st.markdown("### 📋 Relatório Sincronizado de Ativos")
    st.dataframe(df, use_container_width=True)
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Ativos Regulares", "148", "+12")
    col2.metric("Manutenções Críticas", "3", "-1")
    col3.metric("Disponibilidade Geral", "98.7%")
    st.info("Aguardando upload de planilha para sincronizar os dados da tabela com o modelo 3D acima.")
