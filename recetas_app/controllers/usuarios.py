from flask import render_template, request, redirect, session, flash
from recetas_app.models.usuario import Usuario
from recetas_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def registro():
    return render_template('ingresar.html')

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    if not Usuario.validar_usuario(request.form):
        return redirect('/')
    #crear el hash
    pw_hash = bcrypt.generate_password_hash(request.form['contraseña'])
    print(pw_hash)
    #poner pw_hash en el diccionario de datos
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "correo_electronico": request.form['correo_electronico'],
        "contraseña": pw_hash
    }
    # llama al @classmethod de guardado en Usuario
    usuario_id = Usuario.save(data)
    # almacenar id de usuario en la sesión
    session['usuario_id'] = usuario_id
    print(session['usuario_id'])
    return redirect("/perfil")

@app.route('/ingresar', methods=['POST'])
def ingresar():
# ver si el nombre de usuario proporcionado existe en la base de datos
    data = { "correo_electronico": request.form["correo_electronico"] }
    user_in_db = Usuario.get_by_email(data)
    # usuario no está registrado en la base de datos
    if not user_in_db:
        flash("Correo o contraseña inválidos", "ingreso")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.contraseña, request.form['contraseña']):
        # si obtenemos False después de verificar la contraseña
        flash("Correo o contraseña inválidos", "ingreso")
        return redirect('/')
    # si las contraseñas coinciden, configuramos el user_id en sesión
    session['usuario_id'] = user_in_db.id
    # ¡¡¡Nunca renderices en una post!!!
    return redirect("/perfil")

@app.route('/salir')
def limpiar_session():
    session.clear()
    return redirect('/')
