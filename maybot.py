import streamlit as st
import wikipedia
from duckduckgo_search import DDGS
import sympy as sp
import re

# 1. Ultra-Premium "Obsidian Glow" UI
st.set_page_config(page_title="MayBot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #020617;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(16, 185, 129, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 1) 0%, transparent 100%);
        background-attachment: fixed;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .stMarkdown p { color: #f1f5f9 !important; font-size: 1.05rem; }
    [data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

# 2. Smart Search Functions
def get_vast_answer(user_query):
    q = user_query.lower().strip()
    
    # --- A. Identity & Creator ---
    if any(x in q for x in ["founder", "creator", "who made you", "mayon"]):
        return "I am MayBot, an intelligent assistant created by **Mayon Oberoi** from Nagpur, India."

    # --- B. Complex Math (Sympy) ---
    if any(c.isdigit() for c in q) and any(op in q for op in '+-*/^()x'):
        try:
            # Clean for math: 2x becomes 2*x, ^ becomes **
            math_q = q.replace('^', '**').replace('x', '*x').replace('=', '-(') + ')' if '=' in q else q
            return f"🔢 **Math Result:** {sp.sympify(q.replace('^', '**')).evalf()}"
        except: pass

    # --- C. Wikipedia "Deep Dive" ---
    try:
        # Step 1: Find the most relevant topic title
        search_titles = wikipedia.search(q)
        if search_titles:
            # Step 2: Get summary of the #1 result
            # We turn off auto_suggest to prevent "No page found" errors
            return wikipedia.summary(search_titles[0], sentences=4, auto_suggest=False)
    except: pass

    # --- D. Aggressive Web Scraping (DuckDuckGo) ---
    try:
        with DDGS() as ddgs:
            # We take the top 5 results and stitch them together for a "Vast" answer
            results = list(ddgs.text(q, max_results=5))
            if results:
                full_text = ""
                for r in results:
                    if len(r['body']) > 50:
                        full_text += f"{r['body']} "
                
                if full_text:
                    # Clean up the text to make it look like a real answer
                    return full_text[:1000] + "..." # Limit length for readability
    except: pass

    return "I've searched my internal database and the live web, but I couldn't find a clear answer. Could you try rephrasing your question?"

# 3. Main Interface
st.title("MayBot")
st.caption("Your Intelligent Assistance ; Powered By Mayon Oberoi")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Scanning global databases..."):
            response = get_vast_answer(prompt)
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
