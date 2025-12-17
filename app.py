import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="O-Level Physics Tutor", page_icon="🔭")

# --- SECRETS SETUP ---
# This grabs the key from the cloud secrets (or local secrets.toml if testing locally)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Fallback for local testing if you haven't set up secrets.toml
    # You can paste your key here temporarily for local testing, 
    # but remove it before uploading to GitHub!
    api_key = "YOUR_API_KEY_FOR_LOCAL_TESTING" 

genai.configure(api_key=api_key)

# --- DATABASE: OFFICIAL DEFINITIONS ---
# Add your exact definitions here. The AI will strictly refer to this.
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

# --- TEACHER BRAIN (System Instructions) ---
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
6. Scaffolding: Never give the answer immediately. Use hints.
"""

# Use the best available free model
# "gemini-flash-latest" points to the newest stable version (currently 1.5 Flash)
model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

# --- WEBSITE LAYOUT ---
st.title("🔭 O-Level Physics AI Tutor")
st.caption("Ask me about Kinematics, Forces, Lenses, or Electricity!")

# --- SIDEBAR (Image Handling) ---
with st.sidebar:
    st.header("📸 Upload Question")
    st.info("💡 **Tip:** Click the box below and press **Ctrl+V** to paste an image!")
    uploaded_file = st.file_uploader("Upload or Paste Screenshot", type=["png", "jpg", "jpeg"])

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Check if the content is a tuple (text, image) or just text
        if isinstance(message["content"], list): 
             # It's an image block [prompt, image_data]
             st.markdown(message["content"][0]) # Show the text prompt
             st.image(message["content"][1], width=300) # Show the image
        else:
            st.markdown(message["content"])

# --- CHAT INPUT & LOGIC ---
if prompt := st.chat_input("Type your question here..."):
    
    # CASE 1: Image + Text
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        # Display user message immediately
        st.chat_message("user").markdown(prompt)
        st.chat_message("user").image(image, width=300)
        
        # Save to history (We store text and image object)
        st.session_state.messages.append({"role": "user", "content": [prompt, image]})
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing circuit/diagram..."):
                response = model.generate_content([prompt, image])
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    # CASE 2: Text Only
    else:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Start a chat session (without history for now to keep it simple/fast)
        chat = model.start_chat(history=[])
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
