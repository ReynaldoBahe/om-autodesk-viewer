import streamlit as st
import time

# --- CONTROLE DE SESSÃO INTERNO ---
if "login_step" not in st.session_state:
    st.session_state.login_step = 1
if "usuario_validado" not in st.session_state:
    st.session_state.usuario_validado = ""

# --- BANCO DE DADOS DINÂMICO VIA CONFIG (SECRETS) ---
try:
    lista_usuarios = st.secrets["users"]
except KeyError:
    # Caso rode localmente sem o arquivo configurado
    lista_usuarios = {
        "gerente.om@resortboaviagem.com": {"password": "SenhaResort123", "token": "852369", "cliente": "Resort Boa Viagem"}
    }

# --- INJEÇÃO DE CSS REFORMULADO (PREMIUM FLAT GRADIENT) ---
st.markdown("""
    <style>
        /* 1. Fundo em degradê moderno que traz iluminação para o centro da tela */
        .stApp { 
            background: linear-gradient(135deg, #07162c 0%, #1b355a 50%, #07162c 100%) !important; 
            color: #FFFFFF; 
        }
        
        .left-panel { padding: 40px 20px; text-align: center; }
        
        /* 2. Emblema da marca com brilho neon suave */
        .dt-badge { 
            background: linear-gradient(135deg, #11375c 0%, #1e5286 100%); 
            border-radius: 50%; 
            width: 100px; 
            height: 100px; 
            line-height: 100px; 
            margin: 0 auto 20px auto; 
            font-weight: bold; 
            color: #00D2FF; 
            box-shadow: 0 0 25px rgba(0, 210, 255, 0.4); 
            border: 1px solid rgba(0, 210, 255, 0.3);
        }
        
        .dt-title { font-size: 14px; letter-spacing: 2px; color: #9EBBDE; margin-bottom: 5px; font-weight: 600; }
        .main-brand { font-size: 46px; font-weight: 900; color: #FFFFFF; margin-bottom: 15px; line-height: 1; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
        .sub-brand { font-size: 13px; letter-spacing: 3px; color: #00D2FF; font-weight: bold; margin-bottom: 25px; }
        .slogan { font-style: italic; color: #D1E2F4; font-size: 15px; margin-bottom: 30px; }
        
        /* 3. Card de Login translúcido (Glassmorphism) que clareia a área de foco */
        .login-card { 
            background-color: rgba(255, 255, 255, 0.04); 
            padding: 35px; 
            border-radius: 16px; 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            backdrop-filter: blur(12px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.4); 
        }
        
        .login-title { font-size: 28px; font-weight: bold; color: #FFFFFF; text-align: center; margin-bottom: 5px; }
        .login-subtitle { font-size: 14px; color: #BACCDA; text-align: center; margin-bottom: 30px; }
        
        /* 4. Caixas de entrada brancas (padrão de mercado) para contraste impecável e fim da tela escura */
        div[data-baseweb="input"] { 
            background-color: #FFFFFF !important; 
            border: 1px solid #CBD5E1 !important; 
            border-radius: 8px !important; 
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05) !important;
        }
        
        /* Cor do texto digitado interna mudou para azul escuro corporativo */
        input { color: #0F172A !important; font-weight: 500 !important; }
        input::placeholder { color: #94A3B8 !important; }
        
        label { color: #E2E8F0 !important; font-weight: 600 !important; font-size: 14px !important; margin-bottom: 4px; }
        
        .top-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
        
        .resort-badge { 
            background: rgba(255, 255, 255, 0.06); 
            padding: 6px 14px; 
            border-radius: 20px; 
            font-weight: bold; 
            font-size: 13px; 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(5px);
        }
        
        .verified-badge { 
            background: rgba(0,210,255,0.12); 
            color: #00D2FF; 
            padding: 6px 14px; 
            border-radius: 20px; 
            font-size: 12px; 
            border: 1px solid rgba(0,210,255,0.25); 
            font-weight: 600;
        }
        
        .ssl-footer { color: #9EBBDE; font-size: 12px; margin-top: 20px; display: flex; align-items: center; gap: 6px; justify-content: center; opacity: 0.8; }
    </style>
""", unsafe_allow_html=True)

