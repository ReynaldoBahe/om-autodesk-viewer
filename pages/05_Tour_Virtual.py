import streamlit as st
import streamlit.components.v1 as components

# Configuração da página (agora usando 'st' corretamente)
st.set_page_config(page_title="Tour Virtual 3D", page_icon="📸", layout="wide")

st.title("📸 Tour Virtual e Inspeção Visual 360°")
st.markdown("### Navegue pelas instalações da infraestrutura em tempo real")

# 1. Menu de seleção para o usuário mudar de ambiente
ambiente = st.selectbox(
    "Selecione o local para inspeção visual:",
    ["Subestação Principal", "Sala de Máquinas (Exemplo)"]
)

# 2. Definição dos links das imagens equirretangulares (360 graus)
if ambiente == "Subestação Principal":
    # Imagem de demonstração oficial do Pannellum para o teste funcionar
    url_foto_360 = "https://pannellum.org"
else:
    url_foto_360 = "https://pannellum.org"

# 3. Código HTML estruturado com os links de CDN totalmente corrigidos
pannellum_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizador 360</title>
    <!-- Links corrigidos apontando para o servidor do Pannellum -->
    <link rel="stylesheet" href="https://jsdelivr.net"/>
    <script type="text/javascript" src="https://jsdelivr.net"></script>
    <style>
        #panorama {{
            width: 100%;
            height: 550px;
        }}
    </style>
</head>
<body>

<div id="panorama"></div>

<script>
pannellum.viewer('panorama', {{
    "type": "equirectangular",
    "panorama": "{url_foto_360}",
    "autoLoad": true,
    "compass": true
}});
</script>

</body>
</html>
"""

# 4. Injeção do componente gráfico na tela do seu aplicativo Streamlit
components.html(pannellum_html, height=560, scrolling=False)
