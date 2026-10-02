SUGGESTIONS = {
    "statistics": (
        "Strengthen your knowledge of descriptive statistics, "
        "probability, distributions, and basic statistical analysis."
    ),

    "machine learning": (
        "Consider adding a machine learning project or mentioning "
        "relevant ML experience in your resume."
    ),

    "data visualization": (
        "Showcase your ability to present insights through charts, "
        "dashboards, or interactive visualizations."
    ),

    "power bi": (
        "Add a Power BI dashboard project or highlight your experience "
        "creating interactive reports."
    ),

    "tableau": (
        "Consider adding a Tableau dashboard project to demonstrate "
        "your data visualization skills."
    ),

    "sql": (
        "Highlight SQL projects or practical experience involving "
        "queries, joins, aggregations, and data analysis."
    ),

    "python": (
        "Showcase Python-based data analysis projects using libraries "
        "such as Pandas, NumPy, or Matplotlib."
    ),

    "excel": (
        "Highlight practical Excel work involving formulas, pivot tables, "
        "data cleaning, or dashboards."
    ),

    "pandas": (
        "Mention projects where you used Pandas for data cleaning, "
        "transformation, or analysis."
    ),

    "numpy": (
        "Highlight how you have used NumPy for numerical analysis "
        "or data preprocessing."
    )
}


def get_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        if skill in SUGGESTIONS:
            suggestions.append({
                "skill": skill,
                "suggestion": SUGGESTIONS[skill]
            })

    return suggestions