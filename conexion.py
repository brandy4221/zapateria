from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors

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
        
        # Borra el usuario admin si existe
        cursor.execute("DELETE FROM usuarios WHERE email = %s", (email,))
        
        # Inserta nuevo admin con contraseña hasheada ya creada
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password, rol) VALUES (
                %s, %s, %s, %s
            )
        """, (
            'Administrador',
            email,
            '$pbkdf2-sha256$29000$J6m9H2P6cTHeaV7YN3vfwQ$qlJv5yTK+6W1c0FR4ocArItnUQ3XQjV0U6OAxnmW2u0',
            'admin'
        ))

        mysql.connection.commit()
        return "Admin actualizado correctamente."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
