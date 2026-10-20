from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.entrada import Entrada

# Instancia del Blueprint para entradas
entradas_bp = Blueprint('entradas', __name__)

@entradas_bp.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Cambiado get_by_user a get_by_user_id
    entradas = Entrada.get_by_user_id({'usuario_id': session['usuario_id']})
    return render_template('dashboard.html', entradas=entradas)

@entradas_bp.route('/buscar')
def buscar_redir():
    if 'usuario_id' not in session:
        return redirect('/')
    termino = request.args.get('termino', '')
    if not termino:
        return redirect('/dashboard')
    return redirect(f'/buscar/{termino}')

@entradas_bp.route('/buscar/<string:termino>')
def buscar_entrada(termino):
    if 'usuario_id' not in session:
        return redirect('/')
        
    entradas = Entrada.search_by_notes({
        'usuario_id': session['usuario_id'],
        'termino': termino
    })
    
    return render_template('buscar.html', entradas=entradas, termino=termino)