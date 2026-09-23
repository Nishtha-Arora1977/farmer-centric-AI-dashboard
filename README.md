# Farmer-Centric AI Dashboard

A Streamlit-based AI dashboard designed for farmers to access crop disease detection, AI-powered advisory, weather information, and market prices in one unified interface.

> **Project note**: Aksara replaced by GPT 4.1-mini. CNN model working fine. Weather_market not working.

## Features

### 1. 🧠 AI Assistant
LLM-powered assistant for general farming queries. Uses Hugging Face transformers / OpenAI API via `utils/api_handlers.py`.

### 2. 🔬 Crop Disease Detector
Upload a leaf image for instant disease diagnosis using a trained PyTorch model:
* Model: EfficientNetV2-Small
* Model file: `models/EfficientNetV2-Small_best_model.pth`
* Supports crops: Corn, Potato, Rice, Sugarcane, Wheat
* 17 diseases covered
* AI-generated disease management report in English + Hindi
* Follow-up Q&A with the detected disease context

### 3. 🌤️ Weather Tracker
Displays external weather API data for farming decisions. Implemented in `pages/3_Weather.py`.

### 4. 📈 Market Price
Local market price analysis from `data/market_prices.csv`. Implemented in `pages/4_Market_Price.py`.

## Tech Stack

* **Frontend**: Streamlit
* **ML/DL**: PyTorch, TorchVision, timm
* **AI**: Transformers, SentencePiece, OpenAI API
* **Data**: pandas, requests, Pillow
* **Deployment**: Streamlit `Home.py` entry point with `pages/` auto-routing

## Project Structure

```
farmer-centric-AI-dashboard/
├── Home.py                 # Main Streamlit entry
├── requirements.txt
├── .gitignore
├── data/
│   └── market_prices.csv
├── models/
│   ├── EfficientNetV2-Small_best_model.pth
│   ├── aksara_v1.py
│   └── cnn_model.py
├── pages/
│   ├── 1_AI_Assistant.py
│   ├── 2_Detector.py
│   ├── 3_Weather.py
│   └── 4_Market_Price.py
└── utils/
    ├── api_handlers.py
    └── model_inference.py
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/Nishtha-Arora1977/farmer-centric-AI-dashboard.git
cd farmer-centric-AI-dashboard
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set API keys
The AI Assistant and Disease Detector optionally use OpenAI API. Add your key in `pages/2_Detector.py` and `pages/1_AI_Assistant.py` or via Streamlit secrets:
```bash
mkdir .streamlit
echo "[secrets]\nOPENAI_API_KEY = 'sk-...'" > .streamlit/secrets.toml
```

## Usage

Run the Streamlit app locally:
```bash
streamlit run Home.py
```

Open the local URL shown in terminal, e.g., http://localhost:8501

### Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to https://share.streamlit.io and connect your GitHub account
3. Select `Nishtha-Arora1977/farmer-centric-AI-dashboard`
4. Main file: `Home.py`
5. Add secrets in the dashboard → Settings → Secrets using `.streamlit/secrets.toml.example` as template:
   ```
   OPENAI_API_KEY = "sk-..."
   TOMORROW_API_KEY = "xxx"
   ```
6. Deploy. Git LFS is supported for the model file.

**Note:** The model `models/EfficientNetV2-Small_best_model.pth` is tracked with Git LFS to keep the repo under GitHub limits.

Navigate using the left sidebar:
* **Home** – Project overview
* **1. AI Assistant** – Chat with farming AI
* **2. Detector** – Upload leaf image for disease detection
* **3. Weather** – Weather insights
* **4. Market Price** – Market price trends

## Model Details

* Architecture: EfficientNetV2-Small
* Weights: `models/EfficientNetV2-Small_best_model.pth` ~78 MB
* Inference utilities: `utils/model_inference.py`
* Loading & prediction handled in `pages/2_Detector.py`

## Data

* `data/market_prices.csv` – Historical market prices for analysis

## Notes & Limitations

* Weather and Market modules were reported as not fully working in the original repo.
* AI features require valid OpenAI API key. If not set, detector will run without AI report/Q&A.
* Large model file >50 MB – consider Git LFS for future contributions.

## Disclaimer

AI-generated recommendations are for guidance only. Always consult local agricultural experts for serious crop diseases.

## License

Add license as per your preference.

## Contributing

Pull requests welcome. Please ensure model files are handled via LFS and tests pass.


