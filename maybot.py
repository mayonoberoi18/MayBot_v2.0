import streamlit as st
from PIL import Image
import os
import json
from datetime import datetime
import wikipedia
from duckduckgo_search import DDGS
import sympy as sp

# ====================== PAGE CONFIG + FAVICON ======================
logo_path = "illuminati.jpg"

try:
    favicon = Image.open(logo_path)
except:
    favicon = "🤖"

st.set_page_config(
    page_title="MayBot",
    page_icon=favicon,          # This sets the browser tab icon
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #020617;
        background-image:
            radial-gradient(circle at 20% 30%, rgba(16, 185, 129, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.15) 0%, transparent 50%);
    }
    .stChatMessage {
        border-radius: 18px !important;
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ====================== LOAD LOGO ======================
def load_logo():
    if os.path.exists(logo_path):
        try:
            return Image.open(logo_path)
        except:
            return None
    return None

logo_img = load_logo()

# ====================== SIDEBAR LOGO (Modern) ======================
if logo_img:
    st.logo(logo_img, icon_image=logo_img, size="large")   # Shows in sidebar and collapsed header

# ====================== SESSION STATE INIT ======================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # List of past conversations
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "default"

# ====================== SMART ANSWER FUNCTION (Improved) ======================
def get_vast_answer(user_query):
    q = user_query.lower().strip()
    
    if any(x in q for x in ["who made you", "creator", "founder", "mayon"]):
        return "I am **MayBot**, proudly created by **Mayon Oberoi** from Nagpur, India. 🇮🇳"

    # Math Solver
    if any(c.isdigit() for c in q) and any(op in q for op in '+-*/^()=x'):
        try:
            expr = q.replace('^', '**').replace('x', '*')
            if '=' in expr:
                left, right = expr.split('=', 1)
                result = sp.sympify(f"{left} - ({right})").evalf()
            else:
                result = sp.sympify(expr).evalf()
            return f"🔢 **Math Result:** `{result}`"
        except:
            pass

    # Wikipedia
    try:
        titles = wikipedia.search(user_query, results=3)
        if titles:
            summary = wikipedia.summary(titles[0], sentences=5, auto_suggest=False)
            return f"📖 **Wikipedia Summary:**\n\n{summary}"
    except:
        pass

    # DuckDuckGo Search
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(user_query, max_results=5))
            if results:
                text = "\n\n".join([f"**{r.get('title','')}**\n{r.get('body','')}" for r in results])
                return f"🌐 **Web Search Results:**\n\n{text[:1800]}..."
    except:
        pass

    return "I couldn't find a clear answer after searching my knowledge and the web. Could you rephrase your question?"

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("🛠️ MayBot Controls")
    
    if st.button("🆕 New Chat", use_container_width=True):
        if st.session_state.messages:
            # Save current chat
            chat_title = st.session_state.messages[0]["content"][:40] if st.session_state.messages else "New Chat"
            st.session_state.chat_history.append({
                "id": st.session_state.current_chat_id,
                "title": chat_title,
                "messages": st.session_state.messages.copy(),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        st.session_state.messages = []
        st.session_state.current_chat_id = str(datetime.now().timestamp())
        st.rerun()

    st.divider()
    st.subheader("📜 Chat History")
    for chat in reversed(st.session_state.chat_history[-8:]):   # Show last 8
        if st.button(f"📌 {chat['title']}", key=chat['id'], use_container_width=True):
            st.session_state.messages = chat['messages'].copy()
            st.rerun()

    st.divider()
    
    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("📥 Export Current Chat", use_container_width=True):
        if st.session_state.messages:
            chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
            st.download_button(
                label="⬇️ Download as TXT",
                data=chat_text,
                file_name=f"MayBot_Chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

    st.divider()
    st.caption("Made with ❤️ by Mayon Oberoi • Nagpur")

# ====================== MAIN INTERFACE ======================
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    if logo_img:
        st.image(logo_img, width=110)
    st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
    st.caption("Your Intelligent Assistant • Powered by Mayon Oberoi")

# Example Prompts
st.markdown("**Try asking:**")
cols = st.columns(4)
with cols[0]:
    if st.button("Solve 2x² + 5x - 3 = 0"):
        prompt = "Solve 2x² + 5x - 3 = 0"
        st.session_state.messages.append({"role": "user", "content": prompt})
with cols[1]:
    if st.button("What is Illuminati?"):
        prompt = "What is Illuminati?"
        st.session_state.messages.append({"role": "user", "content": prompt})
with cols[2]:
    if st.button("Latest news on AI"):
        prompt = "Latest news on AI 2026"
        st.session_state.messages.append({"role": "user", "content": prompt})
with cols[3]:
    if st.button("Tell me about Nagpur"):
        prompt = "Tell me about Nagpur India"
        st.session_state.messages.append({"role": "user", "content": prompt})

# Display Chat Messages
for msg in st.session_state.messages:
    avatar = logo_img if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=logo_img):
        with st.spinner("Thinking... Scanning knowledge & web..."):
            response = get_vast_answer(prompt)
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Auto-save current chat when new messages arrive (optional improvement)
