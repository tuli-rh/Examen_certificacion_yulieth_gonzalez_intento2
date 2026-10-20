from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.usuario import Usuario

# Instancia del Blueprint para usuarios
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@usuarios_bp.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    
    usuario_id = Usuario.guardar(request.form)
    session['usuario_id'] = usuario_id
    return redirect('/dashboard')

@usuarios_bp.route('/login', methods=['POST'])
def login():
    usuario = Usuario.validar_login(request.form)
    if not usuario:
        return redirect('/')
    
    session['usuario_id'] = usuario.id
    return redirect('/dashboard')

@usuarios_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')