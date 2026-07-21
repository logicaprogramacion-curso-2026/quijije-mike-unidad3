import sqlite3

def inicializar_base_datos():
    # 1. Crear y conectar a la base de datos (creará el archivo si no existe)
    conexion = sqlite3.connect('contador_calorias.db')
    cursor = conexion.cursor()

    # 2. Crear las tablas
    # Tabla Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        peso_actual REAL,
        meta_calorias_diarias INTEGER,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Tabla Alimentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alimentos (
        id_alimento INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_alimento TEXT NOT NULL,
        marca TEXT,
        calorias_por_100g INTEGER NOT NULL,
        proteinas REAL,
        carbohidratos REAL,
        grasas REAL
    )
    ''')

    # Tabla Registro Diario
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Registro_Diario (
        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_alimento INTEGER,
        cantidad_gramos REAL NOT NULL,
        fecha_consumo DATE NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
        FOREIGN KEY (id_alimento) REFERENCES Alimentos(id_alimento)
    )
    ''')

    # 3. Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()
    
    print("¡Base de datos 'contador_calorias.db' creada con éxito!")

if __name__ == '__main__':
    inicializar_base_datos()