from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuración de MySQL usando variables de entorno
#app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', '127.0.0.1')
#app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
#app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
#app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'zapateria')
#app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
app.config['MYSQL_HOST'] = 'hopper.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cGdaJtdlaUbjKxSFJtSwvSHONLDdfKse'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 39659  
# Usa el puerto externo de Railway
 

app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_segura')


mysql = MySQL(app)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_segura')

# Ruta raíz
@app.route('/')
def index():
    return redirect(url_for('login'))

# Registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        cuenta = cursor.fetchone()

        if cuenta:
            flash('¡El correo ya está registrado!', 'error')
        else:
            hash_pass = generate_password_hash(password)
            cursor.execute(
                'INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)',
                (nombre, email, hash_pass, 'cliente')
            )
            mysql.connection.commit()
            # Iniciar sesión automáticamente después del registro
            session['logueado'] = True
            session['nombre'] = nombre
            session['rol'] = 'cliente'
            flash('¡Registro exitoso! Bienvenido.', 'success')
            return redirect(url_for('productos'))
    return render_template('registro.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['password'], password):
            session['logueado'] = True
            session['id'] = usuario['id']
            session['nombre'] = usuario['nombre']
            session['rol'] = usuario['rol']

            # Si es admin y es el correo especial
            if usuario['rol'] == 'admin' and email == 'martinwzbrandon@gmail.com':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('productos'))
        else:
            flash('Correo o contraseña incorrectos', 'error')

    return render_template('login.html')

# Página para cliente
@app.route('/productos')
def productos():
    if 'logueado' in session and session['rol'] == 'cliente':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        return render_template('productos.html', productos=productos, nombre=session['nombre'])
    return redirect(url_for('login'))

# Panel admin
@app.route('/admin')
def admin():
    if 'logueado' in session and session['rol'] == 'admin':
        return render_template('admin.html', nombre=session['nombre'])
    return redirect(url_for('login'))

# Agregar producto
@app.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    if 'logueado' in session and session['rol'] == 'admin':
        nombre = request.form['nombre']
        precio = request.form['precio']
        imagen = request.form['imagen']
        categoria = request.form['categoria']

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre, precio, imagen, categoria) VALUES (%s, %s, %s, %s)',
            (nombre, precio, imagen, categoria)
        )
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

# Editar producto
@app.route('/editar-producto/<int:id>', methods=['POST'])
def editar_producto(id):
    if 'logueado' in session and session['rol'] == 'admin':
        nombre = request.form['nombre']
        precio = request.form['precio']
        imagen = request.form['imagen']
        categoria = request.form['categoria']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE productos SET nombre=%s, precio=%s, imagen=%s, categoria=%s WHERE id=%s
        """, (nombre, precio, imagen, categoria, id))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

# Eliminar producto
@app.route('/eliminar-producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if 'logueado' in session and session['rol'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM productos WHERE id=%s', (id,))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

# Productos en JSON (para JS del admin)
@app.route('/ver-productos-json')
def ver_productos_json():
    if 'logueado' in session and session['rol'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        return jsonify(productos)
    return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Health check endpoint para Render (opcional)
@app.route('/healthz')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
