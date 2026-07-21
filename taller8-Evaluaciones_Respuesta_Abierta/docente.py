class Docente:
    def __init__(self, id_docente=None, nombre="", apellido="", email="", especialidad=""):
        self.id_docente = id_docente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.especialidad = especialidad

    def to_dict(self):
        """Util para convertir el objeto a JSON en una API Flask."""
        return {
            "id_docente": self.id_docente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "especialidad": self.especialidad
        }

    def __repr__(self):
        return f"<Docente {self.nombre} {self.apellido} - {self.especialidad}>"