from flask import Flask, render_template, jsonify, request, redirect, session
from models.task import Task
from models.user import User
from data.task_data import get_tasks, add_task, update_task, delete_task, get_task_by_id
from data.user_data import get_users, authenticate_user, get_user_by_email

app = Flask(__name__, static_folder="../Frontend", template_folder="../Frontend")
app.secret_key = 'demo_key_123'  # Clave secreta para sesiones (cambia en producción)

# Ruta de login
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# API de login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    email = data.get("email")
    password = data.get("password")
    
    # Autenticar usuario
    user = authenticate_user(email, password)
    
    if user:
        # Guardar en sesión
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.nombre
        session['user_role'] = user.rol
        session['logged_in'] = True
        
        return jsonify({
            "success": True,
            "message": "Login exitoso",
            "user": {
                "id": user.id,
                "nombre": user.nombre,
                "email": user.email,
                "rol": user.rol
            }
        })
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

# Ruta de logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Middleware para verificar autenticación
@app.before_request
def check_auth():
    # Rutas que no requieren autenticación
    public_routes = ['login_page', 'login', 'static']
    
    if request.endpoint in public_routes:
        return
    
    # Verificar si está autenticado
    if not session.get('logged_in'):
        return redirect('/login')

# Ruta principal - ahora requiere login
@app.route("/")
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    
    # Pasar información del usuario al template
    user_info = {
        'id': session.get('user_id'),
        'nombre': session.get('user_name'),
        'email': session.get('user_email'),
        'rol': session.get('user_role')
    }
    
    return render_template("index.html", user=user_info)

# Ruta para obtener información del usuario actual
@app.route("/api/current-user")
def get_current_user():
    if not session.get('logged_in'):
        return jsonify({"error": "No autenticado"}), 401
    
    user_id = session.get('user_id')
    # Aquí podrías buscar el usuario completo en la base de datos
    user_info = {
        'id': session.get('user_id'),
        'nombre': session.get('user_name'),
        'email': session.get('user_email'),
        'rol': session.get('user_role')
    }
    
    return jsonify(user_info)

# Ruta para cambiar contraseña
@app.route("/api/change-password", methods=["POST"])
def change_password():
    if not session.get('logged_in'):
        return jsonify({"error": "No autenticado"}), 401
    
    data = request.get_json()
    if not data or "current_password" not in data or "new_password" not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    # En una implementación real, verificarías la contraseña actual
    # y actualizarías en la base de datos
    
    return jsonify({"success": True, "message": "Contraseña actualizada"})

