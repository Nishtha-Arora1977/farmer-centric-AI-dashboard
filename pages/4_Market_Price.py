import streamlit as st
import pandas as pd
from utils.api_handlers import load_market_data

st.set_page_config(page_title="Market Price Tracker", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f5; }
    .stButton>button {
        background-color: #FF9800; color: white; border-radius: 8px;
        border: none; padding: 10px 24px; font-weight: 500;
    }
    .stButton>button:hover { background-color: #F57C00; }
    .price-card {
        background: white; padding: 1rem; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid #FF9800;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Market Price Tracker")
st.markdown("---")

# ----------------------
# MARKET DATA TRACKER
# ----------------------
st.header("📊 Local Market Price Data")

market_df = load_market_data()

if market_df is None or market_df.empty:
    st.warning("Market data could not be loaded. Please check data/market_prices.csv exists.")
else:
    # Fix column names
    market_df = market_df.rename(columns={
        'Min_x0020_Price': 'Min_Price',
        'Max_x0020_Price': 'Max_Price',
        'Modal_x0020_Price': 'Modal_Price'
    })

    # Filter by commodity
    available_items = market_df['Commodity'].unique().tolist()
    selected_item = st.selectbox("Select Commodity:", available_items)

    filtered_df = market_df[market_df['Commodity'] == selected_item].copy()

    st.subheader(f"Price Trend for {selected_item}")

    # Ensure charting works only if column is numeric
    try:
        filtered_df['Modal_Price'] = pd.to_numeric(filtered_df['Modal_Price'], errors='coerce')
        filtered_df['Min_Price'] = pd.to_numeric(filtered_df['Min_Price'], errors='coerce')
        filtered_df['Max_Price'] = pd.to_numeric(filtered_df['Max_Price'], errors='coerce')
        
        # Prepare date column
        if 'Arrival_Date' in filtered_df.columns:
            filtered_df['Arrival_Date'] = pd.to_datetime(filtered_df['Arrival_Date'])
            filtered_df = filtered_df.sort_values('Arrival_Date')
        
        # Price chart
        chart_df = filtered_df[['Arrival_Date', 'Min_Price', 'Modal_Price', 'Max_Price']].set_index('Arrival_Date')
        st.line_chart(chart_df)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_price = filtered_df['Modal_Price'].mean()
            st.metric("Average Modal Price", f"₹{avg_price:.2f}" if pd.notna(avg_price) else "N/A")
        with col2:
            min_price = filtered_df['Min_Price'].min()
            st.metric("Lowest Price", f"₹{min_price:.2f}" if pd.notna(min_price) else "N/A")
        with col3:
            max_price = filtered_df['Max_Price'].max()
            st.metric("Highest Price", f"₹{max_price:.2f}" if pd.notna(max_price) else "N/A")
            
    except Exception as e:
        st.error(f"Error plotting price chart: {e}")

    st.markdown("---")
    st.subheader("📋 Raw Data Table")
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col1:
        show_all = st.checkbox("Show all columns", value=False)
    with col2:
        rows = st.selectbox("Rows to show:", [10, 25, 50, 100], index=1)
    
    display_df = filtered_df if show_all else filtered_df[['Arrival_Date', 'State', 'District', 'Market', 'Min_Price', 'Modal_Price', 'Max_Price']]
    st.dataframe(display_df.head(rows), use_container_width=True, hide_index=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f'{selected_item}_market_prices.csv',
        mime='text/csv',
        use_container_width=True
    )