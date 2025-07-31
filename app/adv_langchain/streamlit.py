import streamlit as st
import requests

st.set_page_config(page_title="🔐 Auth + LLM", layout="centered")

# Initialisation des états
if "token" not in st.session_state:
    st.session_state.token = None
if "page" not in st.session_state:
    st.session_state.page = "login"  # ou "llm"

# 🔐 Page de connexion
if st.session_state.page == "login":
    st.title("🔐 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        try:
            res = requests.post("http://localhost:8000/login", json={
                "username": username,
                "password": password
            })
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.session_state.page = "llm"
                st.rerun()  # Utilisez st.rerun() au lieu de st._rerun()
            else:
                st.error("❌ Échec de connexion")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erreur de connexion: {e}")

# 🤖 Page d'analyse LLM
elif st.session_state.page == "llm":
    st.title("🤖 Analyse de code avec LLM")

    if st.button("🔒 Déconnexion"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.success("✅ Déconnecté")
        st.rerun()  # Utilisez st.rerun() au lieu de st._rerun()

    code = st.text_area("Fonction Python", height=200)

    if st.button("Analyser"):
        try:
            res = requests.post("http://localhost:8001/analyze_code", json={
                "token": st.session_state.token,
                "code": code
            })

            if res.status_code == 200:
                st.success("✅ Résultat reçu")
                st.json(res.json())
            else:
                st.error("❌ Erreur : " + res.text)
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erreur de requête: {e}")