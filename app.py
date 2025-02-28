# app.py
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Configuration de base
#HOST = "http://127.0.0.1:8181"
HOST = "https://mjb-api-217448161611.europe-west1.run.app"

if "session_id" not in st.session_state:
    st.session_state.session_id = ""

# Fonction pour charger l'animation Lottie
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Configuration de la page
st.set_page_config(
    page_title="SorakaBot - Assistant Médical",
    page_icon="🏥",
    layout="wide"
)

# Styles CSS personnalisés avec des améliorations
st.markdown("""
    <style>
    .stSidebar {background-color: #F0F8FF;}
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .chat-message {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0px;
    }
    .chat-message.user {
        background-color: #E3F2FD;
    }
    .chat-message.bot {
        background-color: #F3E5F5;
    }
    .big-font {
        font-size: 3rem !important;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 1rem;
    }
    .medium-font {
        font-size: 1.5rem !important;
        color: #34495E;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px;
    }
    .centered-text {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Gestion de la navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Page d'accueil
if st.session_state.page == 'home':
    # Animation Lottie pour illustration médicale
    lottie_medical = load_lottie_url('https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json')
    
    # En-tête
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<p class="big-font centered-text">Bienvenue sur SorakaBot</p>', unsafe_allow_html=True)
        st.markdown('<p class="medium-font centered-text">Votre assistant médical intelligent disponible 24/7</p>', unsafe_allow_html=True)
    
    # Animation et description
    col1, col2 = st.columns([1, 1])
    with col1:
        if lottie_medical:
            st_lottie(lottie_medical, height=400)
    with col2:
        st.markdown("""
        ### 🌟 Pourquoi choisir SorakaBot ?
        
        - 📚 **Base de connaissances étendue** : Accédez à des informations médicales fiables
        - 🕒 **Disponible 24/7** : Obtenez des réponses à tout moment
        - 🔒 **Confidentialité** : Vos conversations restent privées
        - 💡 **Réponses précises** : Information claire et pertinente
        - ⚕️ **Support médical** : Guidage vers les ressources appropriées
        """)
    
    # Fonctionnalités
    st.markdown("### 🎯 Nos Services")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🩺 Consultation Préliminaire</h3>
        <p>Obtenez une première évaluation de vos symptômes et des conseils sur les prochaines étapes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>💊 Information Médicale</h3>
        <p>Accédez à des informations fiables sur les médicaments, les conditions médicales et les traitements.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>🚑 Orientation Médicale</h3>
        <p>Recevez des conseils sur quand et où consulter un professionnel de santé.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Bouton pour accéder au chat
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🩺 Commencer la consultation"):
            st.session_state.page = 'chat'
            st.rerun()
    
    # Avertissement
    st.markdown("---")
    st.markdown("""
    <div style='background-color: #FFF3E0; padding: 20px; border-radius: 10px; margin-top: 20px;'>
    <h3>⚠️ Avertissement Important</h3>
    <p>SorakaBot est un outil d'information et ne remplace en aucun cas une consultation médicale professionnelle. 
    Pour tout problème de santé, consultez toujours un professionnel de santé qualifié.</p>
    </div>
    """, unsafe_allow_html=True)

# Page du chat
elif st.session_state.page == 'chat':
    # Button to return to home
    if st.button("🏠 Retour à l'accueil"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.title("🏥 SorakaBot - Assistant Médical")
    st.markdown("Posez vos questions médicales en toute confiance")
    
    # Le reste de votre code de chat existant ici
    with st.sidebar:
        st.markdown("### ⚙️ Paramètres")
        temperature = st.slider("Créativité des réponses", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
        language = st.selectbox("Langue", ["Francais", "English", "Arabic"])
    
    # Initialisation des messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Bonjour! Je suis SorakaBot, votre assistant médical. Comment puis-je vous aider aujourd'hui?"}]
    
    # Affichage des messages
    for message in st.session_state.messages:
        avatar = "🏥" if message["role"] == "assistant" else "👤"
        st.chat_message(message["role"], avatar=avatar).write(message["content"])
    
    # Gestion de l'entrée utilisateur
    if question := st.chat_input("Posez votre question ici..."):
        st.session_state["messages"].append({"role": "user", "content": question})
        st.chat_message("user", avatar="👤").write(question)
        
        try:
            with st.spinner("🏥 Analyse de votre question..."):
                response = requests.post(
                    f"{HOST}/answer",
                    json={
                        "question": question,
                        "temperature": temperature,
                        "language": language,
                        "session_id": st.session_state.session_id,
                        "previous_context": st.session_state["messages"]
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    answer = response.json().get("message", "Désolé, je n'ai pas pu traiter votre demande.")
                    if "session_id" in response_data:
                        st.session_state.session_id = response_data["session_id"]
                    st.session_state["messages"].append({"role": "assistant", "content": answer})
                    st.chat_message("assistant", avatar="🏥").write(answer)
                else:
                    st.error(f"Erreur: {response.status_code} - {response.text}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de communication avec le serveur: {str(e)}")