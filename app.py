


from flask import Flask, render_template, request

app = Flask(__name__)

# chat history
chat_history = []

# Python questions
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

# trackers
question_index = 0
score = 0


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/interview/<category>", methods=["GET", "POST"])
def interview(category):
    if category == "python":

        questions = python_questions

    elif category == "sql":

        questions = sql_questions

    else:

        questions = hr_questions

    global question_index
    global score

    # first AI question
    if len(chat_history) == 0:

        chat_history.append({
            "type": "ai",
            "message": questions[question_index]
        })

        question_index += 1

    if request.method == "POST":

        user_answer = request.form["answer"]

        # save user message
        chat_history.append({
            "type": "user",
            "message": user_answer
        })

        # scoring
        if len(user_answer) < 20:

            ai_reply = "Your answer is too short. Try explaining more."

        else:

            score += 10

            ai_reply = f"Good answer! 🎉\nCurrent Score: {score}"

        # next question
        if question_index < len(questions):

            ai_reply += f"\n\nNext Question:\n{questions[question_index]}"

            question_index += 1

        else:

            ai_reply += "\n\nInterview Completed! 🎉"

        # save AI reply
        chat_history.append({
            "type": "ai",
            "message": ai_reply
        })

    return render_template(
        "interview.html",
        chat_history=chat_history,
        score=score
    )


if __name__ == "__main__":
    app.run(debug=True)