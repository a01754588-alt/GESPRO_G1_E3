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
                        u.get('activo', True)
                    )
                    # Cargar tareas asignadas si existen
                    if 'tareas_asignadas' in u:
                        usuario.tareas_asignadas = u['tareas_asignadas']
                    usuarios.append(usuario)
                return usuarios
    except Exception as e:
        print(f"Error cargando usuarios: {e}")
    
    # Datos iniciales de ejemplo con contraseñas (sin disponibilidad)
    return [
        User(1, "Ana García", "ana@empresa.com", "Product Owner (PO)", "ana123"),
        User(2, "Carlos Rodríguez", "carlos@empresa.com", "Agile Leader / Scrum Master", "carlos123"),
        User(3, "Luis Fernández", "luis@empresa.com", "Desarrollador Backend", "luis123"),
        User(4, "María López", "maria@empresa.com", "Desarrollador Frontend", "maria123"),
        User(5, "Pedro Martínez", "pedro@empresa.com", "Desarrollador Full Stack", "pedro123"),
        User(6, "Laura Sánchez", "laura@empresa.com", "Diseñador UX/UI", "laura123"),
        User(7, "Jorge Ramírez", "jorge@empresa.com", "QA / Tester", "jorge123"),
        User(8, "Sofía Castro", "sofia@empresa.com", "DevOps Engineer", "sofia123"),
        User(9, "David Torres", "david@empresa.com", "Invitado", "david123")
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

def get_roles():
    """Obtiene la lista de roles disponibles"""
    return ROLES_DISPONIBLES

def add_user(nombre, email, rol):
    """Agrega un nuevo usuario"""
    global _next_user_id, _users
    
    # Validar rol
    if rol not in ROLES_DISPONIBLES:
        raise ValueError(f"Rol inválido. Roles disponibles: {', '.join(ROLES_DISPONIBLES)}")
    
    # Crear nuevo usuario
    nuevo_usuario = User(_next_user_id, nombre, email, rol)
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
            if 'password' in nuevos_datos:
                user.password = nuevos_datos['password']
            
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

def get_usuarios_asignables():
    """Obtiene usuarios que pueden ser asignados a tareas"""
    return [user for user in _users if user.activo and user.rol != "Invitado"]

def get_user_stats():
    """Obtiene estadísticas de usuarios"""
    stats = {
        'total_usuarios': len(_users),
        'usuarios_activos': len([u for u in _users if u.activo]),
        'usuarios_por_rol': {}
    }
    
    # Usuarios por rol
    for user in _users:
        rol = user.rol
        if rol in stats['usuarios_por_rol']:
            stats['usuarios_por_rol'][rol] += 1
        else:
            stats['usuarios_por_rol'][rol] = 1
    
    return stats