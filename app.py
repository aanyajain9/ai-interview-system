from db import save_result, get_history
from flask import Flask, render_template, request , redirect
import os
from PyPDF2 import PdfReader
from db import save_result, get_history, get_stats
import ollama


app = Flask(__name__)

chat_history = []

current_category = ""


question_count = 0

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

current_question = ""
score = 0


@app.route("/")
def home():
    stats = get_stats()

    total_interviews = stats[0]
    highest_score = stats[1] if stats[1] else 0
    average_score = round(stats[2], 2) if stats[2] else 0

    global chat_history
    global question_index
    global score

    chat_history = []
    question_index = 0
    score = 0
    total, highest, average = get_stats()

    return render_template(
        "dashboard.html",
        total=total,
        highest=highest,
        average=round(average or 0, 2)
)



@app.route("/interview/<category>", methods=["GET", "POST"])
def interview(category):

    global current_category
    current_category = category

    global question_index
    global score


    if len(chat_history) == 0:

        ai_question = generate_question(category)

        chat_history.append({
            "type": "ai",
            "message": ai_question
        })

        global current_question
        current_question = ai_question

    if request.method == "POST":

        user_answer = request.form["answer"]

        chat_history.append({
            "type": "user",
            "message": user_answer
        })

        ai_reply = evaluate_answer(
            current_question,
            user_answer
)
        
        next_question = generate_question(category)

        current_question = next_question

        ai_reply += f"\n\nNext Question:\n{next_question}"

        chat_history.append({
            "type": "ai",
            "message": ai_reply
        })

    answered_questions = max(question_index - 1, 0)

    progress = min(
    int((question_count / 5) * 100),
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
)

@app.route("/history")
def history():

    records = get_history()

    return render_template(
        "history.html",
        records=records
    )


@app.route("/test-ai")
def test_ai():

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": "Ask one Python interview question."
            }
        ]
    )

    return response["message"]["content"]


def generate_question(topic):

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": f"""
                Ask ONLY ONE SHORT {topic} interview question.

                Rules:
                - Maximum 15 words
                - No explanation
                - No answer
                - No code
                - No examples

                Example:
                What is OOP?
                """
            }
        ]
    )

    return response["message"]["content"]



def evaluate_answer(question, answer):

    global score

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": f"""
                Interview Question:
                {question}

                Candidate Answer:
                {answer}

                Evaluate the answer.

                Give:
                Score: x/10
                Feedback:
                """
            }
        ]
    )

    score += 10

    return response["message"]["content"]



@app.route("/resume")
def resume():
    return render_template("resume.html")



@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]

    filepath = os.path.join(
        "uploads",
        file.filename
    )

    file.save(filepath)

    pdf = PdfReader(filepath)

    text = ""

    for page in pdf.pages:

        text += page.extract_text()

    skills_list = [
        "Python",
        "SQL",
        "Machine Learning",
        "Data Science",
        "Java",
        "Flask",
        "Pandas",
        "NumPy",
        "MySQL",
        "HTML",
        "CSS",
        "JavaScript"
    ]
    detected_skills = []

    for skill in skills_list:

        if skill.lower() in text.lower():

            detected_skills.append(skill)

    total_skills = len(detected_skills)

    recommended_category = "HR"

    if "Python" in detected_skills:

        recommended_category = "Python"

    elif "SQL" in detected_skills:

        recommended_category = "SQL"

    elif "Machine Learning" in detected_skills:

        recommended_category = "Machine Learning"

    return render_template(
        "resumeresult.html",
        resume_text=text,
        skills=detected_skills,
        recommended_category=recommended_category,
        total_skills=total_skills
    )




if __name__ == "__main__":
    app.run(debug=True)