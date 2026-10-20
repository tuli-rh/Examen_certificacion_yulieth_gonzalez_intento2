from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.entrada import Entrada
from flask_app.models.usuario import Usuario

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario = Usuario.get_by_id({'id': session['usuario_id']})
    entradas = Entrada.get_by_user_id({'usuario_id': session['usuario_id']})
    
    return render_template('dashboard.html', usuario=usuario, entradas=entradas)

@app.route('/nueva')
def nueva_entrada():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('nueva_entrada.html')

@app.route('/crear_entrada', methods=['POST'])
def crear_entrada():
    if 'usuario_id' not in session:
        return redirect('/')
        
    if not Entrada.validar_entrada(request.form):
        return redirect('/nueva')
        
    data = {
        'fecha_entrada': request.form['fecha_entrada'],
        'notas': request.form['notas'],
        'usuario_id': session['usuario_id']
    }
    Entrada.save(data)
    return redirect('/dashboard')

@app.route('/ver/<int:id>')
def ver_entrada(id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    entrada = Entrada.get_by_id({'id': id})
    
    # BONUS: Validación de privacidad/propiedad
    if not entrada or entrada.usuario_id != session['usuario_id']:
        return redirect('/dashboard')
        
    return render_template('mostrar_entrada.html', entrada=entrada)

@app.route('/editar/<int:id>')
def editar_entrada(id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    entrada = Entrada.get_by_id({'id': id})
    
    # BONUS: Impedir editar entradas ajenas mediante URL
    if not entrada or entrada.usuario_id != session['usuario_id']:
        return redirect('/dashboard')
        
    return render_template('editar_entrada.html', entrada=entrada)

@app.route('/actualizar_entrada/<int:id>', methods=['POST'])
def actualizar_entrada(id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    entrada = Entrada.get_by_id({'id': id})
    if not entrada or entrada.usuario_id != session['usuario_id']:
        return redirect('/dashboard')
        
    if not Entrada.validar_entrada(request.form):
        return redirect(f'/editar/{id}')
        
    data = {
        'id': id,
        'fecha_entrada': request.form['fecha_entrada'],
        'notas': request.form['notas'],
        'usuario_id': session['usuario_id']
    }
    Entrada.update(data)
    return redirect('/dashboard')

@app.route('/borrar/<int:id>')
def borrar_entrada(id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    # BONUS: Impedir borrar entradas de otros usuarios
    entrada = Entrada.get_by_id({'id': id})
    if entrada and entrada.usuario_id == session['usuario_id']:
        Entrada.destroy({'id': id, 'usuario_id': session['usuario_id']})
        
    return redirect('/dashboard')

@app.route('/buscar')
def buscar_redir():
    if 'usuario_id' not in session:
        return redirect('/')
    # Captura el término del formulario
    termino = request.args.get('termino', '')
    if not termino:
        return redirect('/dashboard')
    return redirect(f'/buscar/{termino}')

@app.route('/buscar/<string:termino>')
def buscar_entrada(termino):
    if 'usuario_id' not in session:
        return redirect('/')
        
    entradas = Entrada.search_by_notes({
        'usuario_id': session['usuario_id'],
        'termino': termino
    })
    
    return render_template('buscar.html', entradas=entradas, termino=termino)
