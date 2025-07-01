from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configuración de Railway MySQL
app.config['MYSQL_HOST'] = 'hopper.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cGdaJtdlaUbjKxSFJtSwvSHONLDdfKse'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 39659  # Usa el puerto externo de Railway

mysql = MySQL(app)

@app.route('/')
def insertar_admin():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        email = 'martinwzbrandon@gmail.com'
        nombre = 'Administrador'
        password = '123456'
        rol = 'admin'

        # Verificar si ya existe
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        existe = cursor.fetchone()

        if existe:
            return 'Ya existe un usuario con ese correo.'
        
        # Encriptar contraseña
        hash_pass = generate_password_hash(password)

        # Insertar admin
        cursor.execute(
            'INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)',
            (nombre, email, hash_pass, rol)
        )
        mysql.connection.commit()
        return 'Administrador insertado correctamente.'
    
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
