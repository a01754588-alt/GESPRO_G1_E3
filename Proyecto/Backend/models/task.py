class Task:
    def __init__(self, id, titulo, estado):
        self.id = id
        self.titulo = titulo
        self.estado = estado

    def to_dict(self):
        # Método para convertir a diccionario y poder devolverlo como JSON
        return {
            "id": self.id,
            "titulo": self.titulo,
            "estado": self.estado
        }
