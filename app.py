import streamlit as st

# 1. Configuração da página em modo AMPLO (Wide) para ocupar a tela toda
st.set_page_config(page_title="RB Consultoria", page_icon="🏢", layout="wide")

# Estilização CSS Avançada para criar o visual de Portal Corporativo
st.markdown("""
    <style>
    /* Remove margens padrão do Streamlit para colar os blocos */
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    
    /* Banner da Esquerda */
    .banner-esquerda {
        background: linear-gradient(135deg, #0e1e38 0%, #1a365d 100%);
        color: #ffffff;
        padding: 60px;
        border-radius: 16px;
        min-height: 550px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* Card de Login da Direita */
    .card-login {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        min-height: 550px;
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
    
    # Criamos um container com margem para não colar nas bordas do monitor
    with st.container():
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Divisão em duas colunas largas e imponentes (Proporção 5 para 4)
        col_logo, col_login = st.columns([5, 4], gap="large")
        
        # -----------------------------------------------------------------
        # COLUNA DA ESQUERDA: Banner Corporativo Premium
        # -----------------------------------------------------------------
        with col_logo:
            st.markdown("""
                <div class="banner-esquerda">
                    <h1 style='font-size: 42px; font-weight: 800; margin-bottom: 10px; color: #fff;'>RB CONSULTORIA</h1>
                    <h3 style='color: #63b3ed; font-weight: 400; margin-bottom: 30px;'>Gestão Estratégica de Ativos</h3>
                    <p style='font-size: 16px; line-height: 1.6; color: #e2e8f0;'>
                        Bem-vindo ao portal integrado de Engenharia e O&M. 
                        Acesse para monitorar métricas operacionais, telemetria em tempo real 
                        e diagnósticos prescritivos por Inteligência Preditiva.
                    </p>
                    <br><br>
                    <small style='color: #a0aec0;'>© 2026 RB Consultoria Engenharia. Todos os direitos reservados.</small>
                </div>
            """, unsafe_allow_html=True)
            
        # -----------------------------------------------------------------
        # COLUNA DA DIREITA: Formulário Clean e Destacado
        # -----------------------------------------------------------------
        with col_login:
            st.markdown('<div class="card-login">', unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #1a202c; font-weight: 700; margin-bottom: 5px;'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #718096; margin-bottom: 30px;'>Insira suas credenciais corporativas.</p>", unsafe_allow_html=True)
            
            # Formulário nativo do Streamlit dentro da nossa div estilizada
            with st.form("formulario_login"):
                usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
                senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
                lembrar = st.checkbox("Lembrar de mim")
                
                st.markdown("<br>", unsafe_allow_html=True)
                botao_entrar = st.form_submit_button("Entrar no Portal", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# LÓGICA DE RENDERIZAÇÃO DAS TELAS
# =========================================================================
if not st.session_state.logged_in:
    
    # Criamos duas colunas de tamanhos iguais (1 para logo, 1 para formulário)
    col_logo, col_login = st.columns(2, gap="large")
    
    # -----------------------------------------------------------------
    # COLUNA DA ESQUERDA: Logomarca e Boas-Vindas
    # -----------------------------------------------------------------
    with col_logo:
        st.markdown("<br><br>", unsafe_allow_html=True) # Espaçamento para alinhar verticalmente
        # Substitua a URL abaixo pelo link real da imagem da sua logomarca
        st.image("https://placeholder.com", use_container_width=True)
        st.markdown("""
            <div style='text-align: center; margin-top: 20px;'>
                <h3>Gestão Estratégica de Ativos</h3>
                <p style='color: gray;'>Painel integrado de Engenharia, Manutenção e Telemetria Operacional.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # -----------------------------------------------------------------
    # COLUNA DA DIREITA: Formulário de Acesso
    # -----------------------------------------------------------------
    with col_login:
        st.markdown("<h2 style='text-align: center;'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Insira suas credenciais para acessar.</p>", unsafe_allow_html=True)
        
        # Formulário estruturado e seguro em caixa
        with st.form("formulario_login"):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            lembrar = st.checkbox("Lembrar de mim")
            
            # Botão de submissão do formulário
            botao_entrar = st.form_submit_button("Entrar", use_container_width=True)
