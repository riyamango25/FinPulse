# 📈 FinPulse Terminal

FinPulse Terminal is a modern stock market dashboard built using **Streamlit** and **FastAPI**. It provides real-time stock information, interactive visualizations, financial statements, market news, portfolio simulation, and AI-generated company summaries powered by Google's Gemini API.

---

## ✨ Features

- 📊 Live stock market data
- 📈 Interactive price charts
- 📰 Latest market news
- 💰 Financial statements & key metrics
- 🤖 AI-generated company summaries
- 📉 Market analytics dashboard
- 💼 Portfolio simulator
- ⭐ Persistent watchlist (saved to the database, survives restarts)

---

## 🛠 Tech Stack

### Frontend
- Streamlit
- Plotly

### Backend
- FastAPI
- SQLAlchemy

### APIs & Data
- Yahoo Finance
- Financial News API
- Google Gemini API

---

## 📂 Project Structure

```text
FinPulse/
│
├── backend/
│   ├── main.py
│   ├── ai_summary.py
│   └── ...
│
├── frontend/
│   ├── app.py
│   ├── charts.py
│   ├── news.py
│   ├── financials.py
│   └── ...
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FinPulse.git

cd FinPulse
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶ Running the Backend

Run this from the **project root** (`FinPulse/`), not from inside `backend/` — the app uses `backend.*` package imports, so it needs to be launched as a module from the root.

```bash
uvicorn backend.main:app --reload
```

---

## ▶ Running the Frontend

Open a new terminal.

```bash
cd frontend

streamlit run app.py
```

---

## 📸 Screenshots

Add screenshots of:

- Dashboard
- AI Summary
- Market Analytics
- Portfolio Simulator

---

## 🔮 Future Improvements

- User authentication
- Price alerts
- Stock comparison mode
- Sector heatmap
- Dark/Light themes

---

## 👩‍💻 Author

Built by **Riya Sardesai**