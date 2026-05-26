from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("dashboard.html")


@app.route("/interview", methods=["GET", "POST"])
def interview():

    user_answer = ""
    ai_reply = ""

    if request.method == "POST":

        user_answer = request.form["answer"]

        # fake AI response
        ai_reply = "Nice answer! Tell me about your strengths."

    return render_template(
        "interview.html",
        user_answer=user_answer,
        ai_reply=ai_reply
    )


if __name__ == "__main__":
    app.run(debug=True)