import streamlit as st
import requests

st.set_page_config(page_title="Auth + LLM", layout="centered")

# États
if "token" not in st.session_state:
    st.session_state.token = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "memory_payload" not in st.session_state:
    st.session_state.memory_payload = None

API_AUTH = "http://api_auth:8000"
API_LLM = "http://api_llm:8001"


def refresh_memory():
    try:
        r = requests.get(f"{API_LLM}/memory", params={"token": st.session_state.token})
        if r.status_code == 200:
            st.session_state.memory_payload = r.json()
        else:
            st.error("Erreur mémoire : " + r.text)
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur mémoire: {e}")


def clear_memory():
    try:
        r = requests.delete(f"{API_LLM}/memory", params={"token": st.session_state.token})
        if r.status_code == 200:
            st.success("Mémoire vidée")
            st.session_state.memory_payload = None
        else:
            st.error("Erreur (clear): " + r.text)
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur (clear): {e}")


# --- Login ---
if st.session_state.page == "login":
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        try:
            res = requests.post(f"{API_AUTH}/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.session_state.page = "llm"
                st.rerun()
            else:
                st.error("Échec de connexion")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion: {e}")

# --- LLM ---
elif st.session_state.page == "llm":
    st.title("Analyse de code avec LLM")

    code = st.text_area("Fonction Python", height=200, placeholder="def add(a, b):\n    return a + b")

    explain_tests = st.checkbox("Expliquer les tests", value=True)

    if st.button("Analyser"):
        try:
            res = requests.post(f"{API_LLM}/analyze_code", json={
                "token": st.session_state.token,
                "code": code,
                "explain_tests": explain_tests
            })
            if res.status_code == 200:
                data = res.json()
                if data.get("status") == "ok":
                    st.success("✅ Analyse réussie")

                    st.subheader("Code des tests")
                    st.code(data.get("tests_code", ""), language="python")

                    if "tests_explanation" in data:
                        st.subheader("Explication")
                        st.write(data["tests_explanation"])

                    if "token_stats" in data and data["token_stats"]:
                        st.info(data["token_stats"])

                elif data.get("status") == "error":
                    st.error("❌ Impossible de générer les tests")
                    st.subheader("Explication")
                    st.write(data.get("explanation", "Pas d'explication fournie."))

                    if "token_stats" in data and data["token_stats"]:
                        st.info(data["token_stats"])
                else:
                    st.warning("Réponse inattendue :")
                    st.json(data)

                refresh_memory()

            else:
                st.error("Erreur : " + res.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de requête: {e}")

    # --- Mémoire LLM ---
    with st.expander("🧠 Mémoire LLM", expanded=False):
        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("Rafraîchir la mémoire", use_container_width=True):
                refresh_memory()
        with btn_cols[1]:
            if st.button("Vider la mémoire", type="secondary", use_container_width=True):
                clear_memory()

        st.markdown("---")
        payload = st.session_state.memory_payload
        if payload:
            st.subheader("Dernier verdict")
            st.json(payload.get("verdict", None))
            st.subheader(f"Messages (n={payload.get('size', 0)})")
            st.json(payload.get("messages", []))
        else:
            st.info("Aucune donnée mémoire chargée. Lance une analyse puis rafraîchis la mémoire.")

    if st.button("Déconnexion"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.success("Déconnecté")
        st.rerun()