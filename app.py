import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(
    page_title="O-Level Physics Tutor", 
    page_icon="🔭",
    initial_sidebar_state="expanded"
)

# --- API KEY SETUP ---
# Securely retrieve key from Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# --- TEACHER BRAIN (System Instructions) ---
system_instruction = """
You are a supportive O-Level Physics tutor (Singapore).
RULES:
1. g = 10 N/kg.
2. Speed of light = 3.0 x 10^8 m/s.
3. Unit Formatting: Use m/s, m/s^2 (NO negative indices like ms^-1).
4. EMI Phrase: Must use "change in number of magnetic field lines going through a coil with time".
5. Field Lines: Remind student to draw sufficient lines to show symmetry.
6. Scaffolding: Never give the answer immediately. Use hints.
"""

model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

# --- WEBSITE LAYOUT ---
st.title("🔭 O-Level Physics AI Tutor")
st.markdown("Ask me about **Kinematics, Forces, Lenses, or Electricity**!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)

    # Show AI response
    with st.chat_message("assistant"):
        st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
