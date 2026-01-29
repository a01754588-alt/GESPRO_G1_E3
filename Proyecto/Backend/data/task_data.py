import json
import os
from models.task import Task

# Archivo donde se guardarán las tareas
TASKS_FILE = "tasks.json"

def _cargar_tareas():
    """Carga las tareas desde el archivo JSON"""
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                datos = json.load(f)
                tareas = []
                for t in datos:
                    # Manejar compatibilidad con diferentes formatos
                    if isinstance(t.get('estado'), bool):
                        estado = "DONE" if t['estado'] else "TODO"
                    else:
                        estado = t.get('estado', "TODO")
                    
                    puntos = t.get('puntos', 1)
                    # Asegurar que puntos sea un número entre 1 y 10
                    try:
                        puntos = int(puntos)
                        if puntos < 1:
                            puntos = 1
                        elif puntos > 10:
                            puntos = 10
                    except (ValueError, TypeError):
                        puntos = 1
                    
                    tareas.append(Task(
                        t['id'],
                        t['titulo'],
                        estado,
                        puntos,
                        t.get('asignado_a')
                    ))
                return tareas
    except Exception as e:
        print(f"Error cargando tareas: {e}")
    
    # Datos iniciales
    return [
        Task(1, "Crear backend mínimo operativo", "TODO", 2, "Núvo"),
        Task(2, "Crear frontend mínimo operativo", "TODO", 2, "Daniel"),
        Task(3, "Conectar frontend con backend", "TODO", 3, None)
    ]

def _guardar_tareas(tareas):
    """Guarda las tareas en el archivo JSON"""
    try:
        datos = [t.to_dict() for t in tareas]
        with open(TASKS_FILE, 'w') as f:
            json.dump(datos, f, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando tareas: {e}")
        return False

# Cargar tareas al inicio
_tasks = _cargar_tareas()
_next_id = max([t.id for t in _tasks]) + 1 if _tasks else 1

def get_tasks():
    return _tasks

def add_task(titulo, puntos=1, asignado_a=None, estado="TODO"):
    global _next_id, _tasks
    nueva_tarea = Task(_next_id, titulo, estado, puntos, asignado_a)
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
                try:
                    puntos = int(nuevos_datos['puntos'])
                    if 1 <= puntos <= 10:
                        task.puntos = puntos
                except (ValueError, TypeError):
                    pass  # Mantener el valor actual si es inválido
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