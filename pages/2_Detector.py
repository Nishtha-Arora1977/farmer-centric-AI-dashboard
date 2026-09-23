import streamlit as st

st.set_page_config(page_title="Detector", page_icon="🔬")
st.title("🔬 Crop Disease Detector")

st.warning("Detector is not available on Vercel deployment.")
st.info("""
The disease detector requires PyTorch and a 78 MB model file, which are not supported on Vercel's serverless platform.

Please use Streamlit Community Cloud or a VM for full functionality.

For local development:
```bash
pip install -r requirements.txt
streamlit run Home.py
```
""")
