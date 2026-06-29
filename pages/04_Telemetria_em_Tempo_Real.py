import streamlit as st
import datetime

# Garanta que a página esteja configurada como "wide" no início do arquivo
# st.set_page_config(layout="wide")

# ==============================================================================
# ⚡ SEÇÃO 1: MONITORAMENTO DE ENERGIA (Totalmente Isolada)
# ==============================================================================
st.header("⚡ Monitoramento de Energia")

# [NOVO - PADRÃO 2]: Gráfico de Linha de Energia inserido de ponta a ponta no topo
st.subheader("Gráfico de Linha - Parâmetros Elétricos (Potência, Corrente, Fator de Potência)")
# Coloque aqui a chamada do seu gráfico de linha original de energia
# Exemplo: st.line_chart(dados_eletricos_linhas_azuis)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Energia (Mantidos idênticos ao Padrão 1)
st.subheader("Consumo de Energia por Período")
col_eng_data1, col_eng_data2, col_eng_card = st.columns(3)

with col_eng_data1:
    data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")

with col_eng_data2:
    data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")

with col_eng_card:
    # Substitua o valor pelo cálculo da soma do seu dataframe de energia filtrado
    consumo_acumulado_eng = 1452.8 
    st.metric(label="Consumo Acumulado no Período", value=f"{consumo_acumulado_eng:,} kWh".replace(",", "."))

st.write("**Consumo Integrado (15 min):**")
# O seu gráfico de barras LARANJA (kWh) continua aqui abaixo do cartão
# Exemplo: st.bar_chart(dados_energia_filtrados, color="#FF4B4B")


st.markdown("<br><br><br><br>", unsafe_allow_html=True) # Espaçamento generoso entre as duas áreas


# ==============================================================================
# 💧 SEÇÃO 2: MONITORAMENTO DE ÁGUA (Totalmente Isolada)
# ==============================================================================
st.header("💧 Monitoramento de Água")

# [NOVO - PADRÃO 2]: Gráfico de Linha de Água inserido de ponta a ponta no topo
st.subheader("Gráfico de Linha - Vazão e Parâmetros Hidráulicos")
# Coloque aqui a chamada do seu gráfico de linha original de água
# Exemplo: st.line_chart(dados_agua_linhas_azuis)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Água (Mantidos idênticos ao Padrão 1)
st.subheader("Consumo de Água por Período")
col_agua_data1, col_agua_data2, col_agua_card = st.columns(3)

with col_agua_data1:
    data_ini_agua = st.date_input("Data Inicial (Água)", datetime.date(2026, 6, 22), key="ini_agua")

with col_agua_data2:
    data_fim_agua = st.date_input("Data Final (Água)", datetime.date(2026, 6, 29), key="fim_agua")

with col_agua_card:
    # Substitua o valor pelo cálculo da soma do seu dataframe de água filtrado
    consumo_acumulado_agua = 34.5 
    st.metric(label="Consumo Acumulado no Período", value=f"{consumo_acumulado_agua:,} m³".replace(",", "."))
