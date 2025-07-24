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

# Crear tabla carrito
cursor.execute("""
    CREATE TABLE IF NOT EXISTS carrito (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT NOT NULL,
        producto_id INT NOT NULL
    );
""")

# Crear tabla historial de compras
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_compras (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT NOT NULL,
        producto_id INT NOT NULL,
        fecha DATETIME NOT NULL
    );
""")

conexion.commit()
print("✅ Tablas 'carrito' y 'historial_compras' creadas o verificadas con éxito.")

cursor.close()
conexion.close()
