from db import save_result
from flask import Flask, render_template, request , redirect

app = Flask(__name__)

chat_history = []

current_category = ""

python_questions = [
    "What is Python?",
    "Explain OOP.",
    "What is a list?",
    "What is a dictionary?"
]

sql_questions = [
    "What is SQL?",
    "What is a Primary Key?",
    "Difference between DELETE and TRUNCATE?",
    "What is JOIN?"
]

hr_questions = [
    "Tell me about yourself.",
    "What are your strengths?",
    "Why should we hire you?",
    "Where do you see yourself in 5 years?"
]

question_index = 0
score = 0


@app.route("/")
def home():

    global chat_history
    global question_index
    global score

    chat_history = []
    question_index = 0
    score = 0

    return render_template("dashboard.html")


@app.route("/interview/<category>", methods=["GET", "POST"])
def interview(category):

    global current_category
    current_category = category

    global question_index
    global score

    if category == "python":
        questions = python_questions

    elif category == "sql":
        questions = sql_questions

    else:
        questions = hr_questions

    if len(chat_history) == 0:

        chat_history.append({
            "type": "ai",
            "message": questions[question_index]
        })

        question_index += 1

    if request.method == "POST":

        user_answer = request.form["answer"]

        chat_history.append({
            "type": "user",
            "message": user_answer
        })

        if len(user_answer) < 20:

            ai_reply = "Your answer is too short. Try explaining more."

        else:

            score += 10

            ai_reply = f"Good answer! 🎉\nCurrent Score: {score}"

        if question_index < len(questions):

            ai_reply += f"\n\nNext Question:\n{questions[question_index]}"

            question_index += 1

        else:

            return redirect("/result")
        chat_history.append({
            "type": "ai",
            "message": ai_reply
        })

    answered_questions = max(question_index - 1, 0)

    progress = min(
        int((answered_questions / len(questions)) * 100),
        100
    )

    
    return render_template(
        "interview.html",
        chat_history=chat_history,
        score=score,
        progress=progress
    )


@app.route("/result")
def result():

    global score

    if score >= 30:
        performance = "Excellent ⭐"

    elif score >= 20:
        performance = "Good 👍"

    else:
        performance = "Needs Improvement 📚"

    save_result(
    current_category,
    score,
    performance
    )

    return render_template(
        "result.html",
        score=score,
        performance=performance,
        category=current_category
    )

@app.route("/history")
def history():
    pass


if __name__ == "__main__":
    app.run(debug=True)