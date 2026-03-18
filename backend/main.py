from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import io
from typing import Optional, List

from backend.skill_extractor import extract_skills, normalize_skills, skills_to_string
from backend.predictor import predict_career, get_all_career_info
from backend.auth import signup_user, login_user, save_prediction

# PDF / DOCX extractors
try:
    import PyPDF2
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "uploads",
    "resumes"
)
os.makedirs(UPLOAD_DIR, exist_ok=True)


app = FastAPI(
    title="CareerFit AI API",
    description="AI-powered Career Prediction API",
    version="1.0.0"
)

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://careerfit-ai-tau.vercel.app",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ PRE-FLIGHT FIX (IMPORTANT)
@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    return JSONResponse(content={"message": "OK"})


# ─── Pydantic Models ─────────────────────────────────────────────────────────

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class SkillsRequest(BaseModel):
    skills: str
    email: Optional[str] = None


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "CareerFit AI Backend is running 🚀", "version": "1.0.0"}


@app.post("/signup")
def signup(req: SignupRequest):
    result = signup_user(req.name, req.email, req.password)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/login")
def login(req: LoginRequest):
    result = login_user(req.email, req.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result


@app.post("/predict-skills")
def predict_from_skills(req: SkillsRequest):
    """Predict career from manually entered skills."""
    if not req.skills.strip():
        raise HTTPException(status_code=400, detail="Skills cannot be empty")

    skills = normalize_skills(req.skills)

    if not skills:
        raise HTTPException(status_code=400, detail="No valid skills found")

    result = predict_career(skills)

    if req.email:
        save_prediction(req.email, {
            "type": "skills",
            "input": req.skills,
            "result": result["best_career"]
        })

    return {
        "success": True,
        "skills_detected": skills,
        "prediction": result
    }


@app.post("/predict")
async def predict_from_resume(
    file: UploadFile = File(...),
    email: Optional[str] = Form(None)
):
    """Predict career from uploaded resume (PDF or DOCX)."""

    filename = file.filename.lower()

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".docx")
        or filename.endswith(".doc")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    # Save file
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    contents = await file.read()

    with open(save_path, "wb") as f:
        f.write(contents)

    # Extract text
    text = ""

    try:
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(contents)
        else:
            text = extract_text_from_docx(save_path)

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Could not read file: {str(e)}"
        )

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from the file"
        )

    # Extract skills
    skills = extract_skills(text)

    if not skills:
        skills = normalize_skills(text[:500])

    if not skills:
        raise HTTPException(
            status_code=422,
            detail="No recognizable skills found in resume"
        )

    result = predict_career(skills)

    if email:
        save_prediction(email, {
            "type": "resume",
            "filename": file.filename,
            "result": result["best_career"]
        })

    return {
        "success": True,
        "filename": file.filename,
        "skills_detected": skills,
        "prediction": result
    }


@app.get("/career-info")
def career_info():
    """Get all career information from dataset."""
    careers = get_all_career_info()

    return {
        "success": True,
        "count": len(careers),
        "careers": careers
    }


# ─── Helpers ─────────────────────────────────────────────────────────────────

def extract_text_from_pdf(contents: bytes) -> str:
    if not HAS_PYPDF:
        return ""

    reader = PyPDF2.PdfReader(io.BytesIO(contents))

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def extract_text_from_docx(filepath: str) -> str:
    if not HAS_DOCX:
        return ""

    doc = Document(filepath)

    return "\n".join([para.text for para in doc.paragraphs])