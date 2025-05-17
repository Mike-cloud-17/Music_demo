from flask import Flask, render_template, request, redirect, url_for, jsonify
from logic import RealRecommender

app = Flask(
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

rec = RealRecommender()
user_ctx = {}

# ─── routes ─────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_ctx["city"]   = request.form.get("city")
        user_ctx["gender"] = request.form.get("gender")
        return redirect(url_for("player"))
    return render_template("index.html")

@app.route("/player")
def player():
    return render_template("player.html", item=rec._cur())

# ─── AJAX API ───────────────────────────────────────────
@app.route("/api/next", methods=["POST"])
def api_next():
    return jsonify(rec.next_track())

@app.route("/api/genre", methods=["POST"])
def api_genre():
    genre = request.json.get("genre", "Pop")
    return jsonify(rec.by_genre(genre))

@app.route("/api/like", methods=["POST"])
def api_like():
    rec.like();   return ("", 204)

@app.route("/api/dislike", methods=["POST"])
def api_dislike():
    rec.dislike(); return ("", 204)

# ─── run ────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
