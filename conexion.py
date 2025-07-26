import MySQLdb

# Conexión a Railway
conexion = MySQLdb.connect(
    host="hopper.proxy.rlwy.net",
    user="root",
    passwd="cGdaJtdlaUbjKxSFJtSwvSHONLDdfKse",
    db="railway",
    port=39659
)

cursor = conexion.cursor()

# Tabla de historial (según tu back.py guarda nombre y precio directamente)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT NOT NULL,
        producto VARCHAR(255) NOT NULL,
        precio DECIMAL(10, 2) NOT NULL,
        fecha DATETIME NOT NULL
    );
""")

conexion.commit()
print("✅ Tabla 'historial' creada o verificada correctamente.")

cursor.close()
conexion.close()
