import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Telemetria em Tempo Real", page_icon="📊", layout="wide")

# =========================================================================
# # TRAVA DE SEGURANÇA INTEGRADA AO SEU PORTAL
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, faça o login na página inicial.")
    st.stop()

nome_cliente = st.session_state.get("cliente_ativo", "Cliente")

st.markdown(f'<h2 style="color: #1E3A8A;">📊 Telemetria de Ativos & Utilidades — {nome_cliente}</h2>', unsafe_allow_html=True)
st.write("Monitoramento contínuo e histórico de grandezas elétricas e consumo hídrico.")

st.markdown("---")

# =========================================================================
# # METRICS DE TELEMETRIA (IoT) - CARDS DO TOPO
# =========================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Potência Ativa Atual", value="45.3 kW", delta="+0.2 kW")
with col2:
    st.metric(label="Fator de Potência Médio", value="0.92 cos φ", delta="⚡ Dentro do Limite")
with col3:
    st.metric(label="Corrente Instantânea", value="68.6 A", delta="Estável")
with col4:
    st.metric(label="Fluxo de Água Atual", value="3.4 m³/h", delta="-0.2 m³/h (Economia)")

st.markdown("---")

# =========================================================================
# # SEÇÃO 1: ACOMPANHAMENTO DA GRANDEZA ELÉTRICA (CÓDIGO ORIGINAL)
# =========================================================================
st.subheader("⚡ 1. Acompanhamento de Grandezas Elétricas")

config_grandezas = {
    "Potência Ativa (kW)": {
        "titulo_y": "Potência Ativa (kW)", 
        "valores": [45.2, 46.1, 44.8, 45.5, 47.2, 45.0, 44.2, 45.9, 45.1, 45.3]
    },
    "Potência Aparente (kVA)": {
        "titulo_y": "Potência Aparente (kVA)", 
        "valores": [49.1, 50.2, 48.9, 49.6, 51.3, 49.0, 48.1, 49.9, 49.0, 49.2]
    },
    "Fator de Potência": {
        "titulo_y": "Fator de Potência (cos φ)", 
        "valores": [0.92, 0.92, 0.91, 0.91, 0.92, 0.91, 0.92, 0.92, 0.92, 0.92]
    },
    "Corrente (A)": {
        "titulo_y": "Corrente Nominal (A)", 
        "valores": [68.5, 69.8, 67.9, 68.9, 71.5, 68.2, 67.0, 69.5, 68.3, 68.6]
    }
}

grandeza_selecionada = st.selectbox(
    "Selecione a grandeza elétrica para acompanhamento no gráfico:",
    list(config_grandezas.keys())
)

dados_grandeza = config_grandezas[grandeza_selecionada]

horarios_eixo = pd.date_range(start='2026-06-29 08:00', periods=10, freq='15min')

dados_eletricos = pd.DataFrame({
    'Tempo': horarios_eixo,
    'Valor': dados_grandeza["valores"]
})

grafico_eletrico = alt.Chart(dados_eletricos).mark_line(color='#1f77b4', point=True).encode(
    x=alt.X('Tempo:T', 
            title='Horário da Leitura',
            axis=alt.Axis(format='%H:%M', tickCount='minute', values=list(dados_eletricos['Tempo']))),
    y=alt.Y('Valor:Q', title=dados_grandeza["titulo_y"], scale=alt.Scale(zero=False)),
    tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Horário'), alt.Tooltip('Valor:Q', title=grandeza_selecionada)]
).properties(height=300)

st.altair_chart(grafico_eletrico, use_container_width=True)

st.markdown("---")

# =========================================================================
# # SEÇÃO 2: NOVO GRÁFICO DE MEDIÇÃO DE ÁGUA ADICIONADO ABAIXO
# =========================================================================
st.subheader("💧 2. Histórico de Consumo de Água (m³)")

dados_agua = pd.DataFrame({
    'Tempo': horarios_eixo,
    'Consumo': [3.1, 3.4, 3.2, 3.5, 3.8, 3.4, 3.3, 3.6, 3.4, 3.4]
})

grafico_agua = alt.Chart(dados_agua).mark_line(color='#2563EB', point=True).encode(
    x=alt.X('Tempo:T', 
            title='Horário da Leitura',
            axis=alt.Axis(format='%H:%M', tickCount='minute', values=list(dados_agua['Tempo']))),
    y=alt.Y('Consumo:Q', title='Volume Consumido (m³)', scale=alt.Scale(zero=False)),
    tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Horário'), alt.Tooltip('Consumo:Q', title='Consumo (m³)')]
).properties(height=300)

st.altair_chart(grafico_agua, use_container_width=True)
