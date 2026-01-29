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
            # Asegurar compatibilidad con tareas antiguas
            tareas = []
            for t in datos:
                # Si es tarea antigua (solo booleano en estado)
                if isinstance(t['estado'], bool):
                    estado = "DONE" if t['estado'] else "TODO"
                else:
                    estado = t.get('estado', "TODO")
                
                tareas.append(Task(
                    t['id'],
                    t['titulo'],
                    estado,
                    t.get('puntos', 0),
                    t.get('asignado_a')
                ))
            return tareas
    else:
        # Datos iniciales con los nuevos campos
        return [
            Task(1, "Crear backend mínimo operativo", "TODO", 2, "Núvo"),
            Task(2, "Crear frontend mínimo operativo", "TODO", 2, "Daniel"),
            Task(3, "Conectar frontend con backend", "TODO", 3)
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

def add_task(titulo, puntos=0, asignado_a=None):
    global _next_id, _tasks
    nueva_tarea = Task(_next_id, titulo, "TODO", puntos, asignado_a)
    _next_id += 1
    _tasks.append(nueva_tarea)
    _guardar_tareas(_tasks)
    return nueva_tarea

def update_task(task_id, nuevos_datos):
    global _tasks
    for i, task in enumerate(_tasks):
        if task.id == task_id:
            # Actualizar campos permitidos
            if 'titulo' in nuevos_datos:
                task.titulo = nuevos_datos['titulo']
            if 'estado' in nuevos_datos:
                task.estado = nuevos_datos['estado']
            if 'puntos' in nuevos_datos:
                task.puntos = nuevos_datos['puntos']
            if 'asignado_a' in nuevos_datos:
                task.asignado_a = nuevos_datos['asignado_a']
            
            _guardar_tareas(_tasks)
            return task
    return None

def get_task_by_id(task_id):
    for task in _tasks:
        if task.id == task_id:
            return task
    return None
def delete_task(task_id):
    global _tasks
    tarea_encontrada = None
    
    # Buscar y eliminar la tarea
    for i, task in enumerate(_tasks):
        if task.id == task_id:
            tarea_encontrada = _tasks.pop(i)
            break
    
    if tarea_encontrada:
        _guardar_tareas(_tasks)  # Guardar cambios
        return True
    return False