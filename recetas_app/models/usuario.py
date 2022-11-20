from recetas_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from recetas_app import app
bcrypt = Bcrypt(app) 
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    db_name = 'esquema_recetas'
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.correo_electronico= data['correo_electronico']
        self.contraseña = data['contraseña']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recetas = [] #lista de recetas de un usuario , en razón de la union de las tablas
    
    @classmethod
    def save(cls, data): #registrar usuario
        query = """INSERT INTO usuarios (nombre, apellido, correo_electronico, contraseña) 
        VALUES ( %(nombre)s, %(apellido)s, %(correo_electronico)s, %(contraseña)s);"""
        resultado = connectToMySQL(cls.db_name).query_db(query, data)
        return resultado
    
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s"
        resultado = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(resultado[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = "Select * FROM usuarios WHERE correo_electronico = %(correo_electronico)s"
        resultado = connectToMySQL(cls.db_name).query_db(query, data)
        if len(resultado) < 1:
            return False 
        return cls(resultado[0])
    
    @staticmethod
    def validar_usuario(usuario):
        correo = { "correo_electronico": usuario['correo_electronico']}
        is_valid = True
        #VALIDACION NOMBRE
        if len(usuario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        #VALIDACION APELLIDO
        if len(usuario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        #VALIDACIÓN CORREO ELECTRONICO
        if not (usuario['correo_electronico']):
            flash("Debe ingresar un correo electrónico.", "registro")
            is_valid = False
        elif not EMAIL_REGEX.match(usuario['correo_electronico']): 
            flash("¡Correo electrónico inválido! Ingresa uno nuevo.", "registro")
            is_valid = False
        elif Usuario.get_by_email(correo):
            flash("Este correo ya fue registrado, ingresa con tu contraseña.", "registro")
            is_valid = False
        #VALIDACION CONTRASEÑA
        if not (usuario['contraseña']):
            flash("Debe ingresar una contraseña.", "registro")
            is_valid = False
        #VALIDACION CONFIRMACION CONTRASEÑA
        if usuario['contraseña'] != usuario['contraseña2']:
            flash("Las contraseñas no coinciden, inténtalo de nuevo.", "registro")
            is_valid = False
        return is_valid