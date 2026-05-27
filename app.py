from flask import Flask, render_template, request
import google.generativeai as genai
import os


app = Flask(__name__)
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
model = genai.GenerativeModel(
    "models/gemini-1.5-flash"
)
chat_history = []

# question list
questions = [

    "What is Python?",

    "Explain OOP concepts.",

    "What is Machine Learning?",

    "What is SQL?",

    "What are your strengths?"

]

question_index = 0

@app.route("/")
def home():

    return render_template("dashboard.html")


@app.route("/interview", methods=["GET", "POST"])
def interview():

    global question_index

    if len(chat_history) == 0:
        chat_history.append([{
            "type": "ai",
            "message": questions[question_index]
        }])
        question_index=question_index+1

    if request.method == "POST":

        user_answer = request.form["answer"]

        # user message
        chat_history.append({
            "type": "user",
            "message": user_answer
        })

        # simple answer checking

        if len(user_answer) < 10:

            feedback = "Your answer is too short. Try explaining more."

        else:

            prompt = f"""
            You are an AI interviewer.

            Ask interview questions.
            Check the user's answer.
            Give feedback.
            Then ask next question.

            User Answer:
            {user_answer}
            """

            response = model.generate_content(prompt)
            ai_reply = response.text


        # next question
        next_question = questions[question_index]

        ai_reply = f"{feedback}\n\nNext Question: {next_question}"

        # ai message
        chat_history.append({
            "type": "ai",
            "message": ai_reply
        })

        # next index
        question_index += 1

        # restart questions
        if question_index >= len(questions):
            question_index = 0

    return render_template(
        "interview.html",
        chat_history=chat_history
    )


if __name__ == "__main__":
    app.run(debug=True)