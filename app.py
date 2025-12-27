import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="O-Physics Buddy", 
    page_icon="💻📱🏋️",
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
ACCEPTABLE_DEFINITIONS = """
Scalar Quantity: Scalar quantities are physical quantities that have magnitude only.
Vector Quantity: Vector quantities are physical quantities that possess both magnitude and direction.
Speed: Speed is the rate of change of distance; or the change of distance with time taken for the change.
Velocity: Velocity is the rate of change of displacement; or the change of displacement with time taken for the chagne.
Acceleration: Acceleration is the rate of change of velocity; or, the change of velocity with time taken for the change.
Uniform Acceleration: Uniform acceleration is a constant rate of change of velocity. 
Mass: Mass is a measure of the amount of matter in a body and is the same for an object everywhere in the universe.
Weight: Weight is the amount of gravitational force acting on an object.
Inertia: The inertia of an object is the reluctance of the object to change its state of motion.
Gravitational Field: Gravitational field is a region which a mass experiences a force due to gravitational attraction.
Gravitational Field Strength: Gravitational field strength (at a point) is the gravitational force acting per unit mass on an object when it is placed at that point.
Moment: Moment is the turning effect of a force about a pivot, calculated using the product of the force and the perpendicular distance between the pivot and the line of action of the force.
Principle of Moments: Principle of moments states that when an object is in equilibrium there is no resultant turning moment about any pivot OR Principle of moments states that when an object is in equilibrium, the total clockwise moment about any pivot is equal to the total anti-clockwise moment about that pivot.
Centre of Gravity: The center of gravity is the point where the entire weight of an object appears to act.
Pressure: Pressure is force exerted per unit area.
Principle of Conservation of Energy: Principle of conservation of energy states that energy cannot be created or destroyed, it can only be transfer from one energy store to another. The total energy of an isolated system is a constant.
Work Done: Work done is the product of a force and the distance moved in the direction of the force; energy is transferred during the process.
Power: Power is the rate of work done.
Efficiency: Efficiency is the ratio of useful energy output of a system to the total energy input into it. OR The proportion of the energy supplied to a system that is transferred in a useful way.
Principle of Conservation of Energy: For an isolated system, energy cannot be destroyed or created; it can only be converted from one form to the other, or transfer from one object to the other.
Internal Energy: Internal energy is an energy store that make up of the total kinetic energy associated with the random motion of the particles and the total potential energy between the particles in the system.
Heat Capacity: Heat capacity is the change of an object’s internal energy per unit change in its temperature.
Specific Heat Capacity: Specific heat capacity is the change of an object’s internal energy per unit mass of every unit change in its temperature.
Latent Heat: Latent heat is energy absorbed or released by a substance to change its state without changing its temperature.
Specific Latent Heat: Specific latent heat is the energy absorbed or released per unit mass by a substance to change its state without changing its temperature.
Waves: Waves are disturbances or oscillations that travel through space and matter, transferring energy from one place to another without transferring matter.
Transverse Waves: Transverse waves are waves with the oscillations or vibrations occur perpendicular to the direction of wave travel.
Longitudinal Waves: Longitudinal waves are waves with the oscillations or vibrations occur parallel to the direction of wave travel.
Wave Speed: Wave speed is the distance a wave travels per unit time. It is a measure of how fast energy propagates through a medium.
Frequency: Frequency is the number of complete oscillations made in unit time.
Wavelength: Wavelength of a transverse wave is the distance between 2 successive crests, 2 successive troughs or 2 successive wavefronts on the wave.
Period: Period is the time taken to complete one oscillation.
Amplitude: Amplitude is the maximum displacement of a particle from its equilibrium position.
Wavefront: Wavefront is an imaginary line that joins all the points of a wave that are in phase or are vibrating in unison.
Ultrasound: Ultrasounds are sound waves with frequency higher than the upper limit of human hearing range.
Normal: Normal is an imaginary line perpendicular to the surface at the point where the light ray strikes. It serves as a reference line for measuring angles of incidence and reflection.
Angle Of Incidence: Angle of incidence is the angle between the incident light ray (the incoming ray) and the normal to the surface at the point of incidence.
Angle Of Reflection: Angle of reflection is the angle between the reflected light ray (the ray that bounces off the surface) and the normal to the surface at the point of reflection.
Angle Of Refraction: Angle of refraction is the angle between the refracted ray (the light ray that passes into and bends within a new medium) and the normal to the surface at the point of refraction.
Refractive Index: Refractive index of a medium is the ratio of speed of light in vacuum to the speed of light in that medium.
Critical Angle: Critical angle is the angle of incidence in an optically denser medium for which the angle of refraction in the optically less dense medium is 90°.
Total Internal Reflection: Total internal reflection is the complete reflection of a light ray in an optically denser medium at the boundary with an optically less dense medium.
Focal Point: Focal point is the point on the principal axis of a lens for which all the rays parallel to the principal axis meet after passing through the lens.
Focal Length: Focal length is the distance between the principal focal point and the optical centre of a lens.
Electric Field: Electric field is a region for which an object experiences a force because of the charge it carries.
Magnetic Field: Magnetic field is a region for which an object experiences a force because of its magnetic property.
Current: Current is the rate of flow of charges.
Electromotive Force: Electromotive force of a source is the work done per unit charge by the source in driving charges around a complete circuit and it is measured in volts.
Potential Difference: Potential difference across a component in a circuit is the work done per unit charge in driving charges through the component and it is measured in volts.
Resistance: Resistance of an electrical component is the ratio of the potential difference across it to the current flowing through it.
Ohm’s Law: Ohm’s Law states that the potential difference across a conductor at constant temperature is directly proportional to the current flowing through it.
Live: Live are connections that currents take to flow from the main to an electrical appliance, and it is usually maintains at high voltage.
Neutral: Neutral are connections allows the current to flow from the electrical appliance to the main, and it is usually maintains at zero potential.
Earth: Earth carries no current under normal working condition; current flows through it when there is a short-circuit.
Nuclear Decay
Radioactive Decay: Nuclear decay is a random process for which unstable nucleus loses its energy by emitting particles and electromagnetic radiations to process stable nucleus.
Half-life: Half-life of a radioactive nuclide is the time taken for half the nuclei of that nuclide in any sample to decay.
Nuclear Fission: Nuclear fission is a process in which the nucleus of an atom splits (usually into two parts) and releases a huge amount of energy.
Nuclear Fusion: Nuclear fusion is a process in which two light atomic nuclei combine to form one heavier atomic nucleus and releases a huge amount of energy.
Newton (N): 1 N is the amount of force required to cause an object of 1 kg mass to have an acceleration of 1 m/s2.
Joule (J): 1 J of work is done on an object when 1 N of force is applied on it for a distance of 1.
Pascal (Pa): 1 Pa is pressure acting on a 1 m2 area is 1 Pa when the force exerted on the area is 1 N.
Coulomb (c): 1 C is the amount of charges flow in a conductor when the current in 1 s is 1 A.
Volt (V): 1 V is the potential difference across a device when 1 C of charges move through it, 1 J of work is done.
"""

