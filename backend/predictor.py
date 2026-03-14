import joblib
import pandas as pd
import numpy as np
import os
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'career_model.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'models', 'label_encoder.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'models', 'vectorizer.pkl')
CAREER_INFO_PATH = os.path.join(BASE_DIR, 'dataset', 'career_info.xlsx')

_model = None
_encoder = None
_vectorizer = None
_career_info_df = None


def load_models():
    global _model, _encoder, _vectorizer, _career_info_df
    if _model is None:
        _model = joblib.load(MODEL_PATH)
        _encoder = joblib.load(ENCODER_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)
    if _career_info_df is None:
        _career_info_df = pd.read_excel(CAREER_INFO_PATH)
    return _model, _encoder, _vectorizer, _career_info_df


def predict_career(skills: List[str]) -> Dict[str, Any]:
    """Predict best career and top 3 careers from a list of skills."""
    model, encoder, vectorizer, career_info_df = load_models()

    skills_text = ', '.join([s.lower().strip() for s in skills])
    X = vectorizer.transform([skills_text])

    # Get probabilities for all classes
    proba = model.predict_proba(X)[0]
    top_indices = np.argsort(proba)[::-1][:5]

    top_careers = []
    for idx in top_indices:
        career_name = encoder.classes_[idx]
        confidence = round(float(proba[idx]) * 100, 1)
        career_data = get_career_info(career_name, career_info_df)
        top_careers.append({
            "career": career_name,
            "confidence": confidence,
            **career_data
        })

    best = top_careers[0]
    return {
        "best_career": best["career"],
        "confidence": best["confidence"],
        "description": best.get("description", ""),
        "average_salary": best.get("average_salary", ""),
        "top_companies": best.get("top_companies", ""),
        "learning_path": best.get("learning_path", ""),
        "key_skills": best.get("key_skills", ""),
        "top_3": [
            {"career": c["career"], "confidence": c["confidence"]}
            for c in top_careers[:3]
        ]
    }


def get_career_info(career_name: str, df: pd.DataFrame) -> Dict[str, str]:
    """Fetch career information from the info dataset."""
    row = df[df['Career Role'].str.lower() == career_name.lower()]
    if row.empty:
        return {
            "description": f"{career_name} is an exciting career in the modern tech landscape.",
            "average_salary": "8-15 LPA",
            "top_companies": "TCS, Infosys, Wipro, Accenture, IBM",
            "learning_path": "Foundation → Core Skills → Advanced → Certification → Projects",
            "key_skills": career_name + " related skills"
        }
    row = row.iloc[0]
    return {
        "description": str(row.get('Description', '')),
        "average_salary": str(row.get('Average Salary (LPA)', '')),
        "top_companies": str(row.get('Top Companies', '')),
        "learning_path": str(row.get('Learning Path', '')),
        "key_skills": str(row.get('Key Skills', ''))
    }


def get_all_career_info() -> List[Dict]:
    """Return all career info from the dataset."""
    _, _, _, career_info_df = load_models()
    return career_info_df.fillna('').to_dict(orient='records')
