# pages/2_Detector.py
import streamlit as st
from utils.model_inference import load_model, predict_image
from PIL import Image
from openai import OpenAI
from datetime import datetime

def get_client():
    """Initialize Z.ai client from secrets"""
    try:
        api_key = st.secrets.get("ZAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(
            api_key=api_key,
            base_url="https://api.z.ai/v1"
        )
    except Exception:
        return None

def generate_disease_report(client, disease_name, crop_name, confidence):
    """Generate comprehensive disease report using AI"""
    prompt = f"""You are an expert agricultural pathologist. A farmer has detected the following disease on their crop:

**Crop**: {crop_name}
**Disease**: {disease_name}
**Detection Confidence**: {confidence:.1%}

Generate a comprehensive, farmer-friendly report in the following structure. Use simple language that farmers can understand. Include both English and Hindi (हिंदी) key terms where helpful.

**IMPORTANT**: Keep the response well-structured, practical, and actionable. Focus on solutions the farmer can implement.

Please provide:

1. **Disease Overview** (2-3 sentences)
   - What is this disease and what causes it?
   - How serious is it?

2. **Symptoms to Look For** (bullet points)
   - Visual signs on leaves, stems, or crops
   - How it spreads

3. **Immediate Action Required** (step-by-step)
   - What the farmer should do RIGHT NOW
   - Urgent steps to prevent spread

4. **Treatment Options**
   A. **Organic/Natural Methods** (for farmers preferring chemical-free solutions)
   B. **Chemical Control** (fungicides/pesticides with common names available in India)
   C. **Cultural Practices** (farming techniques to control disease)

5. **Prevention for Future**
   - How to avoid this disease in next season
   - Best practices for crop health

6. **Important Notes**
   - Weather conditions that worsen this disease
   - When to consult an expert
   - Estimated recovery time if treated properly

Make it practical, actionable, and encouraging. The farmer should feel empowered to handle this."""

    try:
        response = client.chat.completions.create(
            model="glm-4.5",
            messages=[
                {"role": "system", "content": "You are an expert agricultural pathologist helping farmers with crop disease management. Provide practical, actionable advice in simple language. Support both English and Hindi terms."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Unable to generate AI report: {str(e)}\n\nPlease check your API key configuration."

def get_disease_context_response(client, user_question, disease_name, crop_name, conversation_history):
    """Get AI response for follow-up questions about the detected disease"""
    system_prompt = f"""You are an agricultural expert helping a farmer who has just detected **{disease_name}** on their **{crop_name}** crop.

The farmer is asking follow-up questions about this specific disease. Your role:

1. **Stay focused on {disease_name}** - all answers should relate to this detected disease
2. **Be practical and actionable** - farmers need solutions they can implement
3. **Use simple language** - avoid overly technical jargon
4. **Support bilingual queries** - respond in the same language the farmer asks (English/Hindi/Hinglish)
5. **Provide specific recommendations** - mention actual products, techniques, and practices available in India
6. **Be encouraging** - give hope while being realistic

If the farmer asks about something completely unrelated to farming or this disease, politely redirect them back to the disease management topic.

Answer their questions as a knowledgeable, friendly agricultural advisor would."""

    try:
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_question})
        
        response = client.chat.completions.create(
            model="glm-4.5",
            messages=messages,
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def parse_disease_label(label):
    """Parse the disease label to extract crop and disease name"""
    parts = label.split('___')
    if len(parts) == 2:
        crop = parts[0].replace('_', ' ')
        disease = parts[1].replace('_', ' ')
        return crop, disease
    return "Unknown Crop", label

def main():
    st.set_page_config(
        page_title="Crop Disease Detector",
        page_icon="🔬",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main { background-color: #f5f7f5; }
        .stButton>button {
            background-color: #4CAF50; color: white; border-radius: 8px;
            border: none; padding: 10px 24px; font-weight: 500; font-size: 16px;
        }
        .stButton>button:hover { background-color: #45a049; }
        .report-section {
            background-color: white; padding: 20px; border-radius: 10px;
            border-left: 4px solid #FF9800; margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .chat-message { padding: 12px; border-radius: 8px; margin-bottom: 10px; color: #1e1e1e; }
        .user-message { background-color: #e8f5e9; border-left: 4px solid #4CAF50; }
        .assistant-message { background-color: #ffffff; border-left: 4px solid #2196F3; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔬 AI-Powered Crop Disease Detector")
    st.markdown("**Upload a leaf image for instant diagnosis with AI-powered treatment recommendations**")
    st.markdown("*छवि अपलोड करें और AI से तुरंत निदान और उपचार सुझाव प्राप्त करें*")
    st.markdown("---")
    
    # Initialize session state
    for key in ["detection_done", "detected_disease", "detected_crop", "ai_report", "qa_messages", "confidence", "full_label"]:
        if key not in st.session_state:
            st.session_state[key] = False if key == "detection_done" else None
    
    client = get_client()
    api_available = client is not None
    
    if not api_available:
        st.warning("⚠️ **AI Features Limited**: Add `ZAI_API_KEY` or `OPENAI_API_KEY` in Streamlit Secrets to enable AI-powered disease reports and Q&A.")
    
    # Load the model
    with st.spinner("Loading disease detection model..."):
        model = load_model()
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Crop Image")
        uploaded_file = st.file_uploader(
            "Choose a leaf image (JPG or PNG)", 
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the affected crop leaf for best results"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_container_width=True)
            
            if st.button('🔍 Diagnose Crop Disease', use_container_width=True):
                with st.spinner('🔬 Analyzing image for diseases...'):
                    label, confidence = predict_image(uploaded_file, model)
                    crop_name, disease_name = parse_disease_label(label)
                    
                    st.session_state.detection_done = True
                    st.session_state.detected_disease = disease_name
                    st.session_state.detected_crop = crop_name
                    st.session_state.confidence = confidence
                    st.session_state.full_label = label
                    
                    if api_available:
                        with st.spinner('🤖 Generating AI-powered disease report...'):
                            st.session_state.ai_report = generate_disease_report(
                                client, disease_name, crop_name, confidence
                            )
                    st.session_state.qa_messages = []
                st.rerun()
    
    with col2:
        if st.session_state.detection_done:
            st.subheader("📊 Diagnosis Result")
            if "healthy" in st.session_state.full_label.lower():
                st.success(f"✅ **Status: {st.session_state.detected_disease}**")
                st.balloons()
            else:
                st.error(f"⚠️ **Disease Detected: {st.session_state.detected_disease}**")
            
            st.info(f"**Crop**: {st.session_state.detected_crop}")
            st.metric("Confidence Level", f"{st.session_state.confidence:.1%}")
            
            if st.button("🔄 Analyze Another Image", use_container_width=True):
                for key in ["detection_done", "detected_disease", "detected_crop", "ai_report", "qa_messages", "confidence", "full_label"]:
                    st.session_state[key] = False if key == "detection_done" else None
                st.rerun()
    
    # Display AI Report
    if st.session_state.detection_done and st.session_state.ai_report:
        st.markdown("---")
        st.subheader("🤖 AI-Generated Disease Management Report")
        st.markdown(f'<div class="report-section">{st.session_state.ai_report}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader(f"💬 Ask Questions About {st.session_state.detected_disease}")
        st.markdown(f"*Have specific questions about treating **{st.session_state.detected_disease}** on your **{st.session_state.detected_crop}**? Ask away!*")
        
        for msg in st.session_state.qa_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🧑‍🌾 You:</strong><br>{msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Expert:</strong><br>{msg["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([5, 1])
        with col1:
            user_question = st.text_input(
                "Ask your question:",
                placeholder=f"e.g., What is the best organic treatment? / कौन सा जैविक उपचार सबसे अच्छा है?",
                key="disease_question", label_visibility="collapsed"
            )
        with col2:
            ask_button = st.button("Ask 💬", use_container_width=True)
        
        st.markdown("**Quick Questions:**")
        q_col1, q_col2, q_col3 = st.columns(3)
        with q_col1:
            if st.button("💊 Best treatment?"):
                user_question = f"What is the most effective treatment for {st.session_state.detected_disease}?"
                ask_button = True
        with q_col2:
            if st.button("🌱 Organic options?"):
                user_question = f"What are the organic treatment options for {st.session_state.detected_disease}?"
                ask_button = True
        with q_col3:
            if st.button("⏱️ Recovery time?"):
                user_question = f"How long does it take to recover from {st.session_state.detected_disease}?"
                ask_button = True
        
        if ask_button and user_question.strip():
            st.session_state.qa_messages.append({"role": "user", "content": user_question})
            with st.spinner("🤔 Getting expert answer..."):
                ai_answer = get_disease_context_response(
                    client, user_question,
                    st.session_state.detected_disease,
                    st.session_state.detected_crop,
                    st.session_state.qa_messages[:-1]
                )
            st.session_state.qa_messages.append({"role": "assistant", "content": ai_answer})
            st.rerun()
    
    elif st.session_state.detection_done and not api_available:
        st.markdown("---")
        st.info("💡 **Enable AI features** by adding `ZAI_API_KEY` in Streamlit Secrets for detailed disease reports and expert Q&A!")
    
    st.markdown("---")
    st.caption("⚠️ **Disclaimer**: AI-generated recommendations are for guidance only. Always consult local agricultural experts for serious crop diseases.")
    st.caption("🌾 **Supported Crops**: Corn, Potato, Rice, Sugarcane, Wheat | **Total Diseases**: 17")

if __name__ == "__main__":
    main()