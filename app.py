from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os

# load env file
load_dotenv()

app = Flask(__name__)

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# chat history
chat_history = []

# question list
questions = [

    "What is Python?",

    "Explain OOP concepts.",

    "What is Machine Learning?",

    "What is SQL?",

    "What are your strengths?"

]

# question tracker
question_index = 0


@app.route("/")
def home():

    return render_template("dashboard.html")


@app.route("/interview", methods=["GET", "POST"])
def interview():

    global question_index

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

        # short answer check
        if len(user_answer) < 10:

            ai_reply = "Your answer is too short. Try explaining more."

        else:

            prompt = f"""
            You are an AI interviewer.

            Check the user's answer.
            Give feedback.
            Then ask the next interview question.

            User Answer:
            {user_answer}

            Next Question:
            {questions[question_index]}
            """

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            ai_reply = response.text

        # save AI reply
        chat_history.append({
            "type": "ai",
            "message": ai_reply
        })

        # next question
        question_index += 1

        # restart question list
        if question_index >= len(questions):

            question_index = 0

    return render_template(
        "interview.html",
        chat_history=chat_history
    )


if __name__ == "__main__":
    app.run(debug=True)