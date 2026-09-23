# pages/1_AI_Assistant.py
import streamlit as st
from openai import OpenAI
from datetime import datetime

# System prompt with strict farming focus
SYSTEM_PROMPT = """You are FarmSathi (Farm Friend), an expert agricultural assistant designed to help farmers with their farming-related queries. You provide practical, actionable advice based on scientific agricultural knowledge.

STRICT GUIDELINES:
1. ONLY answer questions related to:
   - Crop cultivation (planting, growing, harvesting)
   - Soil health and fertilizers
   - Pest and disease management
   - Irrigation and water management
   - Weather and seasonal planning
   - Organic farming practices
   - Crop rotation and intercropping
   - Seeds and varieties
   - Farm equipment and tools
   - Post-harvest management and storage
   - Market prices and selling strategies
   - Government schemes for farmers
   - Animal husbandry (if related to farming)
   - Sustainable farming practices

2. If asked ANYTHING outside farming (politics, entertainment, general knowledge, coding, etc.):
   - Politely decline and redirect to farming topics
   - Say: "I'm specifically designed to help with farming and agriculture. Please ask me questions about crops, soil, pests, irrigation, or any other farming-related topics. How can I help you with your farming needs?"

3. Language Support:
   - Respond in the same language the user asks in
   - Support English, Hindi, and Hinglish (mixed)
   - Use simple, farmer-friendly language
   - Avoid overly technical jargon unless necessary

4. Response Style:
   - Be friendly, respectful, and encouraging
   - Give practical, actionable advice
   - Include specific steps when possible
   - Mention regional considerations when relevant (North India focus)
   - If you need more details (like location, crop type, season), ask clarifying questions

5. Safety First:
   - Always recommend consulting local agricultural experts for serious issues
   - Suggest soil testing before major fertilizer decisions
   - Warn about proper pesticide handling and safety equipment

Remember: You are a helpful farming companion, not a general-purpose AI. Stay focused on agriculture!"""

def get_client():
    """Initialize Z.ai client from secrets"""
    try:
        api_key = st.secrets.get("ZAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return None
        # Z.ai uses OpenAI-compatible API
        return OpenAI(
            api_key=api_key,
            base_url="https://api.z.ai/v1"  # Z.ai endpoint
        )
    except Exception:
        return None

def get_ai_response(client, user_message, conversation_history):
    """Get response from Z.ai with conversation context"""
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model="glm-4.5",
            messages=messages,
            max_tokens=800,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error connecting to AI service: {str(e)}\nPlease check your API key configuration."

def main():
    st.set_page_config(
        page_title="FarmSathi - AI Farming Assistant",
        page_icon="🌾",
        layout="centered"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main { background-color: #f5f7f5; }
        .stButton>button {
            background-color: #4CAF50; color: white; border-radius: 8px;
            border: none; padding: 8px 16px; font-weight: 500;
        }
        .stButton>button:hover { background-color: #45a049; }
        .chat-message {
            padding: 12px; border-radius: 8px; margin-bottom: 10px; color: #1e1e1e;
        }
        .user-message { background-color: #e8f5e9; border-left: 4px solid #4CAF50; }
        .assistant-message { background-color: #ffffff; border-left: 4px solid #FF9800; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    
    client = get_client()
    
    # Header
    st.title("🌾 FarmSathi - Your AI Farming Assistant")
    st.markdown("*Ask me anything about farming, crops, soil, pests, irrigation, and more!*")
    st.markdown("*मुझसे खेती, फसलों, मिट्टी, कीटों, सिंचाई और अन्य कृषि विषयों के बारे में पूछें!*")
    
    # Check API key
    if not client:
        st.error("⚠️ **API Key Not Configured**")
        st.info("Add `ZAI_API_KEY` or `OPENAI_API_KEY` in Streamlit Secrets to use this assistant.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Quick Guide")
        st.markdown("""
        **Ask me about:**
        - 🌱 Crop cultivation
        - 🪴 Soil & fertilizers
        - 🐛 Pest control
        - 💧 Irrigation tips
        - 🌦️ Seasonal planning
        - 📦 Storage & selling
        - 🏛️ Govt. schemes
        
        **Language:**
        - English ✅
        - हिंदी ✅
        - Hinglish ✅
        """)
        st.divider()
        if st.button("🔄 Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_started = False
            st.rerun()
        st.divider()
        st.caption(f"💬 Messages: {len(st.session_state.messages)}")
    
    # Welcome message for new users
    if not st.session_state.chat_started:
        st.info("👋 **Welcome!** I'm FarmSathi, your farming assistant. Ask me any agriculture-related question!")
        st.markdown("**Try asking:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌾 Best crops for winter?", use_container_width=True):
                st.session_state.chat_started = True
                user_msg = "What are the best crops to grow in winter in North India?"
                st.session_state.messages.append({"role": "user", "content": user_msg, "timestamp": datetime.now()})
                with st.spinner("🤔 Thinking..."):
                    ai_response = get_ai_response(client, user_msg, st.session_state.messages[:-1])
                st.session_state.messages.append({"role": "assistant", "content": ai_response, "timestamp": datetime.now()})
                st.rerun()
        
        with col2:
            if st.button("🐛 Organic pest control?", use_container_width=True):
                st.session_state.chat_started = True
                user_msg = "How can I control pests organically without chemicals?"
                st.session_state.messages.append({"role": "user", "content": user_msg, "timestamp": datetime.now()})
                with st.spinner("🤔 Thinking..."):
                    ai_response = get_ai_response(client, user_msg, st.session_state.messages[:-1])
                st.session_state.messages.append({"role": "assistant", "content": ai_response, "timestamp": datetime.now()})
                st.rerun()
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.container():
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🧑‍🌾 You:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🌾 FarmSathi:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.divider()
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Ask your farming question:",
            placeholder="e.g., How to improve soil fertility? / मिट्टी की उर्वरता कैसे बढ़ाएं?",
            key="user_input", label_visibility="collapsed"
        )
    with col2:
        send_button = st.button("Send 📤", use_container_width=True)
    
    if send_button and user_input.strip():
        st.session_state.chat_started = True
        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
        with st.spinner("🤔 Thinking..."):
            ai_response = get_ai_response(client, user_input, st.session_state.messages[:-1])
        st.session_state.messages.append({"role": "assistant", "content": ai_response, "timestamp": datetime.now()})
        st.rerun()
    
    st.divider()
    st.caption("💡 Tip: Always consult local agricultural experts for region-specific advice and serious crop issues.")

if __name__ == "__main__":
    main()