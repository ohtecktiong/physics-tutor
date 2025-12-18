import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. PAGE CONFIGURATION
# This sets up the web browser tab title and icon.
# "initial_sidebar_state='expanded'" forces the side menu to stay open 
# so students don't miss the upload button.
# ==========================================
st.set_page_config(
    page_title="O-Level Physics Tutor", 
    page_icon="💻",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SECURITY & API SETUP
# This connects your code to the Google AI Brain.
# It checks if you are on the Cloud (st.secrets) or testing locally.
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # ⚠️ SAFETY WARNING: Only use this for testing on your laptop. 
    # Remove the key below before uploading to GitHub!
    api_key = "YOUR_API_KEY_FOR_LOCAL_TESTING" 

genai.configure(api_key=api_key)

# ==========================================
# 3. KNOWLEDGE BASE (CUSTOMISABLE)
# ✅ ACTION FOR MR TAN: Add new definitions to this list below.
# The AI will strictly use these words when asked "Define X".
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
# ✅ ACTION FOR MR TAN: This is where you set the rules of the classroom.
# You can edit the values for 'g', speed of light, or add new pedagogical rules here.
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
# We use "gemini-flash-latest" so it always points to the best fast model (currently 1.5).
# ==========================================
model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

# ==========================================
# 6. VISUAL LAYOUT (TITLE & SIDEBAR)
# This draws the text and buttons on the screen.
# ==========================================
st.title("🔭 O-Level Physics AI Tutor")
st.caption("Ask me about Kinematics, Forces, Lenses, or Electricity!")

# The Sidebar (The menu on the left)
with st.sidebar:
    st.header("📸 Upload Question")
    st.info("💡 **Tip:** Click the box below and press **Ctrl+V** to paste an image!")
    # The file uploader widget
    uploaded_file = st.file_uploader("Upload or Paste Screenshot", type=["png", "jpg", "jpeg"])

# ==========================================
# 7. CHAT HISTORY (MEMORY)
# This ensures the bot remembers the conversation as long as the browser is open.
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Loop through history and display previous messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Check if the message contains an image
        if isinstance(message["content"], list): 
             # Display Text + Image
             st.markdown(message["content"][0]) 
             st.image(message["content"][1], width=300)
        else:
            # Display Text only
            st.markdown(message["content"])

# ==========================================
# 8. MAIN LOGIC LOOP
# This waits for the student to type something in the chat box.
# ==========================================
if prompt := st.chat_input("Type your question here..."):
    
    # --- SCENARIO A: Student uploaded an image ---
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        # 1. Show student's message & image on screen
        st.chat_message("user").markdown(prompt)
        st.chat_message("user").image(image, width=300)
        
        # 2. Save to history
        st.session_state.messages.append({"role": "user", "content": [prompt, image]})
        
        # 3. Ask AI (Send both text + image)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing circuit/diagram..."):
                response = model.generate_content([prompt, image])
                st.markdown(response.text)
        
        # 4. Save AI response to history
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    # --- SCENARIO B: Text question only ---
    else:
        # 1. Show student's message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2. Create a chat session
        chat = model.start_chat(history=[])
        
        # 3. Ask AI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        # 4. Save AI response
        st.session_state.messages.append({"role": "assistant", "content": response.text})

