from flask_app import app
from flask_app.controllers import usuarios, entradas
from flask import render_template

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)