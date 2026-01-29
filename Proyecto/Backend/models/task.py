class Task:
    def __init__(self, id, titulo, estado="TODO", puntos=0, asignado_a=None):
        self.id = id
        self.titulo = titulo
        self.estado = estado  # Ahora será: "TODO", "IN_PROGRESS", "DONE"
        self.puntos = puntos
        self.asignado_a = asignado_a

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "estado": self.estado,
            "puntos": self.puntos,
            "asignado_a": self.asignado_a
        }