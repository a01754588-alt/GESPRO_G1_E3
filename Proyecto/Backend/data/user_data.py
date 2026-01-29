import json
import os
from models.user import User

# Archivo donde se guardarán los usuarios
USERS_FILE = "users.json"

# Roles disponibles en el sistema
ROLES_DISPONIBLES = [
    "Product Owner (PO)",
    "Agile Leader / Scrum Master",
    "Desarrollador Backend",
    "Desarrollador Frontend",
    "Desarrollador Full Stack",
    "Diseñador UX/UI",
    "QA / Tester",
    "DevOps Engineer",
    "Analista de Negocio",
    "Arquitecto de Software",
    "Líder Técnico",
    "Invitado"
]

def _cargar_usuarios():
    """Carga los usuarios desde el archivo JSON"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                datos = json.load(f)
                usuarios = []
                for u in datos:
                    usuario = User(
                        u['id'],
                        u['nombre'],
                        u['email'],
                        u['rol'],
                        u.get('password', '123456'),  # Contraseña por defecto
                        u.get('disponibilidad', 100),
                        u.get('activo', True)
                    )
                    # Cargar tareas asignadas si existen
                    if 'tareas_asignadas' in u:
                        usuario.tareas_asignadas = u['tareas_asignadas']
                    usuarios.append(usuario)
                return usuarios
    except Exception as e:
        print(f"Error cargando usuarios: {e}")
    
    # Datos iniciales de ejemplo con contraseñas
    return [
        User(1, "Ana García", "ana@empresa.com", "Product Owner (PO)", "ana123", 100),
        User(2, "Carlos Rodríguez", "carlos@empresa.com", "Agile Leader / Scrum Master", "carlos123", 100),
        User(3, "Luis Fernández", "luis@empresa.com", "Desarrollador Backend", "luis123", 80),
        User(4, "María López", "maria@empresa.com", "Desarrollador Frontend", "maria123", 90),
        User(5, "Pedro Martínez", "pedro@empresa.com", "Desarrollador Full Stack", "pedro123", 70),
        User(6, "Laura Sánchez", "laura@empresa.com", "Diseñador UX/UI", "laura123", 60),
        User(7, "Jorge Ramírez", "jorge@empresa.com", "QA / Tester", "jorge123", 85),
        User(8, "Sofía Castro", "sofia@empresa.com", "DevOps Engineer", "sofia123", 75),
        User(9, "David Torres", "david@empresa.com", "Invitado", "david123", 0)
    ]

def _guardar_usuarios(usuarios):
    """Guarda los usuarios en el archivo JSON"""
    try:
        datos = [u.to_dict() for u in usuarios]
        with open(USERS_FILE, 'w') as f:
            json.dump(datos, f, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando usuarios: {e}")
        return False

# Cargar usuarios al inicio
_users = _cargar_usuarios()
_next_user_id = max([u.id for u in _users]) + 1 if _users else 1

def get_users():
    """Obtiene todos los usuarios"""
    return _users

def get_user_by_id(user_id):
    """Obtiene un usuario por su ID"""
    for user in _users:
        if user.id == user_id:
            return user
    return None

def get_user_by_email(email):
    """Obtiene un usuario por su email"""
    for user in _users:
        if user.email == email:
            return user
    return None

def authenticate_user(email, password):
    """Autentica un usuario con email y contraseña"""
    user = get_user_by_email(email)
    if user and user.activo and user.verificar_password(password):
        return user
    return None

def get_user_by_name(name):
    """Obtiene un usuario por su nombre (búsqueda parcial)"""
    name_lower = name.lower()
    for user in _users:
        if name_lower in user.nombre.lower():
            return user
    return None

def get_users_by_role(rol):
    """Obtiene usuarios por rol"""
    return [u for u in _users if u.rol == rol]

def get_available_users():
    """Obtiene usuarios con disponibilidad > 0"""
    return [u for u in _users if u.disponibilidad > 0]

def get_roles():
    """Obtiene la lista de roles disponibles"""
    return ROLES_DISPONIBLES

def add_user(nombre, email, rol, disponibilidad=100):
    """Agrega un nuevo usuario"""
    global _next_user_id, _users
    
    # Validar rol
    if rol not in ROLES_DISPONIBLES:
        raise ValueError(f"Rol inválido. Roles disponibles: {', '.join(ROLES_DISPONIBLES)}")
    
    # Validar disponibilidad
    if disponibilidad < 0 or disponibilidad > 100:
        raise ValueError("La disponibilidad debe estar entre 0 y 100")
    
    # Crear nuevo usuario
    nuevo_usuario = User(_next_user_id, nombre, email, rol, disponibilidad)
    _next_user_id += 1
    _users.append(nuevo_usuario)
    _guardar_usuarios(_users)
    
    return nuevo_usuario

def update_user(user_id, nuevos_datos):
    """Actualiza un usuario existente"""
    global _users
    
    for i, user in enumerate(_users):
        if user.id == user_id:
            # Actualizar campos permitidos
            if 'nombre' in nuevos_datos:
                user.nombre = nuevos_datos['nombre']
            if 'email' in nuevos_datos:
                user.email = nuevos_datos['email']
            if 'rol' in nuevos_datos:
                if nuevos_datos['rol'] not in ROLES_DISPONIBLES:
                    raise ValueError(f"Rol inválido. Roles disponibles: {', '.join(ROLES_DISPONIBLES)}")
                user.rol = nuevos_datos['rol']
            if 'disponibilidad' in nuevos_datos:
                disponibilidad = nuevos_datos['disponibilidad']
                if disponibilidad < 0 or disponibilidad > 100:
                    raise ValueError("La disponibilidad debe estar entre 0 y 100")
                user.disponibilidad = disponibilidad
            
            _guardar_usuarios(_users)
            return user
    
    return None

def delete_user(user_id):
    """Elimina un usuario"""
    global _users
    
    usuario_encontrado = None
    
    # Buscar y eliminar el usuario
    for i, user in enumerate(_users):
        if user.id == user_id:
            usuario_encontrado = _users.pop(i)
            break
    
    if usuario_encontrado:
        _guardar_usuarios(_users)
        return True
    return False

def assign_task_to_user(user_id, task_id):
    """Asigna una tarea a un usuario"""
    user = get_user_by_id(user_id)
    if user:
        user.asignar_tarea(task_id)
        _guardar_usuarios(_users)
        return True
    return False

def remove_task_from_user(user_id, task_id):
    """Remueve una tarea de un usuario"""
    user = get_user_by_id(user_id)
    if user:
        user.remover_tarea(task_id)
        _guardar_usuarios(_users)
        return True
    return False

def get_users_with_tasks():
    """Obtiene usuarios con sus tareas asignadas"""
    from data.task_data import get_tasks
    tareas = get_tasks()
    
    usuarios_info = []
    for user in _users:
        tareas_usuario = []
        for task_id in user.tareas_asignadas:
            tarea = next((t for t in tareas if t.id == task_id), None)
            if tarea:
                tareas_usuario.append(tarea.to_dict())
        
        usuario_info = user.to_dict()
        usuario_info['tareas_detalle'] = tareas_usuario
        usuario_info['carga_actual'] = user.carga_trabajo_actual(tareas)
        usuario_info['disponibilidad_real'] = user.disponibilidad_real(tareas)
        
        usuarios_info.append(usuario_info)
    
    return usuarios_info

def get_user_stats():
    """Obtiene estadísticas de usuarios"""
    from data.task_data import get_tasks
    tareas = get_tasks()
    
    stats = {
        'total_usuarios': len(_users),
        'usuarios_activos': len([u for u in _users if u.disponibilidad > 0]),
        'usuarios_por_rol': {},
        'carga_total': 0,
        'disponibilidad_total': 0,
        'usuarios_sobrecargados': []
    }
    
    # Usuarios por rol
    for user in _users:
        rol = user.rol
        if rol in stats['usuarios_por_rol']:
            stats['usuarios_por_rol'][rol] += 1
        else:
            stats['usuarios_por_rol'][rol] = 1
    
    # Carga y disponibilidad
    for user in _users:
        carga = user.carga_trabajo_actual(tareas)
        stats['carga_total'] += carga
        stats['disponibilidad_total'] += user.disponibilidad_real(tareas)
        
        # Verificar sobrecarga (más del 80% de disponibilidad usada)
        if user.disponibilidad > 0:
            porcentaje_uso = (carga * 10) / user.disponibilidad * 100
            if porcentaje_uso > 80:
                stats['usuarios_sobrecargados'].append({
                    'id': user.id,
                    'nombre': user.nombre,
                    'rol': user.rol,
                    'porcentaje_uso': round(porcentaje_uso, 1)
                })
    
    stats['carga_promedio'] = stats['carga_total'] / len(_users) if _users else 0
    stats['disponibilidad_promedio'] = stats['disponibilidad_total'] / len(_users) if _users else 0
    
    return stats

def get_suggested_users_for_task(puntos_tarea, estado=None, rol_preferido=None):
    """Sugiere usuarios adecuados para una tarea"""
    from data.task_data import get_tasks
    tareas = get_tasks()
    
    usuarios_sugeridos = []
    
    for user in _users:
        # Filtrar por rol si se especifica
        if rol_preferido and user.rol != rol_preferido:
            continue
        
        # Verificar si puede tomar la tarea
        if user.puede_tomar_tarea(puntos_tarea, tareas):
            info_usuario = user.to_dict()
            info_usuario['disponibilidad_real'] = user.disponibilidad_real(tareas)
            info_usuario['carga_actual'] = user.carga_trabajo_actual(tareas)
            
            # Calcular prioridad (mayor disponibilidad = mayor prioridad)
            prioridad = user.disponibilidad_real(tareas)
            
            usuarios_sugeridos.append({
                'usuario': info_usuario,
                'prioridad': prioridad
            })
    
    # Ordenar por prioridad (mayor a menor)
    usuarios_sugeridos.sort(key=lambda x: x['prioridad'], reverse=True)
    
    return [item['usuario'] for item in usuarios_sugeridos]