# GET /tasks → devuelve todas las tareas ordenadas por tiempo
@app.route("/tasks", methods=["GET"])
def tasks_get():
    try:
        tasks = get_tasks()
        # Convertir a formato JSON
        tasks_data = [task.to_dict() for task in tasks]
        return jsonify(tasks_data)
    except Exception as e:
        print(f"Error en GET /tasks: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# GET /tasks/<id> → devuelve una tarea específica
@app.route("/tasks/<int:task_id>", methods=["GET"])
def task_get(task_id):
    try:
        task = get_task_by_id(task_id)
        if task:
            return jsonify(task.to_dict())
        else:
            return jsonify({"error": "Tarea no encontrada"}), 404
    except Exception as e:
        print(f"Error en GET /tasks/{task_id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# POST /tasks → crea una nueva tarea
@app.route("/tasks", methods=["POST"])
def tasks_post():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data or "titulo" not in data:
            return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400
        
        titulo = data.get("titulo", "").strip()
        if not titulo:
            return jsonify({"error": "El título no puede estar vacío"}), 400
        
        # Campos con valores por defecto
        puntos = data.get("puntos", 1)
        try:
            puntos = int(puntos)
            if puntos < 1:
                puntos = 1
            elif puntos > 10:
                puntos = 10
        except (ValueError, TypeError):
            puntos = 1
        
        asignado_a = data.get("asignado_a")
        if asignado_a:
            asignado_a = asignado_a.strip()
            if asignado_a == "":
                asignado_a = None
        
        estado = data.get("estado", "TODO")
        # Validar estado
        estados_validos = ["TODO", "IN_PROGRESS", "DONE"]
        if estado not in estados_validos:
            estado = "TODO"
        
        estimacion_minutos = data.get("estimacion_minutos", 60)
        try:
            estimacion_minutos = int(estimacion_minutos)
            if estimacion_minutos < 5:
                estimacion_minutos = 5
            elif estimacion_minutos > 480:
                estimacion_minutos = 480
        except (ValueError, TypeError):
            estimacion_minutos = 60
        
        # Crear la tarea
        nueva_tarea = add_task(
            titulo=titulo,
            puntos=puntos,
            asignado_a=asignado_a,
            estado=estado,
            estimacion_minutos=estimacion_minutos
        )
        
        return jsonify(nueva_tarea.to_dict()), 201
        
    except Exception as e:
        print(f"Error en POST /tasks: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# PUT /tasks/<id> → actualiza una tarea (para cambiar estado o editar)
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def task_update(task_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se enviaron datos para actualizar"}), 400
        
        # Validar que la tarea existe
        task = get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Preparar datos para actualización
        update_data = {}
        
        # Validar y procesar cada campo
        if 'titulo' in data:
            titulo = data.get("titulo", "").strip()
            if titulo:
                update_data['titulo'] = titulo
            else:
                return jsonify({"error": "El título no puede estar vacío"}), 400
        
        if 'estado' in data:
            estado = data.get("estado")
            estados_validos = ["TODO", "IN_PROGRESS", "DONE"]
            if estado in estados_validos:
                update_data['estado'] = estado
            else:
                return jsonify({"error": "Estado inválido"}), 400
        
        if 'puntos' in data:
            try:
                puntos = int(data.get("puntos"))
                if 1 <= puntos <= 10:
                    update_data['puntos'] = puntos
                else:
                    return jsonify({"error": "Los puntos deben estar entre 1 y 10"}), 400
            except (ValueError, TypeError):
                return jsonify({"error": "Los puntos deben ser un número válido"}), 400
        
        if 'asignado_a' in data:
            asignado_a = data.get("asignado_a")
            if asignado_a is None:
                update_data['asignado_a'] = None
            else:
                asignado_a = str(asignado_a).strip()
                update_data['asignado_a'] = asignado_a if asignado_a else None
        
        if 'estimacion_minutos' in data:
            try:
                estimacion = int(data.get("estimacion_minutos"))
                if 5 <= estimacion <= 480:
                    update_data['estimacion_minutos'] = estimacion
                else:
                    return jsonify({"error": "La estimación debe estar entre 5 y 480 minutos"}), 400
            except (ValueError, TypeError):
                return jsonify({"error": "La estimación debe ser un número válido"}), 400
        
        # Si no hay datos válidos para actualizar
        if not update_data:
            return jsonify({"error": "No se proporcionaron datos válidos para actualizar"}), 400
        
        # Actualizar la tarea
        tarea_actualizada = update_task(task_id, update_data)
        
        if tarea_actualizada:
            return jsonify(tarea_actualizada.to_dict())
        else:
            return jsonify({"error": "Error al actualizar la tarea"}), 500
            
    except Exception as e:
        print(f"Error en PUT /tasks/{task_id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# DELETE /tasks/<id> → elimina una tarea
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def task_delete(task_id):
    try:
        # Verificar que la tarea existe
        task = get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Eliminar la tarea
        eliminada = delete_task(task_id)
        
        if eliminada:
            return jsonify({
                "mensaje": f"Tarea '{task.titulo}' eliminada correctamente",
                "id": task_id
            })
        else:
            return jsonify({"error": "Error al eliminar la tarea"}), 500
            
    except Exception as e:
        print(f"Error en DELETE /tasks/{task_id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Ruta para obtener estadísticas
@app.route("/stats", methods=["GET"])
def get_stats():
    try:
        tasks = get_tasks()
        
        # Estadísticas por estado
        todos = [t for t in tasks if t.estado == "TODO"]
        in_progress = [t for t in tasks if t.estado == "IN_PROGRESS"]
        dones = [t for t in tasks if t.estado == "DONE"]
        
        # Tiempo total por estado
        tiempo_todo = sum(t.estimacion_minutos for t in todos)
        tiempo_progress = sum(t.estimacion_minutos for t in in_progress)
        tiempo_done = sum(t.estimacion_minutos for t in dones)
        tiempo_total = tiempo_todo + tiempo_progress + tiempo_done
        
        # Tareas asignadas vs no asignadas
        asignadas = [t for t in tasks if t.asignado_a]
        no_asignadas = [t for t in tasks if not t.asignado_a]
        
        stats = {
            "total_tareas": len(tasks),
            "todo": len(todos),
            "in_progress": len(in_progress),
            "done": len(dones),
            "tiempo_total": tiempo_total,
            "tiempo_todo": tiempo_todo,
            "tiempo_progress": tiempo_progress,
            "tiempo_done": tiempo_done,
            "asignadas": len(asignadas),
            "no_asignadas": len(no_asignadas),
            "promedio_puntos": sum(t.puntos for t in tasks) / len(tasks) if tasks else 0,
            "promedio_tiempo": sum(t.estimacion_minutos for t in tasks) / len(tasks) if tasks else 0
        }
        
        return jsonify(stats)
        
    except Exception as e:
        print(f"Error en GET /stats: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Ruta para buscar tareas
@app.route("/tasks/search", methods=["GET"])
def search_tasks():
    try:
        query = request.args.get('q', '').strip().lower()
        if not query:
            return jsonify([])
        
        tasks = get_tasks()
        results = []
        
        for task in tasks:
            # Buscar en título
            if query in task.titulo.lower():
                results.append(task.to_dict())
                continue
            
            # Buscar en asignado
            if task.asignado_a and query in task.asignado_a.lower():
                results.append(task.to_dict())
                continue
            
            # Buscar en estado
            if query in task.estado.lower():
                results.append(task.to_dict())
        
        return jsonify(results)
        
    except Exception as e:
        print(f"Error en GET /tasks/search: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Ruta para obtener tareas por responsable
@app.route("/tasks/responsable/<string:responsable>", methods=["GET"])
def tasks_by_responsable(responsable):
    try:
        tasks = get_tasks()
        responsable_tasks = [t.to_dict() for t in tasks if t.asignado_a and t.asignado_a.lower() == responsable.lower()]
        
        return jsonify(responsable_tasks)
        
    except Exception as e:
        print(f"Error en GET /tasks/responsable/{responsable}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Ruta para obtener todos los usuarios (solo para usuarios autenticados)
@app.route("/api/users", methods=["GET"])
def get_all_users():
    if not session.get('logged_in'):
        return jsonify({"error": "No autenticado"}), 401
    
    try:
        users = get_users()
        users_data = [user.to_dict() for user in users]
        return jsonify(users_data)
    except Exception as e:
        print(f"Error en GET /api/users: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Middleware CORS manual para peticiones del mismo origen
@app.after_request
def add_cors_headers(response):
    # Permitir peticiones desde el mismo origen (mismo puerto y dominio)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Para desarrollo
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Manejar preflight OPTIONS requests
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    response = jsonify()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Manejar errores 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

# Manejar errores 405
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Método no permitido"}), 405

# Manejar errores 500
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

# Middleware para logging
@app.before_request
def before_request():
    if request.endpoint and request.endpoint != 'static':
        print(f"[{request.method}] {request.path}")

@app.after_request
def after_request_logging(response):
    if request.endpoint and request.endpoint != 'static':
        print(f"[{response.status_code}] {request.path}")
    return response

if __name__ == "__main__":
    print("=== Iniciando Gestor de Tareas ===")
    print("Servidor corriendo en: http://localhost:5000")
    print("Página de login: http://localhost:5000/login")
    print("Credenciales de prueba:")
    print("  - ana@empresa.com / ana123")
    print("  - carlos@empresa.com / carlos123")
    print("  - luis@empresa.com / luis123")
    print("Presiona Ctrl+C para detener")
    print("=" * 40)
    
    # Iniciar el servidor
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0',  # Accesible desde cualquier IP en la red
        threaded=True  # Manejar múltiples peticiones simultáneamente
    )