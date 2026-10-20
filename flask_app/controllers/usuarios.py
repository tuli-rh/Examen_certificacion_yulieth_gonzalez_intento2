from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    
    password_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'edad': request.form['edad'],
        'password': password_hash
    }
    
    usuario_id = Usuario.save(data)
    session['usuario_id'] = usuario_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_email({'email': request.form['email']})
    
    if not usuario or not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Credenciales inválidas", "login")
        return redirect('/')
        
    session['usuario_id'] = usuario.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')