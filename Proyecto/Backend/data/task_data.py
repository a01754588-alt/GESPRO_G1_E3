from models.task import Task

# Datos iniciales en memoria
_tasks = [
    Task(1, "Aprender Flask", False),
    Task(2, "Crear API REST", False),
    Task(3, "Conectar frontend", True)
]
_next_id = 4

def get_tasks():
    return _tasks

def add_task(titulo):
    global _next_id
    nueva_tarea = Task(_next_id, titulo)
    _next_id += 1
    _tasks.append(nueva_tarea)
    return nueva_tarea

def get_task_by_id(task_id):
    for task in _tasks:
        if task.id == task_id:
            return task
    return None