from flask import Blueprint, render_template, request
from models.generator import generate

main_bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static"
)

def to_int(value, default):
    try:
        return int(value)
    except:
        return default

def to_float(value, default):
    try:
        return float(value)
    except:
        return default


@main_bp.route("/", methods=["GET", "POST"])
def index():
    output = None

    if request.method == "POST":
        prompt = request.form.get("prompt")
        method = request.form.get("method")

        params = {
            "max_length": to_int(request.form.get("max_length"), 100),
            "num_return_sequences": to_int(request.form.get("num_return_sequences"), 1),
            "top_k": to_int(request.form.get("top_k"), 50),
            "top_p": to_float(request.form.get("top_p"), 0.9),
            "temperature": to_float(request.form.get("temperature"), 0.8),
            "num_beams": to_int(request.form.get("num_beams"), 5),
        }

        output = generate(prompt, method=method, **params)

    return render_template("index.html", output=output)
