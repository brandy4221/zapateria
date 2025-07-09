import MySQLdb
from werkzeug.security import generate_password_hash

# Conexión a Railway
conexion = MySQLdb.connect(
    host="hopper.proxy.rlwy.net",
    user="root",
    passwd="cGdaJtdlaUbjKxSFJtSwvSHONLDdfKse",
    db="railway",
    port=39659
)

cursor = conexion.cursor()

# Datos del nuevo usuario
email = 'martinwzbrandon@gmail.com'
nombre = 'Administrador'
password_plano = '123456'
rol = 'admin'
hashed_password = generate_password_hash(password_plano)

# Crear usuario
cursor.execute("""
    INSERT INTO usuarios (nombre, email, password, rol)
    VALUES (%s, %s, %s, %s)
""", (nombre, email, hashed_password, rol))
conexion.commit()

print(f"✅ Usuario admin creado correctamente: {email}")

cursor.close()
conexion.close()
