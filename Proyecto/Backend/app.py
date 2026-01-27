# backend/app.py

from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="../Frontend")

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # Ejecuta el servidor en modo desarrollo
    app.run(debug=True)
