import MySQLdb
from werkzeug.security import generate_password_hash

# Conexión a Railway
conexion = MySQLdb.connect(
    host='yamanote.proxy.rlwy.net',
    user='root',
    passwd='cAIVufUhqilyQcyljngZppKBcPfJEzae',
    db='railway',
    port=21739
)

cursor = conexion.cursor()

# Crear tablas necesarias
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol VARCHAR(20) DEFAULT 'cliente'
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        precio DECIMAL(10, 2) NOT NULL,
        imagen TEXT,
        categoria VARCHAR(50)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT NOT NULL,
        producto VARCHAR(255) NOT NULL,
        precio DECIMAL(10, 2) NOT NULL,
        fecha DATETIME NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS carrito (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT NOT NULL,
        producto_id INT NOT NULL,
        cantidad INT DEFAULT 1,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    );
""")

# Insertar usuario administrador si no existe
email_admin = 'martinwzbrandon@gmail.com'
nombre_admin = 'Administrador'
password_clara = '123456'
hashed_password = generate_password_hash(password_clara)

cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email_admin,))
existe = cursor.fetchone()

if not existe:
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, password, rol)
        VALUES (%s, %s, %s, %s)
    """, (nombre_admin, email_admin, hashed_password, 'admin'))
    print(f"✅ Usuario administrador creado: {email_admin}")
else:
    print("⚠️ El usuario administrador ya existe.")

conexion.commit()
cursor.close()
conexion.close()

print("✅ Base de datos configurada completamente.")
