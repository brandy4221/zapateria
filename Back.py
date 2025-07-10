

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

app = Flask(__name__)

# Configuraciones de seguridad para cookies
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Configuración de base de datos Railway
app.config['MYSQL_HOST'] = 'hopper.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cGdaJtdlaUbjKxSFJtSwvSHONLDdfKse'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 39659

mysql = MySQL(app)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_segura')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        # Validar email básico
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Correo inválido", "error")
            return redirect(url_for('registro'))

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
            session['logueado'] = True
            session['nombre'] = nombre
            session['rol'] = 'cliente'
            flash('¡Registro exitoso! Bienvenido.', 'success')
            return redirect(url_for('productos'))
    return render_template('registro.html')

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

            if usuario['rol'] == 'admin' and email == 'martinwzbrandon@gmail.com':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('productos'))
        else:
            flash('Correo o contraseña incorrectos', 'error')

    return render_template('login.html')

@app.route('/productos')
def productos():
    if 'logueado' in session and session['rol'] == 'cliente':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        response = make_response(render_template('productos.html', productos=productos, nombre=session['nombre']))
        response.headers['Content-Security-Policy'] = "default-src 'self'; img-src *; script-src 'self' 'unsafe-inline'"
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'logueado' in session and session['rol'] == 'admin':
        response = make_response(render_template('admin.html', nombre=session['nombre']))
        response.headers['Content-Security-Policy'] = "default-src 'self'; img-src *; script-src 'self' 'unsafe-inline'"
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    return redirect(url_for('login'))

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

@app.route('/eliminar-producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if 'logueado' in session and session['rol'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM productos WHERE id=%s', (id,))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/ver-productos-json')
def ver_productos_json():
    if 'logueado' in session and session['rol'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        return jsonify(productos)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/healthz')
def health():
    return 'OK', 200

@app.route('/api/productos', methods=['GET'])
def api_productos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, nombre, precio FROM productos')
    productos = cursor.fetchall()
    return jsonify(productos)

@app.route('/api/secure-productos', methods=['GET'])
def secure_productos():
    token = request.args.get('token')
    if token != '123abc':
        return jsonify({'error': 'No autorizado'}), 401

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    return jsonify(productos)

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')
@app.route("/api/productos")
def api_productos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = cursor.fetchall()
    return jsonify(productos)
@app.route("/api/secure-productos")
def secure():
    if request.args.get("token") != "123abc":
        return {"error": "No autorizado"}, 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

@app.after_request
def set_secure_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

# También en la configuración de Flask:
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
