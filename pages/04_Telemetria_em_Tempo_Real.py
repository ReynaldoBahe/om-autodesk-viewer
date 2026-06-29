import streamlit as st
import datetime

# Garanta que a página esteja configurada como "wide" no início do arquivo
# st.set_page_config(layout="wide")

# ==============================================================================
# ⚡ TOPO: SEÇÃO ELÉTRICA CLÁSSICA (LARGURA TOTAL DA TELA)
# ==============================================================================
st.header("⚡ Monitoramento de Energia - Tempo Real")

# O gráfico original de linhas azuis que responde à janela suspensa
st.subheader("Parâmetros Elétricos (Potência, Corrente, Fator de Potência)")
# Coloque aqui o seu gráfico de linha clássico amplo
# Exemplo: st.line_chart(dados_eletricos_classicos)

st.markdown("---") # Linha divisória para o rodapé

# ==============================================================================
# 📊 RODAPÉ: SEÇÃO POR PERÍODO LADO A LADO (DUAS COLUNAS PERFEITAS)
# ==============================================================================
coluna_esquerda_energia, coluna_direita_agua = st.columns(2)

# ------------------------------------------------------------------------------
# COLUNA DA ESQUERDA: GERENCIAMENTO DE ENERGIA (BARRAS LARANJA)
# ------------------------------------------------------------------------------
with coluna_esquerda_energia:
    st.subheader("⚡ Consumo de Energia por Período")
    
    col_eng_filtro, col_eng_grafico = st.columns([1, 2])
    
    with col_eng_filtro:
        st.write("**Período**")
        data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")
        data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")

    with col_eng_grafico:
        st.write("**Consumo Integrado (15 min)**")
        # Coloque aqui o seu gráfico de barras LARANJA (kWh)
        # Exemplo: st.bar_chart(dados_energia_filtrados, color="#FF4B4B")


# ------------------------------------------------------------------------------
# COLUNA DA DIREITA: GERENCIAMENTO DE ÁGUA (BARRAS AZUIS)
# ------------------------------------------------------------------------------
with coluna_direita_agua:
    st.subheader("💧 Consumo de Água por Período")
    
    col_agua_filtro, col_agua_grafico = st.columns([1, 2])
    
    with col_agua_filtro:
        st.write("**Período**")
        data_ini_agua = st.date_input("Data Inicial (Água)", datetime.date(2026, 6, 22), key="ini_agua")
        data_fim_agua = st.date_input("Data Final (Água)", datetime.date(2026, 6, 29), key="fim_agua")

    with col_agua_grafico:
        st.write("**Consumo Integrado (15 min)**")
        # Coloque aqui o seu gráfico de barras AZUL (m³)
        # Exemplo: st.bar_chart(dados_agua_filtrados, color="#0000FF")
