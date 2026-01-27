# backend/data/tasks_data.py
from models.task import Task

# Lista que mantiene las tareas en memoria
tasks = [
    Task(1, "Comprar leche", "pendiente"),
    Task(2, "Hacer ejercicio", "completada"),
    Task(3, "Leer libro", "pendiente")
]

# Función para obtener todas las tareas
def get_tasks():
    return tasks

# Función para agregar una nueva tarea
def add_task(titulo, estado="pendiente"):
    new_id = len(tasks) + 1
    nueva_tarea = Task(new_id, titulo, estado)
    tasks.append(nueva_tarea)
    return nueva_tarea
