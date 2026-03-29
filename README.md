# Dev Nautics CRM Dashboard 🎓

A professional 10-page CRM dashboard for **Dev Nautics** — education tuition business in Surat, Gujarat.  
Built with **Python + Streamlit + Plotly**. Single-file architecture — zero import issues on Streamlit Cloud.

🌐 **Website**: [devnautics.com](https://devnautics.com) · 📞 8866713206  
📍 U-33 Corner Point, Citylight, Surat – 395007

---

## 🚀 Deploy in 3 Steps

### Option A — Streamlit Cloud (Free, Recommended)
1. Push this repo to GitHub (upload the extracted zip)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select repo → branch `main` → file `app.py` → **Deploy** ✅

### Option B — Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📄 10 Dashboard Pages

| # | Page | Highlights |
|---|------|-----------|
| 1 | 🏠 Executive Overview | KPI cards, revenue trend, health gauge, pipeline funnel |
| 2 | 👦 Student Management | Roster, heatmap, scatter, gender split |
| 3 | 📋 Services | 8 service cards, enrollment & revenue charts |
| 4 | 📦 Products & Inventory | Catalog, downloads, PAN India shipping map |
| 5 | 💰 Revenue & Finance | Waterfall, stacked bar, fee status pie |
| 6 | 📣 Leads & Enquiries | Funnel, source pie, conversion by channel |
| 7 | ⭐ Testimonials & Feedback | NPS gauge, sentiment, review cards |
| 8 | 📊 Academic Performance | Before/after bars, Olympiad medals, leaderboard |
| 9 | 👩‍🏫 Staff & Operations | Directory, payroll, batch capacity, job pipeline |
| 10 | 📡 Social & Digital | Follower trends, traffic, downloads, WhatsApp leads |

---

## 📂 Structure

```
devnautics-dashboard/
├── app.py               ← All 10 pages in one file (no import issues)
├── requirements.txt     ← streamlit, plotly, pandas
├── .streamlit/
│   └── config.toml      ← Teal-green theme
└── data/
    ├── students.csv
    ├── revenue.csv
    ├── leads.csv
    ├── feedback.csv
    ├── staff.csv
    ├── performance.csv
    └── social.csv
```

## ✏️ Using Real Data
Open any CSV in `/data/`, replace sample rows with real data, keep column names unchanged.

## 🛠️ Tech Stack
Python 3.11 · Streamlit · Plotly Express · Pandas
