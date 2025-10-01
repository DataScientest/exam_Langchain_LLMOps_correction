import os
import json
import requests
import streamlit as st

# =========================
# CONFIG (Docker services)
# =========================
AUTH_URL = os.getenv("AUTH_URL", "http://auth:8001")
API_URL  = os.getenv("API_URL",  "http://main:8000")

st.set_page_config(page_title="Assistant Test Unitaire", page_icon="🧪", layout="wide")

# =========================
# SESSION STATE
# =========================
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "chat_draft" not in st.session_state:
    st.session_state.chat_draft = ""

# =========================
# HELPERS HTTP
# =========================
def auth_headers():
    if not st.session_state.token:
        return {}
    return {"Authorization": f"Bearer {st.session_state.token}"}

def post_json(url, payload, headers=None):
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        return r
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur réseau: {e}")
        return None

def get_json(url, headers=None):
    try:
        r = requests.get(url, headers=headers, timeout=60)
        return r
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur réseau: {e}")
        return None

def delete_json(url, headers=None):
    try:
        r = requests.delete(url, headers=headers, timeout=60)
        return r
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur réseau: {e}")
        return None

def show_response(res):
    if res is None:
        return
    try:
        data = res.json()
    except Exception:
        st.error(f"Réponse non JSON: {res.text}")
        return
    if 200 <= res.status_code < 300:
        st.success("OK")
        st.json(data)
    else:
        st.error(data)

# =========================
# SIDEBAR AUTH
# =========================
st.sidebar.title("🔑 Authentification")
mode = st.sidebar.radio("Action", ["Se connecter", "Créer un compte"])

username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

col_a1, col_a2 = st.sidebar.columns(2)
with col_a1:
    if mode == "Créer un compte":
        if st.button("Signup"):
            res = post_json(f"{AUTH_URL}/signup", {"username": username, "password": password})
            if res is not None and res.status_code == 200:
                st.sidebar.success("Compte créé ✅. Connectez-vous.")
            else:
                show_response(res)
    else:
        if st.button("Login"):
            res = post_json(f"{AUTH_URL}/login", {"username": username, "password": password})
            if res is not None and res.status_code == 200:
                data = res.json()
                st.session_state.token = data.get("access_token")
                st.session_state.username = username
                st.sidebar.success(f"Connecté en tant que {username}")
            else:
                show_response(res)

with col_a2:
    if st.session_state.token and st.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.success("Déconnecté.")

# =========================
# MAIN UI
# =========================
st.title("🧪 Assistant de Tests Unitaires")

if not st.session_state.token:
    st.info("Veuillez vous connecter pour utiliser l’assistant.")
    st.stop()

headers = auth_headers()

tabs = st.tabs([
    "🔍 Analyse",
    "📝 Générer Test",
    "📖 Expliquer Test",
    "⚡ Pipeline Complet",
    "💬 Chat libre",
    "🧠 Historique"
])

# --------- TAB 1: ANALYSE ----------
with tabs[0]:
    st.subheader("🔎 Analyse de code Python")

    code_input = st.text_area("Collez votre code ici :", height=220, key="analyze_code")

    if st.button("Analyser", key="btn_analyze"):
        res = post_json(f"{API_URL}/analyze", {"code": code_input}, headers=headers)

        if res and res.status_code == 200:
            data = res.json()

            st.markdown("### 📊 Résultat de l'analyse")

            # Résumé optimal / non optimal
            if data.get("is_optimal"):
                st.success("✅ Le code est considéré comme **optimal**")
            else:
                st.error("⚠️ Le code n'est **pas optimal**")

            # Problèmes détectés
            if data.get("issues"):
                with st.expander("🚨 Problèmes détectés"):
                    for issue in data["issues"]:
                        st.markdown(f"- {issue}")

            # Suggestions proposées
            if data.get("suggestions"):
                with st.expander("💡 Suggestions d'amélioration"):
                    for suggestion in data["suggestions"]:
                        st.markdown(f"- {suggestion}")

            # Affichage du code analysé
            st.markdown("### 💻 Code analysé")
            st.code(code_input, language="python")

        else:
            show_response(res)

# --------- TAB 2: GENERATE TEST ----------
with tabs[1]:
    st.subheader("🧪 Génération de test unitaire")

    code_input_2 = st.text_area("Code source :", height=220, key="gen_code")

    if st.button("Générer Test", key="btn_generate_test"):
        res = post_json(f"{API_URL}/generate_test", {"code": code_input_2}, headers=headers)

        if res and res.status_code == 200:
            data = res.json()

            st.markdown("### 📊 Résultat de la génération")

            unit_test = data.get("unit_test")
            if unit_test:
                st.success("✅ Test généré avec succès")
                st.markdown("### 📝 Code du test")
                st.code(unit_test, language="python")
            else:
                st.warning("⚠️ Aucun test généré")

            # Code source rappelé
            with st.expander("💻 Code source analysé"):
                st.code(code_input_2, language="python")

        else:
            show_response(res)


