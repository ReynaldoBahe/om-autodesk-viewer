import streamlit as st

st.set_page_config(page_title="Home - RB Consultoria", page_icon="🏠", layout="wide")


# =========================================================================
# 🔒 TRAVA DE SEGURANÇA (Primeira linha obrigatória do arquivo)
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, faça o login na página inicial.")
    st.stop()

# Se passou da trava, o sistema descobre quem é o cliente logado
nome_cliente = st.session_state.get("cliente_ativo", "Cliente")

# =========================================================================
# 🏛️ INTERFACE VISUAL DA HOME (O "Cartão de Visitas" do seu Portal)
# =========================================================================
st.markdown(f'<h1 style="color: #1E3A8A;">🏗️ Portal de Engenharia & Gestão de Ativos</h1>', unsafe_allow_html=True)
st.markdown(f"### Bem-vindo ao centro operacional de O&M, **{nome_cliente}**!")
st.write("Esta plataforma centraliza o controle de manutenção, monitoramento energético e indicadores de performance.")

st.markdown("---")

st.subheader("📁 Conheça os Módulos Operacionais")
st.write("Utilize os blocos abaixo ou o menu lateral esquerdo para navegar pelas ferramentas disponíveis:")

# Linha 1 de Módulos (Existentes)
col_esq, col_dir = st.columns(2)

with col_esq:
    st.markdown("### ⚡ Engenharia & Telemetria")
    st.info(
        "**Módulos de Engenharia & Telemetria em Tempo Real**\n\n"
        "Acompanhe as grandezas elétricas críticas (Potência, Corrente, Fator de Potência) "
        "e monitore o consumo integrado de energia (kWh) e água (m³) em intervalos de 15 minutos."
    )

with col_dir:
    st.markdown("### 🔧 Gestão & Indicadores")
    st.success(
        "**Gestão da Manutenção & Indicadores de Tempo**\n\n"
        "Controle ordens de serviço, cronogramas de manutenção preventiva/corretiva "
        "e analise os principais KPIs de eficiência e disponibilidade da planta."
    )

# Linha 2 de Módulos (Novas Implementações)
col_novas1, col_novas2 = st.columns(2)

with col_novas1:
    st.markdown("### 📸 Inspeção Visual")
    st.info(
        "**Tour Virtual e Modelagem 360°**\n\n"
        "Navegue interativamente pelas plantas e subestações do ativo "
        "através de registros fotográficos equirretangulares imersivos."
    )
    if st.button("Abrir Tour Virtual 📸", use_container_width=True):
        st.switch_page("pages/05_Tour_Virtual.py")

with col_novas2:
    st.markdown("### 🛠️ Operação Ativa")
    st.success(
        "**Portal CMMS Operacional**\n\n"
        "Abra chamados emergenciais, emita Ordens de Serviço (OS) e "
        "acompanhe em tempo real o status das manutenções planejadas."
    )
    if st.button("Abrir Portal CMMS 🛠️", use_container_width=True):
        st.switch_page("pages/06_Portal_CMMS.py")

st.markdown("---")
st.caption("ℹ️ Sistema de Telemetria e Gestão — Versão 1.0 | Acesso Restrito e Seguro.")
