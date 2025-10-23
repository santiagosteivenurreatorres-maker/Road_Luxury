from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esta clave en producción

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='rutalibre'
        )
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE nombre = %s AND contraseña = %s", (usuario, contraseña))
        resultado = cursor.fetchone()

        if resultado:
            session['usuario'] = resultado['nombre']
            return redirect(url_for('catalogo'))
        else:
            mensaje = "Usuario o contraseña incorrectos"
            return render_template('login.html', error=mensaje)

        cursor.close()
        conexion.close()

    return render_template('login.html', mensaje=mensaje)

# Registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='rutalibre'
        )
        cursor = conexion.cursor()

        try:
            cursor.execute("SELECT * FROM usuario WHERE nombre = %s", (usuario,))
            existente = cursor.fetchone()

            if existente:
                mensaje = "El nombre de usuario ya existe"
            else:
                print("Registrando nuevo usuario:")
                print("Nombre:", usuario)
                print("Correo:", correo)
                print("Contraseña:", contraseña)

                print("Ejecutando INSERT...")
                cursor.execute("""
                    INSERT INTO usuario (nombre, correo, contraseña)
                    VALUES (%s, %s, %s)
                """, (usuario, correo, contraseña))

                print("Haciendo commit...")
                conexion.commit()
                print("Registro guardado en la base de datos")

                session['usuario'] = usuario
                return redirect(url_for('catalogo'))

        except mysql.connector.Error as err:
            mensaje = "Error al registrar el usuario"
            print("MySQL Error:", err)

        finally:
            cursor.close()
            conexion.close()

    return render_template('registro.html', mensaje=mensaje)

# Catálogo
@app.route('/catalogo')
def catalogo():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('catalogo.html', usuario=session['usuario'])

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# Ruta agregada para evitar el BuildError
@app.route('/solicita_reserva')
def solicita_reserva():
    return "<h1>Página de solicitud de reserva en construcción</h1>"

if __name__ == '__main__':
    app.run(debug=True)
