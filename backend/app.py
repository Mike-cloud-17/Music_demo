# backend/app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
from logic import RealRecommender

app = Flask(
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

rec = RealRecommender()
user_ctx = {}  # здесь будем хранить введённые и сгенерированные данные

# ─── routes ─────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    now = datetime.utcnow()
    default_registered_via = request.user_agent.browser or "web-browser"
    default_registration_init_time = now.isoformat()
    default_expiration_date = (now + timedelta(days=30)).isoformat()

    if request.method == "POST":
        # 1) читаем форму
        user_ctx["fullname"]               = request.form["fullname"]
        user_ctx["city"]                   = request.form["city"]
        user_ctx["age"]                    = int(request.form["age"])
        user_ctx["gender"]                 = request.form["gender"]
        # 2) автоматически-заполненные
        user_ctx["registered_via"]         = request.form["registered_via"]
        user_ctx["registration_init_time"] = request.form["registration_init_time"]
        user_ctx["expiration_date"]        = request.form["expiration_date"]
        return redirect(url_for("player"))

    # GET: показываем форму с дефолтами
    return render_template(
        "index.html",
        registered_via=default_registered_via,
        registration_init_time=default_registration_init_time,
        expiration_date=default_expiration_date
    )


@app.route("/player")
def player():
    return render_template("player.html", item=rec._cur())


# ─── AJAX API ───────────────────────────────────────────
@app.route("/api/next", methods=["POST"])
def api_next():
    return jsonify(rec.next_track())


@app.route("/api/genre", methods=["POST"])
def api_genre():
    # сразу следующий трек того же жанра
    return jsonify(rec.by_genre())


@app.route("/api/like", methods=["POST"])
def api_like():
    rec.like()
    return ("", 204)


@app.route("/api/dislike", methods=["POST"])
def api_dislike():
    rec.dislike()
    return ("", 204)


# ─── run ────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
