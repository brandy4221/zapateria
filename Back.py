from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

app = Flask(__name__)

# =========================
# 🔒 Configuración básica de cookies
# =========================
app.config['SESSION_COOKIE_SECURE'] = False     # ⚠️ Cambiado a False para entorno local
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# =========================
# 🗄️ Configuración de base de datos (Railway)
# =========================
app.config['MYSQL_HOST'] = 'crossover.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'BUTErcDTUHpxSkpZkOZdooYDdNFcgzzD'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 36112

mysql = MySQL(app)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_segura')

# =========================
# 🔹 Rutas principales
# =========================
@app.route('/')
def index():
    return redirect(url_for('login'))

# --------------------
# Registro
# --------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        aceptar = request.form.get('aceptar_terminos')

        if not aceptar:
            flash("Debes aceptar los Términos y Condiciones para registrarte.", "error")
            return redirect(url_for('registro'))

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

# --------------------
# Login
# --------------------
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

            if usuario['rol'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('productos'))
        else:
            flash('Correo o contraseña incorrectos', 'error')

    return render_template('login.html')

# --------------------
# Productos (cliente)
# --------------------
@app.route('/productos')
def productos():
    if 'logueado' in session and session['rol'] == 'cliente':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        return render_template('productos.html', productos=productos, nombre=session['nombre'])
    return redirect(url_for('login'))

# --------------------
# Panel de administrador
# --------------------
@app.route('/admin')
def admin():
    if 'logueado' in session and session['rol'] == 'admin':

        # 🔥 CAMBIO AÑADIDO (ver productos)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        return render_template('admin.html', productos=productos, nombre=session['nombre'])

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

# --------------------
# API / JSON
# --------------------
@app.route('/ver-productos-json')
def ver_productos_json():
    if 'logueado' in session and session['rol'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        return jsonify(productos)
    return redirect(url_for('login'))

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

# --------------------
# Carrito y compras
# --------------------
@app.route('/carrito')
def carrito():
    if 'logueado' not in session:
        return redirect(url_for('login'))
    carrito = session.get('carrito', [])
    return render_template('carrito.html', carrito=carrito)

@app.route('/agregar-al-carrito/<int:id>')
def agregar_al_carrito(id):
    if 'logueado' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, nombre, precio FROM productos WHERE id = %s', (id,))
    producto = cursor.fetchone()

    if producto:
        if 'carrito' not in session:
            session['carrito'] = []
        session['carrito'].append(producto)
        session.modified = True
        flash(f'{producto["nombre"]} agregado al carrito.', 'success')
    return redirect(url_for('productos'))

@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    if 'logueado' not in session:
        return redirect(url_for('login'))

    carrito = session.get('carrito', [])
    if not carrito:
        flash('El carrito está vacío.', 'error')
        return redirect(url_for('carrito'))

    cursor = mysql.connection.cursor()
    for item in carrito:
        cursor.execute("""
            INSERT INTO historial (usuario_id, producto, precio, fecha)
            VALUES (%s, %s, %s, NOW())
        """, (session['id'], item['nombre'], item['precio']))
    mysql.connection.commit()

    session['carrito'] = []
    flash('✅ Compra finalizada y registrada en tu historial.', 'success')
    return redirect(url_for('historial'))

@app.route('/historial')
def historial():
    if 'logueado' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT producto, precio, fecha FROM historial
        WHERE usuario_id = %s ORDER BY fecha DESC
    """, (session['id'],))
    compras = cursor.fetchall()
    return render_template('historial.html', historial=compras)

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/healthz')
def health():
    return 'OK', 200

# =========================
# 🚫 Sin cabeceras de seguridad (modo prueba)
# =========================
@app.after_request
def disable_security_headers(response):
    headers_to_remove = [
        'Content-Security-Policy',
        'X-Frame-Options',
        'Strict-Transport-Security',
        'X-Content-Type-Options',
        'Referrer-Policy'
    ]
    for h in headers_to_remove:
        response.headers.pop(h, None)
    return response

# =========================
# 🚀 Ejecución
# =========================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
