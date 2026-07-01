import streamlit as st

# 1. Configuração inicial obrigatória do ecossistema
st.set_page_config(page_title="Portal RB Engenharia", page_icon="🏗️", layout="wide")

# Inicializa as variáveis de sessão se não existirem
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 2. DEFINIÇÃO DAS PÁGINAS DO MENU (O segredo para mantê-las fixas à esquerda)
paginas_do_portal = [
    st.Page("pages/01_Home.py", title="Home", icon="🏠"),
    st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="⚙️"),
    st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="🔧"),
    st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="📊"),
    st.Page("pages/04_Telemetria_em_Tempo_Real.py", title="Telemetria em Tempo Real", icon="⚡"),
    st.Page("pages/05_Tour_Virtual.py", title="Tour Virtual", icon="📸"),
    st.Page("pages/06_Portal_CMMS.py", title="Portal CMMS", icon="🛠️")
]

# 3. FLUXO DE SEGURANÇA E RENDERIZAÇÃO DA INTERFACE
if not st.session_state.logged_in:
    
    # =========================================================================
    # REGRAS DO SEU LOGIN ORIGINAL (Colunas, Imagem Decorativa e Estilo)
    # =========================================================================
    col_imagem, col_formulario = st.columns([1, 1.2]) # Mantém a divisão clássica do seu design
    
    with col_imagem:
        # Link ou caminho da imagem corporativa técnica que ficava na esquerda da sua tela
        st.image("https://githubusercontent.com", use_container_width=True) 

    with col_formulario:
        st.markdown('<h2 style="color: #1E3A8A; font-weight: bold; margin-bottom: 20px;">Acesso ao Portal RB Consultoria</h2>', unsafe_allow_html=True)
        
        # Campos de entrada limpos
        usuario = st.text_input("Usuário ou E-mail Corporativo:")
        senha = st.text_input("Senha de Acesso:", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão de entrada estilizado no padrão original
        if st.button("Entrar no Sistema", use_container_width=True):
            if usuario == "ADMIN" and senha == "1234": # Ajuste para as suas credenciais reais
                st.session_state.logged_in = True
                st.session_state.cliente_ativo = "ADMIN"
                st.rerun()
            else:
                st.error("❌ Credenciais incorretas. Por favor, tente novamente.")
else:
    # Quando logado, roda o gerenciador que exibe a barra lateral com as 6 abas completas
    navegacao = st.navigation(paginas_do_portal)
    navegacao.run()
