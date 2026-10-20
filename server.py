from flask_app import app
from flask_app.controllers.usuarios import usuarios_bp
from flask_app.controllers.entradas import entradas_bp
from flask import render_template


app.register_blueprint(usuarios_bp)
app.register_blueprint(entradas_bp)

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)