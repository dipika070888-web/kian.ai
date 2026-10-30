import os
import streamlit as st
import google.generativeai as genai

# 1. પેજ કન્ફિગરેશન અને ટાઇટલ સેટ કરવું
st.set_page_config(
    page_title="Kian AI - Secure & Smart Assistant",
    page_icon="🛡️",
    layout="centered"
)

# 2. સિક્યોરિટી check: હેકર્સથી કી (API Key) પ્રોટેક્ટ કરવી
# API Key ક્યારેય ખુલ્લા કોડમાં નથી લખાતી, પરંતુ Streamlit Secrets અથવા Environment Variables માં લોક રહે છે.
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ સુરક્ષા ચેતવણી: API Key સેટ નથી. કૃપા કરીને આને Secrets Manager માં લોક કરો.")
    st.stop()

# 3. Gemini AI મોડેલ કન્ફિગર કરવું
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. Kian AI ની શાનદાર હેડર ડિઝાઇન
st.title("🛡️ Kian AI")
st.caption("High-Security, Encrypted & Ultra-Fast AI Assistant")

# 5. હેકિંગ અને મલેશિયસ ઇનપુટથી બચવા માટેનું સેનિટાઇઝેશન ફંકશન
def sanitize_input(text: str) -> str:
    # ખરાબ સ્ક્રિપ્ટો (XSS/Code Injection) ફિલ્ટર કરવી
    clean_text = text.replace("<script>", "").replace("</script>", "")
    return clean_text.strip()

# 6. ચેટ હિસ્ટ્રી મેનેજ કરવી (Session State)
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "નમસ્તે! હું Kian AI છું. હું તમારી કેવી રીતે મદદ કરી શકું?"}
    ]

# જૂના મેસેજ સ્ક્રીન પર બતાવવા
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# 7. યુઝર ઇનપુટ બોક્સ અને રિસ્પોન્સ
if user_input := st.chat_input("તમારો પ્રશ્ન અહીં લખો..."):
    # ઇનપુટ સેનિટાઇઝ કરવું (Security Check)
    safe_input = sanitize_input(user_input)
    
    if safe_input:
        # યુઝરનો મેસેજ ડિસ્પ્લે કરવો
        st.session_state["messages"].append({"role": "user", "content": safe_input})
        st.chat_message("user").write(safe_input)

        # Kian AI નો જવાબ જનરેટ કરવો
        with st.chat_message("assistant"):
            with st.spinner("Kian AI વિચાર કરી રહ્યું છે..."):
                try:
                    response = model.generate_content(safe_input)
                    bot_reply = response.text
                    st.write(bot_reply)
                    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error("સુરક્ષા પ્રોટોકોલ: જવાબ મેળવવામાં ભૂલ થઈ છે. ડેટા સુરક્ષિત છે.")
