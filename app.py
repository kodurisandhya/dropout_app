from flask import Flask, render_template, request
import os

app = Flask(__name__)

def predict_dropout(attendance, grades, participation, financial_issue, family_support, health_issue):
    score = 0
    if attendance < 75: score += 1
    if grades < 50: score += 1
    if participation < 5: score += 1
    if financial_issue == "Yes": score += 1
    if family_support == "Poor": score += 1
    if health_issue == "Yes": score += 1

    if score >= 4:
        return "High Risk", ["Immediate counseling required", "Check financial aid", "Provide health support"]
    elif score >= 2:
        return "Moderate Risk", ["Monitor closely", "Offer academic help"]
    else:
        return "Low Risk", ["Encourage continued performance"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            attendance = float(request.form.get("attendance", 0))
            grades = float(request.form.get("grades", 0))
            participation = int(request.form.get("participation", 0))
            financial_issue = request.form.get("financial_issue", "No")
            family_support = request.form.get("family_support", "Good")
            health_issue = request.form.get("health_issue", "No")

            risk, suggestions = predict_dropout(
                attendance, grades, participation,
                financial_issue, family_support, health_issue
            )

            return render_template("index.html", risk=risk, suggestions=suggestions)
        except Exception as e:
            return f"Error: {e}", 500

    return render_template("index.html", risk=None, suggestions=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
