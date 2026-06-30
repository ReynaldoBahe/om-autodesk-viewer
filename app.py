import streamlit as st

# 1. Configuração da página (Deve ser a primeira linha)
st.set_page_config(page_title="RB Consultoria", page_icon="🏢", layout="centered")

# 2. Inicializa as variáveis de controle de login globais
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cliente_ativo" not in st.session_state:
    st.session_state.cliente_ativo = ""

# 3. Definição das Páginas do Sistema utilizando st.Page
# O primeiro parâmetro é o caminho real do arquivo dentro da pasta 'pages/'
pagina_login = st.Page("app.py", title="Acesso ao Sistema", icon="🔒", default=True)
pagina_home = st.Page("pages/01_Home.py", title="Home", icon="🏠")
pagina_engenharia = st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="⚙️")
pagina_manutencao = st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="🛠️")
pagina_indicadores = st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="📊")
pagina_telemetria = st.Page("pages/04_Telemetria_em_Tempo_Real.py", title="Telemetria em Tempo Real", icon="⚡")

# =========================================================================
# 🧭 GERENCIADOR DE NAVEGAÇÃO DINÂMICA
# =========================================================================
if st.session_state.logged_in:
    # Se o usuário ESTIVER LOGADO, ele enxerga o menu completo
    paginas_disponiveis = [pagina_home, pagina_engenharia, pagina_manutencao, pagina_indicadores, pagina_telemetria]
else:
    # Se o usuário NÃO ESTIVER LOGADO, a barra lateral mostra apenas a tela de Login
    paginas_disponiveis = [pagina_login]

# Inicializa a navegação oficial controlada pelo script
pg = st.navigation(paginas_disponiveis)


# =========================================================================
# LÓGICA DE RENDERIZAÇÃO DAS TELAS
# =========================================================================
if not st.session_state.logged_in:
    
    # Título centralizado sem emojis problemáticos
    st.markdown("<h2 style='text-align: center;'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Insira suas credenciais para acessar o painel de engenharia e O&M.</p>", unsafe_allow_html=True)
    
    # Formulário estruturado e seguro em caixa
    with st.form("formulario_login"):
        usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        lembrar = st.checkbox("Lembrar de mim")
        
        # Botão de submissão do formulário
        botao_entrar = st.form_submit_button("Entrar", use_container_width=True)

    # Processamento do clique no botão
    if botao_entrar:
        # Banco de dados temporário para validação
        usuarios_validos = {
            "admin": "admin",
            "fiat": "fiat123",
            "ambev": "ambev123"
        }
        
        if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
            # Ativa a ponte de segurança global na sessão
            st.session_state.logged_in = True
            st.session_state.cliente_ativo = usuario.upper()
            st.rerun() # Recarrega a página para aplicar o acesso liberado
        else:
            st.error("❌ Usuário ou senha incorretos. Verifique suas credenciais.")

else:
    # Caso o usuário já esteja autenticado, executa a página selecionada no menu lateral
    pg.run()
