import os
from datetime import datetime, date
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

DB_NAME = os.getenv('DB_NAME', 'esquema_diario')

class Entrada:
    def __init__(self, data):
        self.id = data['id']
        self.fecha_entrada = data['fecha_entrada']
        self.notas = data['notas']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO entradas (fecha_entrada, notas, usuario_id)
            VALUES (%(fecha_entrada)s, %(notas)s, %(usuario_id)s);
        """
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def get_by_user_id(cls, data):
        # BONUS: Orden de más reciente a más antigua
        query = """
            SELECT * FROM entradas 
            WHERE usuario_id = %(usuario_id)s 
            ORDER BY fecha_entrada DESC, created_at DESC;
        """
        results = connectToMySQL(DB_NAME).query_db(query, data)
        entradas = []
        if results:
            for row in results:
                entradas.append(cls(row))
        return entradas

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM entradas WHERE id = %(id)s;"
        results = connectToMySQL(DB_NAME).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE entradas 
            SET fecha_entrada = %(fecha_entrada)s, notas = %(notas)s 
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM entradas WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def search_by_notes(cls, data):
        # BONUS: Buscar por término en notas restringido al usuario en sesión
        query = """
            SELECT * FROM entradas 
            WHERE usuario_id = %(usuario_id)s AND notas LIKE %(busqueda)s
            ORDER BY fecha_entrada DESC;
        """
        data['busqueda'] = f"%{data['termino']}%"
        results = connectToMySQL(DB_NAME).query_db(query, data)
        entradas = []
        if results:
            for row in results:
                entradas.append(cls(row))
        return entradas

    @staticmethod
    def validar_entrada(entrada):
        is_valid = True
        
        if not entrada.get('fecha_entrada'):
            flash("La fecha no puede estar vacía.", "entrada")
            is_valid = False
        else:
            fecha_ingresada = datetime.strptime(entrada['fecha_entrada'], '%Y-%m-%d').date()
            if fecha_ingresada > date.today():
                flash("No se puede ingresar una fecha en el futuro.", "entrada")
                is_valid = False

        if not entrada.get('notas') or len(entrada['notas'].strip()) == 0:
            flash("Notas no puede estar vacía.", "entrada")
            is_valid = False

        return is_valid