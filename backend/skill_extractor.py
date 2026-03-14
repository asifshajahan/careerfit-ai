import re
from typing import List

SKILL_KEYWORDS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "golang", "go",
    "rust", "kotlin", "swift", "scala", "r", "matlab", "php", "ruby", "perl",
    "dart", "bash", "shell", "sql", "nosql", "solidity",

    # Web Frontend
    "html", "css", "react", "reactjs", "vuejs", "vue", "angular", "angularjs",
    "nextjs", "nuxtjs", "jquery", "bootstrap", "tailwind", "sass", "scss",
    "webpack", "vite", "typescript",

    # Backend
    "nodejs", "node", "expressjs", "django", "fastapi", "flask", "spring",
    "spring boot", "rest api", "restful", "graphql", "grpc", "microservices",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra", "elasticsearch",
    "sqlite", "oracle", "firebase", "dynamodb", "bigquery", "snowflake",

    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform",
    "ansible", "jenkins", "ci/cd", "github actions", "linux", "git",
    "helm", "prometheus", "grafana", "nginx", "apache",

    # Machine Learning / AI
    "machine learning", "deep learning", "neural networks", "nlp",
    "natural language processing", "computer vision", "tensorflow", "pytorch",
    "keras", "scikit-learn", "sklearn", "pandas", "numpy", "matplotlib",
    "huggingface", "transformers", "bert", "gpt", "llm", "mlops",
    "feature engineering", "statistics", "data science",

    # Data
    "data analysis", "data visualization", "tableau", "power bi", "excel",
    "data engineering", "etl", "spark", "hadoop", "kafka", "airflow",
    "data warehouse", "dbt", "looker",

    # Security
    "cybersecurity", "ethical hacking", "penetration testing", "kali linux",
    "metasploit", "burp suite", "siem", "splunk", "osint", "forensics",
    "cryptography", "network security", "firewall", "ssl",

    # Mobile
    "android", "ios", "flutter", "react native", "swift", "kotlin", "firebase",

    # Design
    "figma", "adobe xd", "photoshop", "illustrator", "sketch", "ux", "ui",
    "user research", "wireframing", "prototyping", "canva",

    # Project Management
    "agile", "scrum", "kanban", "jira", "confluence", "product management",
    "project management", "pmp", "lean", "six sigma",

    # Other Technical
    "blockchain", "solidity", "web3", "smart contracts", "iot", "embedded",
    "rtos", "microcontrollers", "arduino", "raspberry pi", "ros",
    "unity", "unreal engine", "opengl", "webgl",

    # Business / Finance
    "excel", "financial modeling", "accounting", "taxation", "audit", "sap",
    "salesforce", "crm", "erp", "tally", "gst",

    # Domain Keywords
    "networking", "tcp/ip", "routing", "switching", "ccna", "vpn",
    "autocad", "revit", "solidworks", "catia", "ansys", "gis", "arcgis",
    "research", "statistics", "econometrics", "stata",
]

def extract_skills(text: str) -> List[str]:
    """Extract skills from text using keyword matching."""
    if not text:
        return []

    text_lower = text.lower()
    # Remove special characters except alphanumeric and spaces
    text_clean = re.sub(r'[^\w\s/#+\-.]', ' ', text_lower)

    found_skills = set()

    # Multi-word skills first
    multi_word = [s for s in SKILL_KEYWORDS if ' ' in s or '/' in s]
    single_word = [s for s in SKILL_KEYWORDS if ' ' not in s and '/' not in s]

    for skill in multi_word:
        if skill in text_clean:
            found_skills.add(skill)

    # Tokenize text for single word matching
    tokens = set(re.findall(r'\b[\w#+./]+\b', text_clean))
    for skill in single_word:
        if skill in tokens:
            found_skills.add(skill)

    return list(found_skills)


def normalize_skills(skills_input: str) -> List[str]:
    """Normalize comma-separated skill input."""
    skills = [s.strip().lower() for s in skills_input.split(',') if s.strip()]
    return skills


def skills_to_string(skills: List[str]) -> str:
    """Convert skill list to string for model input."""
    return ', '.join(skills)
