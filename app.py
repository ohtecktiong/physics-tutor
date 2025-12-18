import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="O-Physics Buddy", 
    page_icon="💻",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SECURITY & API SETUP
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "YOUR_API_KEY_FOR_LOCAL_TESTING" 

genai.configure(api_key=api_key)

# ==========================================
# 3. KNOWLEDGE BASE
# ==========================================
OFFICIAL_DEFINITIONS = """
1. Speed: Distance moved per unit time.
2. Velocity: Rate of change of displacement.
3. Acceleration: Rate of change of velocity.
4. Mass: A measure of the amount of substance in a body.
5. Weight: The force of gravity acting on a body.
6. Density: Mass per unit volume.
7. Moment: The product of force and the perpendicular distance from the pivot to the line of action of the force.
8. Principle of Moments: For an object in equilibrium, the sum of clockwise moments about a pivot is equal to the sum of anticlockwise moments about the same pivot.
9. Centre of Gravity: The point through which the whole weight of the object appears to act.
10. Pressure: Force acting per unit area.
"""

# ==========================================
# 4. THE "TEACHER BRAIN" (SYSTEM INSTRUCTIONS)
# ==========================================
system_instruction = f"""
You are a supportive O-Level Physics tutor (Singapore).

**SOURCE MATERIAL:**
You have access to the following OFFICIAL DEFINITIONS. If a student asks for a definition, you MUST use these exact words:
{OFFICIAL_DEFINITIONS}

**MANDATORY PHYSICS RULES:**
1. g = 10 N/kg.
2. Speed of light = 3.0 x 10^8 m/s.
3. Unit Formatting: Use m/s, m/s^2 (NO negative indices like ms^-1).
4. EMI Phrase: Must use "change in number of magnetic field lines going through a coil with time".
5. Field Lines: Remind student to draw sufficient lines to show symmetry.
6. Scaffolding: Never give the answer immediately. Use hints and Socratic questioning.
"""

# ==========================================
# 5. AI MODEL SELECTION
# ==========================================
model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

# ==========================================
# 6. VISUAL LAYOUT
# ==========================================
st.title("💻 O-Physics Buddy")
st.caption("I am here to partner you in your learning of Physics!")

with st.sidebar:
    st.header("⚙️ Settings")
    
    # 1. The Reset Button
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # 2. The Upload Box
    st.header("📸 Upload Question")
    st.info("💡 **Tip:** Click the box below and press **Ctrl+V** to paste an image!")
    uploaded_file = st.file_uploader("Upload or Paste Screenshot", type=["png", "jpg", "jpeg"])

# ==========================================
# 7. CHAT HISTORY (MEMORY)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], list): 
             st.markdown(message["content"][0]) 
             st.image(message["content"][1], width=300)
        else:
            st.markdown(message["content"])

# ==========================================
# 8. MAIN LOGIC LOOP
# ==========================================
if prompt := st.chat_input("Type your question here..."):
    
    # --- SCENARIO A: Student uploaded an image ---
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        st.chat_message("user").markdown(prompt)
        st.chat_message("user").image(image, width=300)
        
        st.session_state.messages.append({"role": "user", "content": [prompt, image]})
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing circuit/diagram..."):
                response = model.generate_content([prompt, image])
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    # --- SCENARIO B: Text question only (FIXED MEMORY) ---
    else:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- THE FIX: BUILD HISTORY FOR AI ---
        # We translate the Streamlit history into Gemini history so it "remembers"
        history_for_ai = []
        for msg in st.session_state.messages:
            # Map "assistant" (Streamlit) to "model" (Gemini)
            role = "user" if msg["role"] == "user" else "model"
            
            # If the previous message was an image, we just grab the text part 
            # so the AI remembers the CONTEXT, even if it can't "see" the image again.
            if isinstance(msg["content"], list):
                history_for_ai.append({"role": role, "parts": [msg["content"][0]]})
            else:
                history_for_ai.append({"role": role, "parts": [msg["content"]]})

        # Start the chat with the FULL history
        chat = model.start_chat(history=history_for_ai)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})



