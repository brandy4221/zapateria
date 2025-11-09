import MySQLdb
from werkzeug.security import generate_password_hash

# 🚀 Nueva conexión a Railway
conexion = MySQLdb.connect(
    host='crossover.proxy.rlwy.net',
    user='root',
    passwd='BUTErcDTUHpxSkpZkOZdooYDdNFcgzzD',
    db='railway',
    port=36112
)

cursor = conexion.cursor()

# 🧱 Crear tabla de usuarios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol VARCHAR(20) DEFAULT 'cliente'
    );
""")

# 🧱 Crear tabla de productos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        precio DECIMAL(10, 2) NOT NULL,
        imagen TEXT,
        categoria VARCHAR(50)
    );
""")

# 🧱 Crear tabla de historial de compras
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

# 🧱 Crear tabla de carrito
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

# 🧱 Crear tabla de logs opcional (seguridad o auditoría)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        evento VARCHAR(255),
        fecha DATETIME DEFAULT NOW()
    );
""")

# 👤 Crear usuario administrador
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

print("✅ Base de datos configurada completamente en Railway.")
