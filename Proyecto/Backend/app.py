from flask import Flask, render_template, jsonify, request
from models.task import Task
from data.task_data import get_tasks, add_task, update_task, delete_task

app = Flask(__name__, static_folder="../Frontend", template_folder="../Frontend")

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
    
    # Nuevos campos opcionales
    puntos = data.get("puntos", 1)  # Cambié de 0 a 1 por defecto
    asignado_a = data.get("asignado_a")
    estado = data.get("estado", "TODO")  # Estado por defecto
    
    nueva_tarea = add_task(data["titulo"], puntos, asignado_a, estado)
    return jsonify(nueva_tarea.to_dict()), 201

# PUT /tasks/<id> → actualiza una tarea (para cambiar estado)
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def task_update(task_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos para actualizar"}), 400
    
    tarea_actualizada = update_task(task_id, data)
    
    if tarea_actualizada:
        return jsonify(tarea_actualizada.to_dict())
    else:
        return jsonify({"error": "Tarea no encontrada"}), 404

# DELETE /tasks/<id> → elimina una tarea
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def task_delete(task_id):
    eliminada = delete_task(task_id)
    
    if eliminada:
        return jsonify({"mensaje": f"Tarea {task_id} eliminada correctamente"})
    else:
        return jsonify({"error": "Tarea no encontrada"}), 404

# Manejar errores 405
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Método no permitido"}), 405

if __name__ == "__main__":
    app.run(debug=True, port=5000)