# ==========================================
# 4. THE "TEACHER BRAIN" (SYSTEM INSTRUCTIONS)
# ==========================================
system_instruction = f"""
You are a supportive, encouraging, and clear Secondary School Physics tutor for O-Level students in Singapore. Your goal is to help students learn through scaffolding, not just by giving answers.
Your tone should be semi-formal, nurturing, and patient, use emojis occasionally (e.g., 🧲, ⚡, 💡), keep sentences concise (max 15 words).

**SOURCE MATERIAL:**
You have access to the following ACCEPTABLE DEFINITIONS. If a student asks for a definition, you MUST use these exact words:
{ACCEPTABLE_DEFINITIONS}

**MANDATORY PHYSICS RULES:**
1. g = 10 N/kg.
2. Speed of light = 3.0 x 10^8 m/s.
3. Unit Formatting: Use m/s, m/s^2 (NO negative indices like ms^-1).
4. Addition of forces is by parallelogram only, no resolving of forces.
5. EMI Phrase: Must use "change in number of magnetic field lines going through a coil with time".
6. Field Lines (Electric and Magnetic): Remind student to draw sufficient lines to show symmetry.
7. Significant Figures: Strictly follow rules; Multiplication/Division: Least significant figures, Addition/Subtraction: Least decimal places.
8. Include one to two more significant figures in intermediate steps in calculation.
9. Scaffolding: Never give the answer immediately. Use hints and Socratic questioning.
"""

# ==========================================
# 5. AI MODEL SELECTION
# ==========================================
model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

# ==========================================
# 6. VISUAL LAYOUT
# ==========================================
st.title("💻 O-Physics Buddy")
st.caption("I am here to partner you in your learning of O-Level Pure Physics!")

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









