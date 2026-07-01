import streamlit as st

# Se passou da trava do app.py, carrega o nome do cliente autenticado
nome_cliente = st.session_state.get("cliente_ativo", "Cliente")

st.markdown(f'<h1 style="color: #1E3A8A;">🏗️ Portal de Engenharia & Gestão de Ativos</h1>', unsafe_allow_html=True)
st.markdown(f"### Bem-vindo ao centro operacional de O&M, **{nome_cliente}**!")
st.write("Esta plataforma centraliza o controle de manutenção, monitoramento energético e indicadores de performance.")

st.markdown("---")

st.subheader("📁 Conheça os Módulos Operacionais")
st.write("Utilize o menu lateral esquerdo para navegar pelas ferramentas disponíveis:")

# =========================================================================
# LINHA 1 DE MÓDULOS (Existentes)
# =========================================================================
col_esq1, col_dir1 = st.columns(2)

with col_esq1:
    st.markdown("### ⚡ Engenharia & Telemetria")
    st.info(
        "**Módulos de Engenharia & Telemetria em Tempo Real**\n\n"
        "Acompanhe as grandezas elétricas críticas (Potência, Corrente, Fator de Potência) "
        "e monitore o consumo integrado de energia (kWh) e água (m³) em intervalos de 15 minutos."
    )

with col_dir1:
    st.markdown("### 🔧 Gestão & Indicadores")
    st.success(
        "**Gestão da Manutenção & Indicadores de Tempo**\n\n"
        "Controle ordens de serviço, cronogramas de manutenção preventiva/corretiva "
        "e analise os principais KPIs de eficiência e disponibilidade da planta."
    )

# =========================================================================
# LINHA 2 DE MÓDULOS (Novas Implementações Integradas ao Padrão Visual)
# =========================================================================
col_esq2, col_dir2 = st.columns(2)

with col_esq2:
    st.markdown("### 📸 Inspeção Visual")
    st.info(
        "**Tour Virtual e Modelagem 360°**\n\n"
        "Navegue interativamente pelas plantas e subestações do ativo "
        "através de registros fotográficos equirretangulares imersivos."
    )

with col_dir2:
    st.markdown("### 🛠️ Operação Ativa")
    st.success(
        "**Portal CMMS Operacional**\n\n"
        "Abra chamados emergenciais, emita Ordens de Serviço (OS) e "
        "acompanhe em tempo real o status das manutenções planejadas."
    )

st.markdown("---")
st.caption("ℹ️ Sistema de Telemetria e Gestão — Versão 1.0 | Acesso Restrito e Seguro.")
