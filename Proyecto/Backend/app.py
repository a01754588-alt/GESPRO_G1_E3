# backend/app.py
from models.task import Task 
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__, template_folder="../Frontend")

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    # Lista de tareas simuladas usando nuestra clase
    tasks = [
        Task(1, "Comprar leche", "pendiente"),
        Task(2, "Hacer ejercicio", "completada"),
        Task(3, "Leer libro", "pendiente")
    ]
    # Convertimos cada objeto a diccionario
    return jsonify([task.to_dict() for task in tasks])

if __name__ == "__main__":
    # Ejecuta el servidor en modo desarrollo
    app.run(debug=True)
