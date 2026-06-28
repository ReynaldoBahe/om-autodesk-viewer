import streamlit as st
import time
import random
import string

# ─────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="DT Facilities O&M",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# BANCO DE USUÁRIOS (substitua por banco real)
# ─────────────────────────────────────────
USUARIOS = {
    "admin@resortoceano.com": {
        "senha": "dt2026",
        "empreendimento": "Resort Oceano Azul",
        "iniciais": "RO",
        "ultimo_acesso": "27/06/2026 às 09:14"
    },
    "admin@hospitalsl.com": {
        "senha": "dt2026",
        "empreendimento": "Complexo Hospitalar São Lucas",
        "iniciais": "SL",
        "ultimo_acesso": "28/06/2026 às 07:30"
    },
    "admin@resortboaviagem.com": {
        "senha": "dt2026",
        "empreendimento": "Resort Boa Viagem",
        "iniciais": "RV",
        "ultimo_acesso": "28/06/2026 às 08:45"
    },
}

# ─────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────
st.markdown("""
<style>
/* Remove padding padrão do Streamlit */
[data-testid="stAppViewContainer"] {
    padding: 0 !important;
}
[data-testid="stHeader"] {
    display: none;
}
[data-testid="stSidebar"] {
    display: none;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Layout principal */
.login-wrapper {
    display: flex;
    min-height: 100vh;
    width: 100%;
    font-family: 'Inter', sans-serif;
}

/* Lado esquerdo */
.login-left {
    flex: 1;
    background: #021628;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    position: relative;
    overflow: hidden;
}

.grid-bg {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(24,95,165,0.15) 1px, transparent 1px),
        linear-gradient(90deg, rgba(24,95,165,0.15) 1px, transparent 1px);
    background-size: 60px 60px;
}

.overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(2,22,40,0.6);
}

.left-content {
    position: relative;
    z-index: 10;
    text-align: center;
}

/* Ícone rede de ativos */
.network-icon {
    margin: 0 auto 32px;
}

/* Textos lado esquerdo */
.product-label {
    font-size: 11px;
    letter-spacing: 3px;
    color: #85B7EB;
    margin-bottom: 4px;
}
.product-name {
    font-size: 36px;
    font-weight: 800;
    color: white;
    letter-spacing: 2px;
    margin: 0;
    line-height: 1.1;
}
.product-divider {
    width: 200px;
    height: 1px;
    background: #185FA5;
    margin: 12px auto;
}
.product-subtitle {
    font-size: 10px;
    letter-spacing: 2px;
    color: #85B7EB;
    margin-bottom: 20px;
}
.product-tagline {
    font-size: 13px;
    color: #378ADD;
    font-style: italic;
    line-height: 1.6;
    margin-bottom: 28px;
}
.segments {
    font-size: 10px;
    color: #185FA5;
    letter-spacing: 1px;
}

/* Lado direito */
.login-right {
    width: 440px;
    min-width: 380px;
    background: #042C53;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 32px;
}

/* Badge boas-vindas */
.welcome-badge {
    width: 100%;
    background: #031525;
    border: 0.5px solid #0C447C;
    border-radius: 10px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}
.welcome-avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #185FA5;
    color: white;
    font-size: 13px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.welcome-text small {
    font-size: 10px;
    color: #85B7EB;
    display: block;
}
.welcome-text strong {
    font-size: 13px;
    color: white;
    display: block;
}
.welcome-text span {
    font-size: 9px;
    color: #378ADD;
}

/* Card login */
.login-card {
    width: 100%;
    background: #031525;
    border: 0.5px solid #0C447C;
    border-radius: 16px;
    padding: 32px 28px;
}
.card-title {
    font-size: 20px;
    font-weight: 700;
    color: white;
    text-align: center;
    margin-bottom: 4px;
}
.card-subtitle {
    font-size: 11px;
    color: #85B7EB;
    text-align: center;
    margin-bottom: 24px;
}
.card-divider {
    height: 0.5px;
    background: #0C447C;
    margin-bottom: 24px;
}

/* Campos */
.field-label {
    font-size: 11px;
    color: #B5D4F4;
    margin-bottom: 6px;
    display: block;
}

/* 2FA info */
.twofa-info {
    background: #042C53;
    border: 0.5px solid #185FA5;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 10px;
    color: #85B7EB;
    margin-top: 8px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Botão */
.btn-entrar {
    width: 100%;
    background: #185FA5;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
    margin-bottom: 12px;
}
.btn-entrar:hover {
    background: #0C447C;
}

/* Links */
.link-esqueci {
    text-align: center;
    font-size: 10px;
    color: #378ADD;
    cursor: pointer;
    margin-bottom: 20px;
}

/* SSL rodapé */
.ssl-badge {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 8px;
}
.ssl-info {
    font-size: 9px;
    color: #85B7EB;
    background: #042C53;
    border: 0.5px solid #0C447C;
    border-radius: 5px;
    padding: 4px 10px;
}
.copyright {
    font-size: 8px;
    color: #185FA5;
}

/* Campo 2FA */
.twofa-input {
    letter-spacing: 8px;
    font-size: 20px;
    text-align: center;
}

/* Streamlit overrides */
div[data-testid="stTextInput"] input {
    background: #0C447C !important;
    border: 0.5px solid #185FA5 !important;
    border-radius: 8px !important;
    color: #E6F1FB !important;
    font-size: 13px !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #378ADD !important;
}
div[data-testid="stTextInput"] label {
    color: #B5D4F4 !important;
    font-size: 11px !important;
}

/* Erro */
.msg-erro {
    background: #3d0f0f;
    border: 0.5px solid #A32D2D;
    border-radius: 8px;
    color: #F09595;
    font-size: 11px;
    padding: 10px 14px;
    margin-bottom: 12px;
    text-align: center;
}
.msg-sucesso {
    background: #0a2b14;
    border: 0.5px solid #3B6D11;
    border-radius: 8px;
    color: #97C459;
    font-size: 11px;
    padding: 10px 14px;
    margin-bottom: 12px;
    text-align: center;
}

@media (max-width: 768px) {
    .login-wrapper { flex-direction: column; }
    .login-left { min-height: 300px; padding: 24px; }
    .login-right { width: 100%; min-width: unset; padding: 24px 16px; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SVG DO ÍCONE REDE DE ATIVOS (animado)
# ─────────────────────────────────────────
ICONE_REDE = """
<svg width="180" height="180" viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg">
  <style>
    .pulse1{animation:pulse 2s ease-in-out infinite}
    .pulse2{animation:pulse 2s ease-in-out infinite .4s}
    .pulse3{animation:pulse 2s ease-in-out infinite .8s}
    .pulse4{animation:pulse 2s ease-in-out infinite 1.2s}
    .pulse5{animation:pulse 2s ease-in-out infinite 1.6s}
    .la{animation:la 2s ease-in-out infinite}
    @keyframes pulse{0%,100%{opacity:.7}50%{opacity:1}}
    @keyframes la{0%,100%{opacity:.3}50%{opacity:.9}}
  </style>
  <!-- Nó central -->
  <circle cx="90" cy="90" r="28" fill="#185FA5" stroke="#378ADD" stroke-width="2" class="pulse1"/>
  <text x="90" y="86" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="700" fill="white">DT</text>
  <text x="90" y="100" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#B5D4F4">Facilities</text>
  <!-- Linhas -->
  <line x1="90" y1="90" x2="35" y2="38" stroke="#85B7EB" stroke-width="1.5" class="la"/>
  <line x1="90" y1="90" x2="145" y2="38" stroke="#85B7EB" stroke-width="1.5" class="la"/>
  <line x1="90" y1="90" x2="35" y2="142" stroke="#85B7EB" stroke-width="1.5" class="la"/>
  <line x1="90" y1="90" x2="145" y2="142" stroke="#85B7EB" stroke-width="1.5" class="la"/>
  <!-- Pontos animados nas linhas -->
  <circle cx="62" cy="64" r="3.5" fill="#378ADD" class="pulse2"/>
  <circle cx="117" cy="64" r="3.5" fill="#378ADD" class="pulse3"/>
  <circle cx="62" cy="116" r="3.5" fill="#378ADD" class="pulse4"/>
  <circle cx="117" cy="116" r="3.5" fill="#378ADD" class="pulse5"/>
  <!-- Nós satélite -->
  <circle cx="35" cy="38" r="20" fill="#0C447C" stroke="#378ADD" stroke-width="1.2" class="pulse2"/>
  <text x="35" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="white">BIM</text>
  <circle cx="145" cy="38" r="20" fill="#0C447C" stroke="#378ADD" stroke-width="1.2" class="pulse3"/>
  <text x="145" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="white">IA</text>
  <circle cx="35" cy="142" r="20" fill="#0C447C" stroke="#378ADD" stroke-width="1.2" class="pulse4"/>
  <text x="35" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="700" fill="white">IoT</text>
  <circle cx="145" cy="142" r="20" fill="#0C447C" stroke="#378ADD" stroke-width="1.2" class="pulse5"/>
  <text x="145" y="146" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="700" fill="white">O&amp;M</text>
</svg>
"""

# ─────────────────────────────────────────
# ESTADO DE SESSÃO
# ─────────────────────────────────────────
if "etapa" not in st.session_state:
    st.session_state.etapa = "login"       # login | verificar_2fa | logado
if "usuario_temp" not in st.session_state:
    st.session_state.usuario_temp = None
if "codigo_2fa" not in st.session_state:
    st.session_state.codigo_2fa = None
if "logado" not in st.session_state:
    st.session_state.logado = False


def gerar_codigo():
    return "".join(random.choices(string.digits, k=6))


def fazer_logout():
    st.session_state.etapa = "login"
    st.session_state.usuario_temp = None
    st.session_state.codigo_2fa = None
    st.session_state.logado = False


# ─────────────────────────────────────────
# SE JÁ LOGADO — redireciona para o app
# ─────────────────────────────────────────
if st.session_state.logado:
    usuario = USUARIOS[st.session_state.usuario_temp]
    st.markdown(f"""
    <div style="background:#021d38;min-height:100vh;display:flex;
        flex-direction:column;align-items:center;justify-content:center;padding:40px;">
        <div style="background:#031525;border:0.5px solid #0C447C;border-radius:16px;
            padding:40px;text-align:center;max-width:480px;width:100%;">
            <div style="font-size:48px;margin-bottom:16px;">✅</div>
            <h2 style="color:white;margin:0 0 8px;">Login realizado com sucesso!</h2>
            <p style="color:#85B7EB;font-size:13px;margin-bottom:24px;">
                Bem-vindo ao <strong style="color:white;">{usuario['empreendimento']}</strong>
            </p>
            <p style="color:#378ADD;font-size:11px;">
                Redirecionando para o Portal de Engenharia & Gestão de Ativos...
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Carregando o sistema..."):
        time.sleep(2)

    if st.button("🚪 Sair", on_click=fazer_logout):
        st.rerun()
    st.stop()


# ─────────────────────────────────────────
# LADO ESQUERDO — identidade visual
# ─────────────────────────────────────────
col_esq, col_dir = st.columns([1.1, 0.9])

with col_esq:
    st.markdown(f"""
    <div class="login-left" style="min-height:100vh;background:#021628;
        display:flex;flex-direction:column;align-items:center;
        justify-content:center;padding:48px;position:relative;overflow:hidden;">
        <div class="grid-bg"></div>
        <div class="overlay"></div>
        <div class="left-content">
            <div class="network-icon">{ICONE_REDE}</div>
            <p class="product-label">DT &nbsp; FACILITIES</p>
            <h1 class="product-name">O&M</h1>
            <div class="product-divider"></div>
            <p class="product-subtitle">GESTÃO INTELIGENTE DE ATIVOS</p>
            <p class="product-tagline">
                "Seu patrimônio sob controle,<br>onde você estiver."
            </p>
            <p class="segments">Hospital &nbsp;·&nbsp; Resort &nbsp;·&nbsp; Hipermercado &nbsp;·&nbsp; Facilities</p>
        </div>
        <div style="position:absolute;bottom:20px;left:0;right:0;text-align:center;">
            <span class="ssl-info">🔒 Conexão segura SSL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# LADO DIREITO — formulário de login
# ─────────────────────────────────────────
with col_dir:
    st.markdown("""
    <div style="background:#042C53;min-height:100vh;display:flex;
        flex-direction:column;align-items:center;justify-content:center;padding:32px;">
    """, unsafe_allow_html=True)

    # ── ETAPA 1: LOGIN ──
    if st.session_state.etapa == "login":

        st.markdown("""
        <div class="login-card">
            <p class="card-title">Acesse sua conta</p>
            <p class="card-subtitle">Entre com seu e-mail e senha</p>
            <div class="card-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            email = st.text_input("E-mail", placeholder="seu@email.com", key="email_input")
            senha = st.text_input("Senha", placeholder="••••••••", type="password", key="senha_input")

            st.markdown("""
            <div class="twofa-info">
                🔐 &nbsp; Verificação em 2 etapas ativa &nbsp;—&nbsp;
                um código será enviado ao seu e-mail após login
            </div>
            """, unsafe_allow_html=True)

            erro = st.empty()
            entrar = st.button("Entrar →", use_container_width=True, key="btn_entrar")

            st.markdown("""
            <p class="link-esqueci">Esqueci minha senha</p>
            """, unsafe_allow_html=True)

            if entrar:
                if not email or not senha:
                    erro.markdown('<div class="msg-erro">⚠️ Preencha e-mail e senha.</div>', unsafe_allow_html=True)
                elif email not in USUARIOS:
                    erro.markdown('<div class="msg-erro">❌ E-mail não cadastrado.</div>', unsafe_allow_html=True)
                elif USUARIOS[email]["senha"] != senha:
                    erro.markdown('<div class="msg-erro">❌ Senha incorreta. Tente novamente.</div>', unsafe_allow_html=True)
                else:
                    codigo = gerar_codigo()
                    st.session_state.codigo_2fa = codigo
                    st.session_state.usuario_temp = email
                    st.session_state.etapa = "verificar_2fa"
                    # Em produção: enviar código por e-mail real
                    st.info(f"🔐 Código 2FA (simulado): **{codigo}**")
                    time.sleep(1)
                    st.rerun()

    # ── ETAPA 2: VERIFICAÇÃO 2FA ──
    elif st.session_state.etapa == "verificar_2fa":
        usuario = USUARIOS[st.session_state.usuario_temp]

        st.markdown(f"""
        <div class="welcome-badge">
            <div class="welcome-avatar">{usuario['iniciais']}</div>
            <div class="welcome-text">
                <small>Verificando acesso para</small>
                <strong>{usuario['empreendimento']}</strong>
                <span>Último acesso: {usuario['ultimo_acesso']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="login-card">
            <p class="card-title">Verificação em 2 etapas</p>
            <p class="card-subtitle">Digite o código de 6 dígitos enviado ao seu e-mail</p>
            <div class="card-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        codigo_digitado = st.text_input(
            "Código de verificação",
            placeholder="_ _ _ _ _ _",
            max_chars=6,
            key="codigo_2fa_input"
        )

        erro2 = st.empty()

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("← Voltar", use_container_width=True):
                st.session_state.etapa = "login"
                st.rerun()
        with col_v2:
            if st.button("Verificar ✓", use_container_width=True, type="primary"):
                if codigo_digitado == st.session_state.codigo_2fa:
                    st.session_state.logado = True
                    st.rerun()
                else:
                    erro2.markdown('<div class="msg-erro">❌ Código incorreto. Tente novamente.</div>', unsafe_allow_html=True)

        st.markdown("""
        <p class="link-esqueci">Não recebi o código — reenviar</p>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ssl-badge" style="margin-top:24px;">
        <span class="ssl-info">🔒 Conexão segura SSL</span>
        <span class="copyright">© 2026 DT Facilities O&M</span>
    </div>
    </div>
    """, unsafe_allow_html=True)
