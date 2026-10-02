from flask import Flask, render_template, request
from pypdf import PdfReader
from utils.skill_extractor import extract_skills
from utils.suggestions import get_suggestions

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    if request.method == "POST":

        resume = request.files.get("resume")
        job_description = request.form.get("job_description")

        if not resume:
            return "Please upload a resume."

        # ==============================
        # READ RESUME PDF
        # ==============================

        reader = PdfReader(resume)

        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text

        # ==============================
        # EXTRACT RESUME SKILLS
        # ==============================

        resume_skills = extract_skills(resume_text)

        # ==============================
        # EXTRACT JD SKILLS
        # ==============================

        jd_skills = extract_skills(job_description)

        # ==============================
        # DETECT REQUIRED / PREFERRED
        # ==============================

        jd_lower = job_description.lower()

        required_skills = []
        preferred_skills = []

        for skill in jd_skills:

            skill_lower = skill.lower()

            # Find where the skill appears in the JD
            skill_position = jd_lower.find(skill_lower)

            # Text around the skill
            surrounding_text = jd_lower[
                max(0, skill_position - 150):
                skill_position + 150
            ]

            # Preferred / optional indicators
            preferred_words = [
                "preferred",
                "plus",
                "nice to have",
                "bonus",
                "optional",
                "desirable",
                "advantage"
            ]

            is_preferred = any(
                word in surrounding_text
                for word in preferred_words
            )

            if is_preferred:
                preferred_skills.append(skill)
            else:
                required_skills.append(skill)

        # ==============================
        # REMOVE DUPLICATES
        # ==============================

        required_skills = list(dict.fromkeys(required_skills))
        preferred_skills = list(dict.fromkeys(preferred_skills))

        # ==============================
        # MATCH REQUIRED SKILLS
        # ==============================

        matched_required = [
            skill for skill in required_skills
            if skill in resume_skills
        ]

        missing_required = [
            skill for skill in required_skills
            if skill not in resume_skills
        ]

        # ==============================
        # MATCH PREFERRED SKILLS
        # ==============================

        matched_preferred = [
            skill for skill in preferred_skills
            if skill in resume_skills
        ]

        missing_preferred = [
            skill for skill in preferred_skills
            if skill not in resume_skills
        ]

        # ==============================
        # CALCULATE WEIGHTED SCORE
        # ==============================

        required_score = 0

        preferred_score = 0

        if required_skills:

            required_score = (
                len(matched_required)
                / len(required_skills)
            ) * 80

        if preferred_skills:

            preferred_score = (
                len(matched_preferred)
                / len(preferred_skills)
            ) * 20

        if required_skills or preferred_skills:

            match_score = round(
                required_score + preferred_score
            )

        else:

            match_score = 0

        # ==============================
        # ALL MATCHED / MISSING SKILLS
        # ==============================

        matched_skills = (
            matched_required +
            matched_preferred
        )

        missing_skills = (
            missing_required +
            missing_preferred
        )

        # ==============================
        # GENERATE SUGGESTIONS
        # ==============================

        suggestions = get_suggestions(missing_skills)

        # ==============================
        # TERMINAL OUTPUT
        # ==============================

        print("\n========== RESUME SKILLS ==========")
        print(resume_skills)

        print("\n========== JD SKILLS ==========")
        print(jd_skills)

        print("\n========== REQUIRED SKILLS ==========")
        print(required_skills)

        print("\n========== PREFERRED SKILLS ==========")
        print(preferred_skills)

        print("\n========== MATCHED REQUIRED ==========")
        print(matched_required)

        print("\n========== MISSING REQUIRED ==========")
        print(missing_required)

        print("\n========== MATCHED PREFERRED ==========")
        print(matched_preferred)

        print("\n========== MISSING PREFERRED ==========")
        print(missing_preferred)

        print("\n========== MATCH SCORE ==========")
        print(match_score)

        print("\n========== SUGGESTIONS ==========")
        print(suggestions)

        # ==============================
        # SEND DATA TO RESULTS PAGE
        # ==============================

        return render_template(
            "results.html",

            match_score=match_score,

            matched_skills=matched_skills,
            missing_skills=missing_skills,

            required_skills=required_skills,
            preferred_skills=preferred_skills,

            matched_required=matched_required,
            missing_required=missing_required,

            matched_preferred=matched_preferred,
            missing_preferred=missing_preferred,

            suggestions=suggestions
        )

    return render_template("analyze.html")


if __name__ == "__main__":
    app.run(debug=True)