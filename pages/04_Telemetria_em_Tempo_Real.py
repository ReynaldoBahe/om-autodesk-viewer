import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Telemetria em Tempo Real", page_icon="📊", layout="wide")

# =========================================================================
# 🔒 TRAVA DE SEGURANÇA INTEGRADA AO SEU PORTAL
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, faça o login na página inicial.")
    st.stop()

nome_cliente = st.session_state.get("cliente_ativo", "Cliente")

st.markdown(f'<h2 style="color: #1E3A8A;">📊 Telemetria de Ativos & Utilidades — {nome_cliente}</h2>', unsafe_allow_html=True)
st.write("Monitoramento contínuo, histórico de grandezas elétricas e consumo integrado por período.")

st.markdown("---")

# =========================================================================
# # DATA E ESTRUTURAÇÃO DOS SENSORES (CCK90)
# =========================================================================
horarios_eixo = pd.date_range(start='2026-06-29 08:00', periods=10, freq='15min')
ultimo_horario_dt = horarios_eixo[-1]
horario_formatado = ultimo_horario_dt.strftime('%H:%M')

valores_potencia = [45.2, 46.1, 44.8, 45.5, 47.2, 45.0, 44.2, 45.9, 45.1, 45.3]
valores_fp = [0.92, 0.92, 0.91, 0.91, 0.92, 0.91, 0.92, 0.92, 0.92, 0.92]
valores_corrente = [68.5, 69.8, 67.9, 68.9, 71.5, 68.2, 67.0, 69.5, 68.3, 68.6]
valores_energia_kwh = [11.3, 11.5, 11.2, 11.4, 11.8, 11.2, 11.0, 11.5, 11.3, 11.3]
valores_agua_m3 = [0.3, 0.4, 0.2, 0.5, 0.8, 0.4, 0.3, 0.6, 0.4, 0.4]

potencia_instantanea = valores_potencia[-1]
fp_instantaneo = valores_fp[-1]
corrente_instantanea = valores_corrente[-1]
fluxo_agua_instantaneo = 3.4 

st.info(f"⏱️ **Última Atualização dos Sensores:** Medições registradas e consolidadas às **{horario_formatado}**.")

# =========================================================================
# 📈 CARTÕES DE MÉTRICAS (OS QUATRO ELEMENTOS DO TOPO)
# =========================================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Potência Ativa Atual", value=f"{potencia_instantanea} kW", delta="+0.2 kW")
with col2:
    st.metric(label="Fator de Potência Médio", value=f"{fp_instantaneo} cos φ", delta="⚡ Dentro do Limite")
with col3:
    st.metric(label="Corrente Instantânea", value=f"{corrente_instantanea} A", delta="Estável")
with col4:
    st.metric(label="Fluxo de Água Atual", value=f"{fluxo_agua_instantaneo} m³/h", delta="-0.2 m³/h (Economia)")

st.markdown("---")

# =========================================================================
# ⚡ SEÇÃO 1: ACOMPANHAMENTO DA GRANDEZA SELECIONADA (LINHA)
# =========================================================================
st.subheader("⚡ 1. Acompanhamento de Grandezas Elétricas (Instantâneas)")

config_grandezas = {
    "Potência Ativa (kW)": {"titulo_y": "Potência Ativa (kW)", "valores": valores_potencia},
    "Potência Aparente (kVA)": {"titulo_y": "Potência Aparente (kVA)", "valores": [49.1, 50.2, 48.9, 49.6, 51.3, 49.0, 48.1, 49.9, 49.0, 49.2]},
    "Fator de Potência": {"titulo_y": "Fator de Potência (cos φ)", "valores": valores_fp},
    "Corrente (A)": {"titulo_y": "Corrente Nominal (A)", "valores": valores_corrente}
}

# A janela suspensa que você validou:
grandeza_selecionada = st.selectbox(
    "Selecione a grandeza elétrica instantânea para o gráfico de linhas:",
    list(config_grandezas.keys())
)

dados_grandeza = config_grandezas[grandeza_selecionada]
dados_eletricos = pd.DataFrame({'Tempo': horarios_eixo, 'Valor': dados_grandeza["valores"]})

grafico_eletrico = alt.Chart(dados_eletricos).mark_line(color='#1f77b4', point=True).encode(
    x=alt.X('Tempo:T', title='Horário da Leitura', axis=alt.Axis(format='%H:%M', values=list(dados_eletricos['Tempo']))),
    y=alt.Y('Valor:Q', title=dados_grandeza["titulo_y"], scale=alt.Scale(zero=False)),
    tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Horário'), alt.Tooltip('Valor:Q', title=grandeza_selecionada)]
).properties(height=280)

st.altair_chart(grafico_eletrico, use_container_width=True)

st.markdown("---")

# =========================================================================
# 📊 SEÇÃO 2: CONSUMO ACUMULADO POR PERÍODO (RODAPÉ)
# =========================================================================
st.subheader("📊 2. Consumo Acumulado por Período de Medição (15 Minutos)")
col_esq, col_dir = st.columns(2)

with col_esq:
    st.markdown("🔌 **Consumo de Energia Ativa (kWh)**")
    dados_energia_periodo = pd.DataFrame({'Tempo': horarios_eixo, 'Consumo': valores_energia_kwh})
    grafico_energia_barra = alt.Chart(dados_energia_periodo).mark_bar(color='#F59E0B', cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X('Tempo:T', title='Período', axis=alt.Axis(format='%H:%M', values=list(dados_energia_periodo['Tempo']))),
        y=alt.Y('Consumo:Q', title='Energia Consumida (kWh)'),
        tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Período'), alt.Tooltip('Consumo:Q', title='Energia (kWh)')]
    ).properties(height=250)
    st.altair_chart(grafico_energia_barra, use_container_width=True)

with col_dir:
    st.markdown("💧 **Consumo de Volume Hídrico (m³)**")
    dados_agua_periodo = pd.DataFrame({'Tempo': horarios_eixo, 'Consumo': valores_agua_m3})
    grafico_agua_barra = alt.Chart(dados_agua_periodo).mark_bar(color='#2563EB', cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X('Tempo:T', title='Período', axis=alt.Axis(format='%H:%M', values=list(dados_agua_periodo['Tempo']))),
        y=alt.Y('Consumo:Q', title='Volume Consumido (m³)'),
        tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Período'), alt.Tooltip('Consumo:Q', title='Volume (m³)')]
    ).properties(height=250)
    st.altair_chart(grafico_agua_barra, use_container_width=True)
