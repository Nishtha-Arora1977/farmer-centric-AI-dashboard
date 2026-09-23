# pages/3_Weather.py
import streamlit as st
import pandas as pd
from utils.api_handlers import get_weather, get_weather_icon, detect_severe_alerts, crop_advisory, irrigation_advice

st.set_page_config(page_title="Weather Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f5; }
    .stButton>button {
        background-color: #2196F3; color: white; border-radius: 8px;
        border: none; padding: 10px 24px; font-weight: 500;
    }
    .stButton>button:hover { background-color: #1976D2; }
    .metric-card {
        background: white; padding: 1rem; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid #2196F3;
    }
    .alert-card {
        background: #fff3e0; padding: 1rem; border-radius: 8px;
        border-left: 4px solid #FF9800; margin: 0.5rem 0;
    }
    .success-card {
        background: #e8f5e9; padding: 1rem; border-radius: 8px;
        border-left: 4px solid #4CAF50; margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌾 Farmer Weather Dashboard")
st.markdown("Get 5-day forecast, charts, alerts and crop advisories.")

col_input, col_crop = st.columns([3, 1])
with col_input:
    city_input = st.text_input("Enter City Name (or location):", "Delhi", help="City name, e.g. 'Delhi' or 'Ludhiana,IN'")

with col_crop:
    crop_choice = st.selectbox("Crop (for advisory):", ["Wheat", "Rice", "Maize", "Generic"])

if st.button("Get Weather", use_container_width=True):
    with st.spinner("Fetching forecast..."):
        result = get_weather(city_input, days=5)

    if 'error' in result:
        st.error(result['error'])
    else:
        city = result.get("city", city_input)
        current = result.get("current", {})
        daily = result.get("daily", [])

        # Current Weather - Top metrics
        st.subheader(f"Current Weather — {city}")
        icon = get_weather_icon(current.get("weatherCode", None) or current.get("weather_code", None) or 1000)
        
        cols = st.columns(5)
        with cols[0]:
            st.metric("Location", city)
        with cols[1]:
            st.metric("Temperature (°C)", current.get("temperature", "N/A"))
        with cols[2]:
            st.metric("Humidity (%)", current.get("humidity", "N/A"))
        with cols[3]:
            st.metric("Wind (m/s)", current.get("windSpeed", "N/A"))
        with cols[4]:
            st.metric("Rain Prob (%)", current.get("precipitationProbability", "N/A"))

        st.markdown(f"### {icon} Condition (code: {current.get('weatherCode','N/A')})")
        st.markdown("---")

        # Charts
        df = pd.DataFrame(daily)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date').sort_index()
            
            tab1, tab2, tab3 = st.tabs(["🌡️ Temperature", "🌧️ Rain Probability", "💨 Wind Speed"])
            
            with tab1:
                temp_df = df[['temp_min', 'temp_max']].rename(columns={'temp_min': 'Min', 'temp_max': 'Max'})
                st.line_chart(temp_df)
            
            with tab2:
                rain_df = df[['rain_chance']].rename(columns={'rain_chance': 'RainChance'})
                st.line_chart(rain_df)
            
            with tab3:
                wind_df = df[['wind_avg']].rename(columns={'wind_avg': 'Wind'})
                st.line_chart(wind_df)
        else:
            st.info("No daily forecast data available for charts.")

        st.markdown("---")

        # Alerts
        st.subheader("⚠️ Rule-based Alerts")
        alerts = detect_severe_alerts(result)
        if alerts:
            for a in alerts:
                st.markdown(f'<div class="alert-card">{a}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-card">✅ No severe alerts detected by rule-set.</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Crop Advisory
        st.subheader("🌱 Crop Advisory")
        advice = crop_advisory(result, crop_choice)
        st.info(advice)

        # Irrigation Advice
        st.subheader("💧 Irrigation Guidance")
        irr = irrigation_advice(result)
        st.info(irr)

        st.markdown("---")
        st.subheader("📅 5-Day Forecast")
        if daily:
            for day in daily:
                d_icon = get_weather_icon(day.get("weather_code"))
                date_str = day.get("date", "")[:10]
                temp_min = day.get("temp_min", "N/A")
                temp_max = day.get("temp_max", "N/A")
                rain = day.get("rain_chance", "N/A")

                with st.expander(f"{date_str} {d_icon}  |  🌡️ {temp_min}–{temp_max} °C  |  🌧 {rain}% Rain"):
                    st.markdown(f"""
                    - **Min/Max Temp**: {temp_min} / {temp_max} °C
                    - **Rain Chance**: {rain}%
                    - **Weather**: {d_icon} (code: {day.get('weather_code', 'N/A')})
                    """)
        else:
            st.info("No forecast data available.")