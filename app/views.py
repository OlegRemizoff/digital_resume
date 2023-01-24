from app import app


@app.route("/")
def index():
    return "<h1>Flask</h1>"