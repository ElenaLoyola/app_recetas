from flask import render_template, request, redirect, session
from recetas_app import app
from recetas_app.models.receta import Receta
from recetas_app.models.usuario import Usuario

@app.route('/perfil')
def perfil_recetas():
    if 'usuario_id' not in session:   #validar si el usaurio se encuentra registrado
        return redirect('/')
    data = {
        "id": session['usuario_id']
    }
    usuario= Usuario.get_user(data)
    recetas = Receta.get_all_with_user()
    return render_template('perfil_recetas.html', usuario=usuario, recetas=recetas)

@app.route('/crear')
def nueva_receta():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('crear.html')

@app.route('/guardar', methods = ['POST'])
def crear_receta():
    if not Receta.validar_receta(request.form):
        return redirect('/crear')
    receta_id = Receta.save(request.form) #metodo retorna id de receta insertada en db
    return redirect ('/perfil')

@app.route('/ver/<int:id>')
def ver_receta(id):
    if 'usuario_id' not in session:
        return redirect('/')
    data = {
        "id": id 
    }
    receta= Receta.get_one_with_user(data)
    data = {
        "id": session['usuario_id']
    }
    usuario= Usuario.get_user(data)
    return render_template('ver.html', receta=receta, usuario=usuario)

@app.route('/editar/<int:id>')
def editar_receta(id):
    if 'usuario_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    receta= Receta.get_one_with_user(data)
    return render_template('editar.html', receta=receta)

@app.route('/actualizar', methods=['POST'])
def guardar_cambios():
    if not Receta.validar_receta(request.form):
        return redirect('/editar/'+request.form['receta_id']) #receta_id lo guardo con el hidden input en form #(f"/ver/{id}")
    Receta.actualizar(request.form)
    return redirect ('/perfil')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario_id' not in session:
        return redirect('/')
    data ={
        'id': id
    }
    Receta.eliminar(data)
    return redirect('/perfil')

