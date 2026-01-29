class User:
    def __init__(self, id, nombre, email, rol, password="123456", disponibilidad=100, activo=True):
        """
        Clase para representar un usuario del equipo
        
        Args:
            id (int): Identificador único
            nombre (str): Nombre completo
            email (str): Correo electrónico (será el username)
            rol (str): Rol en el equipo
            password (str): Contraseña (por defecto 123456 para demo)
            disponibilidad (int): Porcentaje de disponibilidad (0-100)
            activo (bool): Si el usuario está activo en el sistema
        """
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.password = password  # Contraseña simple para demo
        self.disponibilidad = disponibilidad
        self.activo = activo
        self.tareas_asignadas = []
    
    def to_dict(self):
        """Convierte el usuario a diccionario para JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "password": self.password,
            "disponibilidad": self.disponibilidad,
            "activo": self.activo,
            "tareas_asignadas": self.tareas_asignadas
        }
    
    def verificar_password(self, password):
        """Verifica si la contraseña es correcta"""
        return self.password == password
    
    def cambiar_password(self, nueva_password):
        """Cambia la contraseña del usuario"""
        self.password = nueva_password
    
    def asignar_tarea(self, task_id):
        """Asigna una tarea al usuario"""
        if task_id not in self.tareas_asignadas:
            self.tareas_asignadas.append(task_id)
    
    def remover_tarea(self, task_id):
        """Remueve una tarea del usuario"""
        if task_id in self.tareas_asignadas:
            self.tareas_asignadas.remove(task_id)
    
    def carga_trabajo_actual(self, tasks_data):
        """Calcula la carga de trabajo actual en puntos"""
        from data.task_data import get_tasks
        tareas = get_tasks()
        
        carga = 0
        for task_id in self.tareas_asignadas:
            tarea = next((t for t in tareas if t.id == task_id), None)
            if tarea and tarea.estado != 'DONE':
                carga += tarea.puntos
        
        return carga
    
    def disponibilidad_real(self, tasks_data):
        """Calcula la disponibilidad real considerando carga actual"""
        carga_actual = self.carga_trabajo_actual(tasks_data)
        # Suponemos que 10 puntos = 100% de disponibilidad
        disponibilidad_real = max(0, self.disponibilidad - (carga_actual * 10))
        return disponibilidad_real
    
    def puede_tomar_tarea(self, puntos_tarea, tasks_data):
        """Verifica si el usuario puede tomar una nueva tarea"""
        disponibilidad_real = self.disponibilidad_real(tasks_data)
        return (puntos_tarea * 10) <= disponibilidad_real