# --------- TAB 3: EXPLAIN TEST ----------
with tabs[2]:
    st.subheader("📖 Explication d’un test unitaire")

    test_code = st.text_area("Collez votre test unitaire :", height=220, key="explain_code")

    if st.button("Expliquer", key="btn_explain"):
        res = post_json(f"{API_URL}/explain_test", {"unit_test": test_code}, headers=headers)

        if res and res.status_code == 200:
            data = res.json()

            st.markdown("### 📊 Résultat de l'explication")

            explanation = data.get("explanation")
            if explanation:
                st.success("✅ Explication générée avec succès")
                st.markdown("### 📝 Explication")
                st.write(explanation)
            else:
                st.warning("⚠️ Aucune explication disponible")

            # Rappel du test unitaire fourni
            with st.expander("💻 Test unitaire analysé"):
                st.code(test_code, language="python")

        else:
            show_response(res)

# --------- TAB 4: FULL PIPELINE ----------
with tabs[3]:
    st.subheader("⚡ Pipeline complet : Analyse → Test → Explication")

    code_input_4 = st.text_area("Code source :", height=220, key="pipe_code")

    if st.button("Lancer Pipeline", key="btn_pipeline"):
        res = post_json(f"{API_URL}/full_pipeline", {"code": code_input_4}, headers=headers)

        if res and res.status_code == 200:
            data = res.json()

            # === Étape 1 : Analyse ===
            st.markdown("### 🔎 Analyse")
            analysis = data.get("analysis", {})
            if analysis:
                if analysis.get("is_optimal"):
                    st.success("✅ Le code est considéré comme **optimal**")
                else:
                    st.error("⚠️ Le code n'est **pas optimal**")
                    if analysis.get("issues"):
                        with st.expander("🚨 Problèmes détectés"):
                            for issue in analysis["issues"]:
                                st.markdown(f"- {issue}")
                    if analysis.get("suggestions"):
                        with st.expander("💡 Suggestions d'amélioration"):
                            for suggestion in analysis["suggestions"]:
                                st.markdown(f"- {suggestion}")

            # === Étape 2 : Test généré (si optimal) ===
            test = data.get("test", {})
            if test and test.get("unit_test"):
                st.markdown("### 🧪 Test généré")
                st.code(test["unit_test"], language="python")

            # === Étape 3 : Explication ===
            explanation = data.get("explanation", {})
            if explanation and explanation.get("explanation"):
                st.markdown("### 📖 Explication")
                st.write(explanation["explanation"])

            # === Code source fourni ===
            with st.expander("💻 Code source analysé"):
                st.code(code_input_4, language="python")

        else:
            show_response(res)

# --------- TAB 5: CHAT LIBRE ----------
with tabs[4]:
    st.subheader("Chat libre (mémoire automatique par utilisateur)")
    st.text_area("Message :", key="chat_input", height=120)

    if st.button("Envoyer", key="btn_chat_send"):
        content = st.session_state.get("chat_input", "").strip()
        if not content:
            st.warning("Message vide.")
        else:
            res = post_json(f"{API_URL}/chat", {"input": content}, headers=headers)
            if res and res.status_code == 200:
                data = res.json()
                st.success("Assistant :")
                st.write(data.get("response", ""))
            else:
                show_response(res)

# --------- TAB 6: HISTORY (global endpoints) ----------
with tabs[5]:
    st.subheader("🗂️ Historique complet de la session")

    if st.button("📜 Afficher l'historique", key="btn_history"):
        res = get_json(f"{API_URL}/history", headers=headers)

        if res and res.status_code == 200:
            data = res.json()
            history = data.get("history", [])

            if not history:
                st.info("ℹ️ Aucun historique trouvé pour cette session.")
            else:
                st.markdown("### 💬 Conversation enregistrée")
                for item in history:
                    role = item.get("role", "")
                    content = item.get("content", "")

                    if role == "human":
                        st.markdown(f"<div style='background-color:#e1f5fe; padding:8px; border-radius:8px; margin-bottom:5px;'>"
                                    f"**👤 Vous :** {content}</div>", unsafe_allow_html=True)
                    elif role == "ai":
                        st.markdown(f"<div style='background-color:#f1f8e9; padding:8px; border-radius:8px; margin-bottom:5px;'>"
                                    f"**🤖 Assistant :** {content}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {role}: {content}")

        else:
            show_response(res)

st.caption(f"Connecté en tant que **{st.session_state.username or 'inconnu'}** — APIs: AUTH_URL={AUTH_URL} | API_URL={API_URL}")
