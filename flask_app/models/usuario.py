import re
import os
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB_NAME = os.getenv('DB_NAME', 'esquema_diario')

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.edad = data['edad']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, edad, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(edad)s, %(password)s);
        """
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(DB_NAME).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL(DB_NAME).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validar_registro(usuario):
        is_valid = True
        
        if len(usuario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        if len(usuario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email']):
            flash("El email debe tener un formato válido.", "registro")
            is_valid = False
        else:
            if Usuario.get_by_email({'email': usuario['email']}):
                flash("El email ya está registrado.", "registro")
                is_valid = False
        
        try:
            if int(usuario['edad']) < 18:
                flash("Debes tener al menos 18 años de edad.", "registro")
                is_valid = False
        except (ValueError, TypeError):
            flash("Por favor ingrese una edad válida.", "registro")
            is_valid = False

        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            is_valid = False
        if usuario['password'] != usuario['confirm_password']:
            flash("La contraseña y la confirmación deben ser iguales.", "registro")
            is_valid = False

        return is_valid