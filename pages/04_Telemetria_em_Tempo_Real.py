# =========================================================================
# # ESTRUTURAÇÃO DOS DADOS REAIS DE TELEMETRIA
# =========================================================================
# Geramos o vetor de horários de 15 em 15 minutos
horarios_eixo = pd.date_range(start='2026-06-29 08:00', periods=10, freq='15min')

# Captura de forma automática o último horário registrado na lista (ex: 10:15)
ultimo_horario_dt = horarios_eixo[-1]
horario_formatado = ultimo_horario_dt.strftime('%H:%M')

# Dados fixos das grandezas para indexação
valores_potencia = [45.2, 46.1, 44.8, 45.5, 47.2, 45.0, 44.2, 45.9, 45.1, 45.3]
valores_fp = [0.92, 0.92, 0.91, 0.91, 0.92, 0.91, 0.92, 0.92, 0.92, 0.92]
valores_corrente = [68.5, 69.8, 67.9, 68.9, 71.5, 68.2, 67.0, 69.5, 68.3, 68.6]
valores_agua = [3.1, 3.4, 3.2, 3.5, 3.8, 3.4, 3.3, 3.6, 3.4, 3.4]

# Puxa o último valor de cada lista dinamicamente
potencia_instantanea = valores_potencia[-1]
fp_instantaneo = valores_fp[-1]
corrente_instantanea = valores_corrente[-1]
agua_instantanea = valores_agua[-1]

# Exibe o carimbo de data/hora oficial das medições do topo
st.info(f"⏱️ **Última Atualização dos Sensores:** Medição realizada em tempo real às **{horario_formatado}**.")

# =========================================================================
# # METRICS DE TELEMETRIA AUTOMATIZADOS COM O ÚLTIMO HORÁRIO
# =========================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Potência Ativa Atual", value=f"{potencia_instantanea} kW", delta="+0.2 kW")
with col2:
    st.metric(label="Fator de Potência Médio", value=f"{fp_instantaneo} cos φ", delta="⚡ Dentro do Limite")
with col3:
    st.metric(label="Corrente Instantânea", value=f"{corrente_instantanea} A", delta="Estável")
with col4:
    st.metric(label="Fluxo de Água Atual", value=f"{agua_instantanea} m³/h", delta="-0.2 m³/h (Economia)")
