# CareerFit AI 🚀

> AI-powered career prediction platform — upload your resume or enter your skills and get matched to your ideal career path using Machine Learning.

---

## ✨ Features

- 🧠 **ML-Powered** — RandomForest classifier trained on 100+ career roles
- 📄 **Resume Parsing** — Extracts skills from PDF and DOCX resumes automatically
- ⌨️ **Manual Skills Input** — Tag-based skill entry with suggestions
- 🎯 **Top 3 Predictions** — Best match + confidence scores for top 3 careers
- 💼 **Career Insights** — Salary, top companies, learning path per career
- 👤 **User Auth** — Signup/Login with JSON-based user storage
- 🌐 **Modern UI** — Dark futuristic design with animations

---

## 🗂️ Project Structure

```
careerfit-ai/
├── backend/
│   ├── main.py             # FastAPI app with all endpoints
│   ├── predictor.py        # ML prediction logic
│   ├── skill_extractor.py  # NLP/regex skill extraction
│   ├── auth.py             # User authentication
│   ├── models/
│   │   ├── career_model.pkl
│   │   ├── label_encoder.pkl
│   │   └── vectorizer.pkl
│   ├── dataset/
│   │   ├── career_data.xlsx   # Training data (100+ roles)
│   │   └── career_info.xlsx   # Career descriptions (96+ roles)
│   └── requirements.txt
├── frontend/
│   ├── index.html          # Login / Signup page
│   ├── dashboard.html      # Main dashboard
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js          # REST API calls
│       ├── login.js        # Auth logic
│       └── dashboard.js    # Dashboard logic
├── uploads/
│   └── resumes/            # Uploaded resume storage
├── users.json              # User data (auto-created)
├── run_backend.bat         # Windows quick-start
└── README.md
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.9+
- pip

### Step 1 — Clone or Extract
```bash
# If from ZIP, extract and navigate:
cd careerfit-ai
```

### Step 2 — Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3 — Train the ML Model (first time only)
```bash
# From the project root:
python train_model.py
```
> Models are already pre-trained and included in `backend/models/`

---

## 🚀 Running the Application

### Start Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload
```
Backend will be available at: **http://127.0.0.1:8000**

**API Docs:** http://127.0.0.1:8000/docs

### Open Frontend
Simply open `frontend/index.html` in your browser.

> For best results, use a local server:
> ```bash
> cd frontend
> python -m http.server 5500
> # Then open: http://localhost:5500
> ```

### Windows Quick Start
Double-click `run_backend.bat` to start the backend automatically.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Create new user account |
| POST | `/login` | Authenticate user |
| POST | `/predict` | Predict career from resume (PDF/DOCX) |
| POST | `/predict-skills` | Predict career from skill list |
| GET | `/career-info` | Get all career information |

---

## 🤖 ML Model Details

- **Algorithm:** RandomForestClassifier (200 trees)
- **Vectorizer:** TF-IDF with bigrams
- **Training Data:** 100 career roles × 5 augmented samples
- **Accuracy:** ~95% on test set
- **Output:** Top 3 careers with confidence scores

---

## 💡 Demo Account

Use the **"Fill Demo Credentials"** button on the login page, or register manually.

To create a demo user, sign up with:
- Email: `demo@careerfit.ai`
- Password: `demo123`

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI, Uvicorn |
| ML | Scikit-learn, RandomForest, TF-IDF |
| Data | Pandas, Openpyxl |
| Resume | PyPDF2, python-docx |
| Frontend | HTML5, CSS3, Vanilla JS |
| Auth | SHA-256 hashed passwords, JSON storage |

---

## 📊 Dataset

### career_data.xlsx (Training)
100 career roles with: Required Skills, Personality Type, Learning Topics, Avg Salary

### career_info.xlsx (Insights)
96 career roles with: Description, Key Skills, Average Salary, Top Indian Companies, Learning Path

---

## 🌐 Browser Support
Chrome, Firefox, Edge, Safari (any modern browser)

---

*Built with ❤️ using FastAPI + Scikit-learn + Vanilla JS*
