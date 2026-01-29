class Task:
    def __init__(self, id, titulo, estado, puntos=1, asignado_a=None, estimacion_minutos=60):
        self.id = id
        self.titulo = titulo
        self.estado = estado
        self.puntos = puntos
        self.asignado_a = asignado_a
        self.estimacion_minutos = estimacion_minutos  # Tiempo en minutos
        self.creado_en = None  # Podrías añadir datetime si lo necesitas
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "estado": self.estado,
            "puntos": self.puntos,
            "asignado_a": self.asignado_a,
            "estimacion_minutos": self.estimacion_minutos
        }