import json
import os
from models.task import Task

# Archivo donde se guardarán las tareas
TASKS_FILE = "tasks.json"

def _cargar_tareas():
    """Carga las tareas desde el archivo JSON"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            datos = json.load(f)
            return [Task(t['id'], t['titulo'], t['estado']) for t in datos]
    else:
        # Datos iniciales si el archivo no existe
        return [
            Task(1, "Aprender Flask", False),
            Task(2, "Crear API REST", False),
            Task(3, "Conectar frontend", True)
        ]

def _guardar_tareas(tareas):
    """Guarda las tareas en el archivo JSON"""
    datos = [t.to_dict() for t in tareas]
    with open(TASKS_FILE, 'w') as f:
        json.dump(datos, f, indent=2)

# Cargar tareas al inicio
_tasks = _cargar_tareas()
_next_id = max([t.id for t in _tasks]) + 1 if _tasks else 1

def get_tasks():
    return _tasks

def add_task(titulo):
    global _next_id, _tasks
    nueva_tarea = Task(_next_id, titulo, False)
    _next_id += 1
    _tasks.append(nueva_tarea)
    _guardar_tareas(_tasks)  # ← GUARDA en archivo
    return nueva_tarea

def get_task_by_id(task_id):
    for task in _tasks:
        if task.id == task_id:
            return task
    return None