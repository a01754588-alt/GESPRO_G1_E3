from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "<h1>Acerca de</h1><p>Mi primera web con Flask</p>"

if __name__ == "__main__":
    app.run(debug=True)