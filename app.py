import streamlit as st

# 1. Configuração da página (Centralizada para o card flutuar no meio)
st.set_page_config(page_title="RB Consultoria", page_icon="🏢", layout="centered")

# Estilização CSS Avançada: Imagem de Fundo Completa e Card Flutuante
st.markdown("""
    <style>
    /* Injeta a imagem industrial no fundo da tela inteira */
    .stApp {
        background-image: linear-gradient(rgba(14, 30, 56, 0.45), rgba(14, 30, 56, 0.45)), 
                          url('https://unsplash.com');
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }
    
    /* Remove cabeçalhos e paddings do Streamlit para focar no login */
    [data-testid="stHeader"] { background: transparent !important; }
    .block-container { padding-top: 6rem !important; max-width: 460px !important; }
    
    /* Customização interna dos inputs do formulário */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Customização Premium do Botão de Login */
    div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #1a365d 0%, #2a4365 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 0px !important;
        font-size: 16px !important;
        box-shadow: 0 4px 12px rgba(26, 54, 93, 0.3);
        transition: all 0.3s ease;
    }
    div.stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(26, 54, 93, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Inicializa as variáveis de controle de login globais
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cliente_ativo" not in st.session_state:
    st.session_state.cliente_ativo = ""

# 3. Definição das Páginas do Sistema utilizando st.Page
pagina_login = st.Page("app.py", title="Acesso ao Sistema", icon="🔒", default=True)
pagina_home = st.Page("pages/01_Home.py", title="Home", icon="🏠")
pagina_engenharia = st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="⚙️")
pagina_manutencao = st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="🛠️")
pagina_indicadores = st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="📊")
pagina_telemetria = st.Page("pages/04_Telemetria_em_Tempo_Real.py", title="Telemetria em Tempo Real", icon="⚡")

# Gerenciador de Navegação Dinâmica
if st.session_state.logged_in:
    paginas_disponiveis = [pagina_home, pagina_engenharia, pagina_manutencao, pagina_indicadores, pagina_telemetria]
else:
    paginas_disponiveis = [pagina_login]

pg = st.navigation(paginas_disponiveis)

# =========================================================================
# LÓGICA DE RENDERIZAÇÃO DAS TELAS
# =========================================================================
if not st.session_state.logged_in:
    
    # Card Flutuante Centralizado contendo a marca e o formulário
    # Ele usa a estrutura nativa de container em caixa do Streamlit para manter os inputs 100% integrados
    with st.container(border=True):
        
        # Cabeçalho Interno do Card
        st.markdown("""
            <div style='text-align: center; padding-bottom: 10px;'>
                <h2 style='color: #1a365d; font-weight: 800; margin-bottom: 0px; letter-spacing: 1px;'>RB CONSULTORIA</h2>
                <p style='color: #4a5568; font-size: 14px; font-weight: 500; margin-top: 5px;'>Gestão Estratégica de Ativos</p>
                <hr style='margin-top: 15px; margin-bottom: 15px; border-color: #e2e8f0;'>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulário de Credenciais perfeitamente envelopado
        with st.form("menu_login_final"):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário corporativo")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            lembrar = st.checkbox("Lembrar de mim")
            
            st.markdown("<br>", unsafe_allow_html=True)
            botao_entrar = st.form_submit_button("Acessar Painel", use_container_width=True)
            
        if botao_entrar:
            usuarios_validos = {
                "admin": "admin",
                "fiat": "fiat123",
                "ambev": "ambev123"
            }
            
            if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
                st.session_state.logged_in = True
                st.session_state.cliente_ativo = usuario.upper()
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos.")

else:
    # Se já estiver logado, renderiza a página ativa do menu lateral
    pg.run()
    
    # Inclui o botão de Logout na barra lateral logada
    with st.sidebar:
        st.markdown("---")
        if st.button("Sair da Conta", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
