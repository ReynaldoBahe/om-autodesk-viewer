import streamlit as st

# 1. Configuração da Página Inicial
st.set_page_config(
    page_title="RB Gestão de Ativos",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicialização do estado de login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 3. Tela de Login Manual Estruturada
if not st.session_state["logged_in"]:
    st.title("🔑 Portal de Acesso - Gestão de Ativos")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        usuario = st.text_input("Usuário:")
        senha = st.text_input("Senha:", type="password")
        botao_entrar = st.button("Acessar System", use_container_width=True)
        
        if botao_entrar:
            usuarios_validos = {
                "admin": "RB_eng_admin_2026!",
                "fiat": "Fiat_Ativos_RB99*",
                "ambev": "Ambev_OM_RB2026#"
            }
            
            if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
                st.session_state["logged_in"] = True
                st.session_state["cliente_ativo"] = usuario.upper()
                st.rerun()
            else:
                st.error("❌ Credenciais inválidas. Tente novamente.")
else:
    # 4. ÁREA INTERNA: Executa a navegação clássica automática das páginas
    st.sidebar.title("Navegação")
    st.sidebar.markdown(f"👤 Conectado como: **{st.session_state['cliente_ativo']}**")
    
    # Adiciona botão de Logout na barra lateral
    st.sidebar.markdown("---")
    if st.sidebar.button("Sair da conta", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()
