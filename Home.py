import streamlit as st

st.set_page_config(
    page_title="FarmSathi - Farmer AI Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean dashboard look
st.markdown("""
    <style>
    .main { background-color: #f8faf8; }
    .stButton>button {
        background-color: #2E7D32; color: white; border-radius: 10px;
        border: none; padding: 1rem 1.5rem; font-weight: 600; font-size: 1.1rem;
        width: 100%; height: 100%; transition: all 0.2s;
    }
    .stButton>button:hover { background-color: #1B5E20; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(46,125,50,0.3); }
    .feature-card {
        background: white; padding: 2rem; border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e8f5e9;
        height: 100%; transition: all 0.2s;
    }
    .feature-card:hover { box-shadow: 0 8px 24px rgba(46,125,50,0.15); transform: translateY(-4px); }
    .feature-icon { font-size: 3rem; margin-bottom: 1rem; }
    .feature-title { font-size: 1.3rem; font-weight: 700; color: #1B5E20; margin-bottom: 0.5rem; }
    .feature-desc { color: #424242; line-height: 1.6; }
    .stat-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }
    .stat-value { font-size: 2.5rem; font-weight: 700; color: #2E7D32; }
    .stat-label { color: #616161; font-size: 0.9rem; margin-top: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌾 FarmSathi - Farmer AI Dashboard")
    st.markdown("*Your intelligent farming companion: Disease Detection • AI Advisory • Weather • Market Prices*")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

st.markdown("---")

# Quick stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-card"><div class="stat-value">17</div><div class="stat-label">Diseases Detected</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><div class="stat-value">5</div><div class="stat-label">Crops Supported</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><div class="stat-value">AI</div><div class="stat-label">Powered by Z.ai GLM-4.5</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-card"><div class="stat-value">24/7</div><div class="stat-label">Available Anytime</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Feature cards - main navigation
st.subheader("🚀 Quick Access")

col1, col2 = st.columns(2)

with col1:
    # AI Assistant Card
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Farming Assistant</div>
        <div class="feature-desc">
            Ask any farming question in English, Hindi, or Hinglish. Get instant, practical advice on crops, soil, pests, irrigation, government schemes, and more. Powered by Z.ai GLM-4.5.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💬 Open AI Assistant", key="open_ai", use_container_width=True):
        st.switch_page("pages/1_AI_Assistant.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Weather Card
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌤️</div>
        <div class="feature-title">Weather Dashboard</div>
        <div class="feature-desc">
            5-day forecast with temperature charts, rain probability, wind speed. Get crop-specific advisories and irrigation guidance based on real-time weather data from Tomorrow.io.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🌦️ Check Weather", key="open_weather", use_container_width=True):
        st.switch_page("pages/3_Weather.py")

with col2:
    # Disease Detector Card
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔬</div>
        <div class="feature-title">Crop Disease Detector</div>
        <div class="feature-desc">
            Upload a leaf photo for instant AI diagnosis across 17 diseases in 5 crops (Corn, Potato, Rice, Sugarcane, Wheat). Get detailed treatment reports with organic & chemical options, plus follow-up Q&A.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Detect Disease", key="open_detector", use_container_width=True):
        st.switch_page("pages/2_Detector.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Market Price Card
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Market Price Tracker</div>
        <div class="feature-desc">
            Track commodity prices across markets with interactive charts. Filter by crop, view min/max/modal prices, and download data. Covers major agricultural markets.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📊 View Market Prices", key="open_market", use_container_width=True):
        st.switch_page("pages/4_Market_Price.py")

st.markdown("<br>", unsafe_allow_html=True)

# Bottom info bar
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("🌱 **Supported Crops:** Corn • Potato • Rice • Sugarcane • Wheat")
with col2:
    st.info("🛡️ **Diseases:** 17 classes including blight, rust, rot, spots & healthy")
with col3:
    st.info("🌐 **Languages:** English • हिंदी • Hinglish")

st.caption("💡 Tip: Use the sidebar to navigate between pages. All AI features require ZAI_API_KEY in Streamlit Secrets.")