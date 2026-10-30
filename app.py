import os
import streamlit as st
import google.generativeai as genai

# 1. પેજ કન્ફિગરેશન
st.set_page_config(
    page_title="Kian AI - Secure & Smart Assistant",
    page_icon="🛡️",
    layout="centered"
)

# 2. સિક્યોરિટી check અને API Key ફેચ કરવી
API_KEY = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.warning(f"Secrets Read Warning: {e}")

if not API_KEY:
    API_KEY = os.getenv("GEMINI_API_KEY")

# 3. Kian AI હેડર
st.title("🛡️ Kian AI")
st.caption("High-Security, Encrypted & Ultra-Fast AI Assistant")

if not API_KEY:
    st.error("⚠️ સુરક્ષા ચેતવણી: API Key સેટ નથી. કૃપા કરીને Streamlit Cloud ના Settings -> Secrets માં 'GEMINI_API_KEY' ઉમેરો.")
    st.stop()

# 4. Gemini AI કન્ફિગરેશન
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Gemini Configuration Error: {e}")
    st.stop()

# 5. ઇનપુટ સેનિટાઇઝેશન
def sanitize_input(text: str) -> str:
    return text.replace("<script>", "").replace("</script>", "").strip()

# 6. ચેટ હિસ્ટ્રી મેનેજ કરવી
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "નમસ્તે! હું Kian AI છું. હું તમારી કેવી રીતે મદદ કરી શકું?"}
    ]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# 7. યુઝર ઇનપુટ અને રિસ્પોન્સ
if user_input := st.chat_input("તમારો પ્રશ્ન અહીં લખો..."):
    safe_input = sanitize_input(user_input)
    
    if safe_input:
        st.session_state["messages"].append({"role": "user", "content": safe_input})
        st.chat_message("user").write(safe_input)

        with st.chat_message("assistant"):
            with st.spinner("Kian AI વિચાર કરી રહ્યું છે..."):
                try:
                    response = model.generate_content(safe_input)
                    bot_reply = response.text
                    st.write(bot_reply)
                    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error(f"ટેકનિકલ એરર આવી છે: {e}")
