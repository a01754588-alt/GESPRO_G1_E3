from flask import Flask, render_template, jsonify, request
from models.task import Task
from data.task_data import get_tasks, add_task

app = Flask(__name__, template_folder="../Frontend")

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# GET /tasks → devuelve todas las tareas
@app.route("/tasks", methods=["GET"])
def tasks_get():
    return jsonify([task.to_dict() for task in get_tasks()])

# POST /tasks → crea una nueva tarea
@app.route("/tasks", methods=["POST"])
def tasks_post():
    data = request.get_json()
    
    if not data or "titulo" not in data:
        return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400
    
    nueva_tarea = add_task(data["titulo"])
    return jsonify(nueva_tarea.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)