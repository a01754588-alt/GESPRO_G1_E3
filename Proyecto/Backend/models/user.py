class User:
    def __init__(self, id, nombre, email, rol, disponibilidad=100):
        """
        Clase para representar un usuario del equipo
        
        Args:
            id (int): Identificador único
            nombre (str): Nombre completo
            email (str): Correo electrónico
            rol (str): Rol en el equipo (PO, Agile Leader, Desarrollador, etc.)
            disponibilidad (int): Porcentaje de disponibilidad (0-100)
        """
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.disponibilidad = disponibilidad
        self.tareas_asignadas = []  # Lista de IDs de tareas asignadas
    
    def to_dict(self):
        """Convierte el usuario a diccionario para JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "disponibilidad": self.disponibilidad,
            "tareas_asignadas": self.tareas_asignadas
        }
    
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