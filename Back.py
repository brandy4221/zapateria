# back.py actualizado con carrito e historial de compras

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from datetime import datetime

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
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
            cursor.execute('INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)',
                           (nombre, email, hash_pass, 'cliente'))
            mysql.connection.commit()
            session['logueado'] = True
            session['nombre'] = nombre
            session['rol'] = 'cliente'
            flash('¡Registro exitoso!', 'success')
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

            return redirect(url_for('admin' if usuario['rol'] == 'admin' else 'productos'))
        else:
            flash('Correo o contraseña incorrectos', 'error')
    return render_template('login.html')

@app.route('/productos')
def productos():
    if 'logueado' in session and session['rol'] == 'cliente':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        return render_template('productos.html', productos=productos, nombre=session['nombre'])
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'logueado' in session and session['rol'] == 'admin':
        return render_template('admin.html', nombre=session['nombre'])
    return redirect(url_for('login'))

@app.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    if 'logueado' in session and session['rol'] == 'admin':
        nombre = request.form['nombre']
        precio = request.form['precio']
        imagen = request.form['imagen']
        categoria = request.form['categoria']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO productos (nombre, precio, imagen, categoria) VALUES (%s, %s, %s, %s)',
                       (nombre, precio, imagen, categoria))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/carrito')
def carrito():
    if 'logueado' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT c.id, p.nombre, p.precio FROM carrito c JOIN productos p ON c.producto_id = p.id WHERE c.usuario_id = %s',
                       (session['id'],))
        items = cursor.fetchall()
        return render_template('carrito.html', items=items)
    return redirect(url_for('login'))

@app.route('/agregar-carrito/<int:id>')
def agregar_carrito(id):
    if 'logueado' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO carrito (usuario_id, producto_id) VALUES (%s, %s)', (session['id'], id))
        mysql.connection.commit()
        return redirect(url_for('carrito'))
    return redirect(url_for('login'))

@app.route('/comprar')
def comprar():
    if 'logueado' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT producto_id FROM carrito WHERE usuario_id = %s', (session['id'],))
        items = cursor.fetchall()
        for item in items:
            cursor.execute('INSERT INTO historial_compras (usuario_id, producto_id, fecha) VALUES (%s, %s, %s)',
                           (session['id'], item['producto_id'], datetime.now()))
        cursor.execute('DELETE FROM carrito WHERE usuario_id = %s', (session['id'],))
        mysql.connection.commit()
        return redirect(url_for('historial'))
    return redirect(url_for('login'))

@app.route('/historial')
def historial():
    if 'logueado' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT h.fecha, p.nombre, p.precio FROM historial_compras h JOIN productos p ON h.producto_id = p.id WHERE h.usuario_id = %s',
                       (session['id'],))
        historial = cursor.fetchall()
        return render_template('historial.html', historial=historial)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.after_request
def set_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
