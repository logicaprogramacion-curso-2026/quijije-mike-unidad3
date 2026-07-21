import sqlite3
from docente import Docente

class DocenteDAO:
    def __init__(self, db_path="sistema.db"):
        self.db_path = db_path

    def _obtener_conexion(self):
        conexion = sqlite3.connect(self.db_path)
        conexion.row_factory = sqlite3.Row  # Permite acceder a columnas por su nombre
        return conexion

    def crear_tabla(self):
        """Crea la tabla docentes en SQLite si no existe."""
        sql = '''
        CREATE TABLE IF NOT EXISTS docentes (
            id_docente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            especialidad TEXT
        )
        '''
        with self._obtener_conexion() as conn:
            conn.execute(sql)

    def insertar(self, docente: Docente) -> bool:
        """Inserta un objeto Docente en la base de datos."""
        sql = '''
        INSERT INTO docentes (nombre, apellido, email, especialidad)
        VALUES (?, ?, ?, ?)
        '''
        try:
            with self._obtener_conexion() as conn:
                cursor = conn.execute(sql, (
                    docente.nombre,
                    docente.apellido,
                    docente.email,
                    docente.especialidad
                ))
                docente.id_docente = cursor.lastrowid
                return True
        except sqlite3.IntegrityError:
            print(f"Error: El email {docente.email} ya está registrado.")
            return False

    def obtener_por_id(self, id_docente: int) -> Docente:
        """Busca un docente por su ID."""
        sql = "SELECT * FROM docentes WHERE id_docente = ?"
        with self._obtener_conexion() as conn:
            row = conn.execute(sql, (id_docente,)).fetchone()
            if row:
                return Docente(
                    id_docente=row['id_docente'],
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    email=row['email'],
                    especialidad=row['especialidad']
                )
        return None

    def obtener_todos(self) -> list[Docente]:
        """Devuelve una lista con todos los docentes registrados."""
        sql = "SELECT * FROM docentes"
        with self._obtener_conexion() as conn:
            rows = conn.execute(sql).fetchall()
            return [
                Docente(
                    id_docente=r['id_docente'],
                    nombre=r['nombre'],
                    apellido=r['apellido'],
                    email=r['email'],
                    especialidad=r['especialidad']
                ) for r in rows
            ]

    def actualizar(self, docente: Docente) -> bool:
        """Actualiza la información de un docente existente."""
        sql = '''
        UPDATE docentes
        SET nombre = ?, apellido = ?, email = ?, especialidad = ?
        WHERE id_docente = ?
        '''
        with self._obtener_conexion() as conn:
            cursor = conn.execute(sql, (
                docente.nombre,
                docente.apellido,
                docente.email,
                docente.especialidad,
                docente.id_docente
            ))
            return cursor.rowcount > 0

    def eliminar(self, id_docente: int) -> bool:
        """Elimina un docente por su ID."""
        sql = "DELETE FROM docentes WHERE id_docente = ?"
        with self._obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_docente,))
            return cursor.rowcount > 0