# --- DIVISÃO DA INTERFACE EM 2 COLUNAS ---
col_esquerda, col_direita = st.columns([1.1, 1.0], gap="large")

with col_esquerda:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)
    st.markdown('<div class="dt-badge">DT<br><span style="font-size:10px;">Facilities</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="dt-title">DT FACILITIES</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-brand">O&M</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-brand">GESTÃO INTELIGENTE DE ATIVOS</div>', unsafe_allow_html=True)
    st.markdown('<div class="slogan">"Seu patrimônio sob controle, onde você estiver."</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px; color:#9EBBDE; word-spacing: 10px; font-weight:500;">Hospital • Resort • Supermercado • Facilities</p>', unsafe_allow_html=True)
    st.markdown('<div class="ssl-footer" style="justify-content:flex-start; margin-top:60px;">🔒 Conexão segura SSL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_direita:
    # Identifica dinamicamente o contexto visual se o usuário já inseriu o e-mail na Etapa 1
    nome_cliente = "Acesso Uniforme"
    if st.session_state.login_step == 2 and st.session_state.usuario_validado in lista_usuarios:
        nome_cliente = lista_usuarios[st.session_state.usuario_validado]["cliente"]

    st.markdown('<div class="top-header">', unsafe_allow_html=True)
    st.markdown(f'<div class="resort-badge">🏢 {nome_cliente}</div>', unsafe_allow_html=True)
    st.markdown('<div class="verified-badge">✓ Cliente verificado</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # --- ETAPA 1: LOGIN E SENHA ---
    if st.session_state.login_step == 1:
        st.markdown('<div class="login-title">Acesse sua conta</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Entre com seu e-mail e senha</div>', unsafe_allow_html=True)
        
        with st.form("form_etapa_1", clear_on_submit=False):
            email = st.text_input("E-mail", placeholder="seu.email@email.com")
            senha = st.text_input("Senha", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("🔵 **Verificação em 2 etapas:** Um código será enviado ao seu e-mail.")
            
            if st.form_submit_button("Entrar", use_container_width=True):
                if email in lista_usuarios and senha == lista_usuarios[email]["password"]:
                    st.session_state.usuario_validado = email
                    st.session_state.login_step = 2
                    st.rerun()
                else:
                    st.error("Credenciais inválidas para o ecossistema multi-cliente.")

    # --- ETAPA 2: TOKEN DE SEGURANÇA ---
    elif st.session_state.login_step == 2:
        st.markdown('<div class="login-title">Verificação</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Insira o código de segurança</div>', unsafe_allow_html=True)
        
        with st.form("form_etapa_2", clear_on_submit=False):
            codigo = st.text_input("Código de 6 dígitos", max_chars=6, placeholder="000000")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.form_submit_button("Voltar", use_container_width=True):
                    st.session_state.login_step = 1
                    st.rerun()
            with col_b2:
                if st.form_submit_button("Confirmar", use_container_width=True):
                    user_info = lista_usuarios[st.session_state.usuario_validado]
                    if codigo == user_info["token"]:
                        st.success("Acesso authorized!")
                        time.sleep(0.5)
                        
                        st.session_state.logged_in = True
                        st.session_state.cliente_ativo = user_info["cliente"]
                        st.session_state.user_email = st.session_state.usuario_validado
                        
                        st.session_state.login_step = 1
                        st.rerun()
                    else:
                        st.error("Código incorreto.")
                        
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssl-footer">🔒 Conexão segura SSL <span style="color:#BACCDA; margin-left:20px;">© 2026 DT Facilities O&M</span></div>', unsafe_allow_html=True)
