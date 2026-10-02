import re


SKILLS = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "statistics",
    "machine learning",
    "data analysis",
    "data visualization",
    "postgresql",
    "mysql",
    "mongodb",
    "etl",
    "r",
    "scikit-learn",
    "tensorflow",
    "powerpoint",
    "git",
    "github"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills