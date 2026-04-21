from flask import Flask, render_template, request, url_for, redirect, flash, session
from database import conectar_bd

app = Flask(__name__)
app.secret_key = '123456789'


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_form():
    user     = request.form['user']
    password = request.form['password']

    conn   = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = %s AND password = %s",
        (user, password)
    )
    resultado = cursor.fetchall()
    conn.close()

    if resultado:
        usuario_existente = resultado[0]
        nombre = usuario_existente[1]
        rol    = usuario_existente[3]

        session['usuario'] = nombre
        session['rol']     = rol

        if rol.lower() == 'administrador':
            return redirect(url_for('inicio'))
        elif rol.lower() == 'empleado':
            return "Bienvenido empleado"
        else:
            return "Rol no válido"
    else:
        flash("Usuario o contraseña incorrectos", "danger")
        return redirect(url_for('login'))


@app.route('/inicio')
def inicio():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn   = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('index.html', user=usuarios, emp=empleados )


@app.route('/Salir')
def salir():
    session.clear()
    return redirect(url_for('login'))


@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    nombre    = request.form['nombre_usuario']
    contraseña = request.form['contraseña_usuario']
    rol       = request.form['rol_usuario']
    documento = request.form['documento_usuario']

    conn   = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (nombre,))
        if cursor.fetchone():
            flash("El nombre de usuario ya está registrado", "danger")
            return redirect(url_for('inicio'))

        cursor.execute("SELECT * FROM usuarios WHERE documento_Emple = %s", (documento,))
        if cursor.fetchone():
            flash("Ese documento ya tiene un usuario asignado", "danger")
            return redirect(url_for('inicio'))

        cursor.execute("SELECT * FROM empleados WHERE documento_Emple = %s", (documento,))
        if not cursor.fetchone():
            flash("El empleado con ese documento no está registrado", "danger")
            return redirect(url_for('inicio'))

        cursor.execute(
            "INSERT INTO usuarios (usuario, password, rol, documento_Emple) VALUES (%s, %s, %s, %s)",
            (nombre, contraseña, rol, documento)
        )
        conn.commit()
        flash("Usuario registrado correctamente", "success")

    except Exception as e:
        conn.rollback()
        flash(f"Error al registrar el usuario: {str(e)}", "danger")

    finally:
        conn.close()

    return redirect(url_for('inicio'))


@app.route('/registrar_empleado', methods=['POST'])
def registrar_emple():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Obtener datos del formulario
    documento    = request.form['documento_empleado']
    nombre       = request.form['nombre_empleado']
    apellido     = request.form['apellido_empleado']
    cargo        = request.form['cargo_empleado']
    id_area      = request.form['area_empleado']
    horas_extras = int(request.form['horas_extras'])
    bonificacion = float(request.form['bonificacion'])

    # Validaciones
    if not documento or not nombre or not apellido or not cargo or not id_area:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('inicio'))

    if not documento.isdigit():
        flash("El documento debe ser un número", "danger")
        return redirect(url_for('inicio'))

    # Salario base según cargo
    if cargo.lower() == "gerente":
        salario_base = 5000000
    elif cargo.lower() == "administrador":
        salario_base = 3500000
    elif cargo.lower() == "contador":
        salario_base = 2800000
    else:
        salario_base = 1800000

    # Cálculo de nómina
    horas_extras = horas_extras * 3000
    salario_bruto    = round(salario_base + bonificacion + horas_extras, 2)
    salud            = round(salario_base * 0.04, 2)
    pension          = round(salario_base * 0.04, 2)
    salario_neto     = round(salario_bruto - salud - pension, 2)

    conn   = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM empleados WHERE documento_Emple = %s", (documento,))
        if cursor.fetchone():
            flash("El documento ya está registrado", "danger")
            return redirect(url_for('inicio'))

        cursor.execute("SELECT * FROM areas WHERE id_area = %s", (id_area,))
        if not cursor.fetchone():
            flash("El área seleccionada no existe", "danger")
            return redirect(url_for('inicio'))

        cursor.execute("""
            INSERT INTO empleados
                (documento_Emple, nombre_Emple, apellido_Emple, cargo,
                 Salario_B, Horas_Extras, bonificacion, salud, pension, salario_Neto, id_area)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (documento, nombre, apellido, cargo,
              salario_base, horas_extras, bonificacion,
              salud, pension, salario_neto, id_area))

        conn.commit()
        flash("Empleado registrado correctamente", "success")

    except Exception as e:
        conn.rollback()
        flash(f"Error al registrar el empleado: {str(e)}", "danger")

    finally:
        conn.close()

    return redirect(url_for('inicio'))


@app.route('/eliminar/<int:id>')
def eliminarusu(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn   = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT rol FROM usuarios WHERE id_usuario = %s", (id,))
        resultado = cursor.fetchone()

        if resultado:
            if resultado[0].lower() == 'administrador':
                flash("No se puede eliminar al administrador", "danger")
            else:
                cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
                conn.commit()
                flash("Usuario eliminado correctamente", "success")

    except Exception as e:
        conn.rollback()
        flash(f"Error al eliminar el usuario: {str(e)}", "danger")

    finally:
        conn.close()

    return redirect(url_for('inicio'))

@app.route('/editarusu/<int:id>')
def editar_usu(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    conn   = conectar_bd()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, (id,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario:
        return render_template('editarusuario.html', usu = usuario)
    else:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for('inicio'))
    
    


@app.route('/actualizar', methods=['POST'])
def actualizar_usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    id_usuario = request.form['id_usuario']
    nombre     = request.form['nombre_usuario']
    password   = request.form['contraseña_usuario']
    rol        = request.form['rol_usuario']

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET usuario = %s,
            password = %s,
            rol = %s
        WHERE id_usuario = %s
    """, (nombre, password, rol, id_usuario))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Usuario actualizado correctamente", "success")
    return redirect(url_for('inicio'))


# ── Editar empleado: cargar datos ──
@app.route('/editar_emple/<int:id>')
def editar_emple(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM empleados WHERE id_Empleado = %s", (id,))
    emple = cursor.fetchone()

    cursor.execute("SELECT id_area, Nombre_A FROM areas")
    areas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('editaremple.html', emple=emple, areas=areas)


# ── Actualizar empleado: guardar cambios ──
@app.route('/actualizar_emple', methods=['POST'])
def actualizar_emple():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    id_empleado      = request.form['id_empleado']
    nombre_empleado  = request.form['nombre_empleado']
    apellido_empleado = request.form['apellido_empleado']
    cargo_empleado   = request.form['cargo_empleado']
    area_empleado    = request.form['area_empleado']
    horas_extras     = request.form['horas_extras']
    bonificacion     = request.form['bonificacion']

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE empleados
        SET nombre_Emple  = %s,
            apellido_Emple = %s,
            cargo          = %s,
            id_area        = %s,
            Horas_Extras   = %s,
            bonificacion   = %s
        WHERE id_Empleado = %s
    """, (nombre_empleado, apellido_empleado, cargo_empleado,
          area_empleado, horas_extras, bonificacion, id_empleado))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Empleado actualizado correctamente', 'success')
    return redirect(url_for('inicio'))


# ── Eliminar empleado ──
@app.route('/eliminar_emple/<int:id>')
def eliminar_emple(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM empleados WHERE id_Empleado = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Empleado eliminado correctamente', 'success')
    return redirect(url_for('inicio'))



if __name__ == '__main__':
    app.run(debug=True)