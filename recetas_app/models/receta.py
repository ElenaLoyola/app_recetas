from recetas_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Receta:
    db_name = 'esquema_recetas'
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.instrucciones = data['instrucciones']
        self.fecha = data['fecha']
        self.tiempo_prep = data['tiempo_prep']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']
        self.creador = data['creador'] #agregué como atributo de clase la concatenacion en query del nombre y apellido de usario, para poder llamarla en plantilla
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO recetas (nombre, descripcion, instrucciones, fecha, tiempo_prep, usuario_id) 
        VALUES ( %(nombre)s, %(descripcion)s, %(instrucciones)s, %(fecha)s, %(tiempo_prep)s, %(usuario_id)s );"""
        resultado = connectToMySQL(cls.db_name).query_db(query, data)
        return resultado

    @classmethod
    def get_all_with_user(cls):
        query  = """SELECT recetas.id, recetas.nombre, recetas.descripcion, recetas.instrucciones, recetas.fecha, recetas.tiempo_prep,
        recetas.created_at, recetas.updated_at, recetas.usuario_id, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS creador FROM recetas 
        JOIN usuarios ON recetas.usuario_id = usuarios.id;"""
        resultado = connectToMySQL(cls.db_name).query_db(query)
        recetas_con_usuario = []
        for receta in resultado:
            recetas_con_usuario.append(cls(receta))
        return recetas_con_usuario

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recetas;"
        resultado = connectToMySQL(cls.db_name).query_db(query)
        recetas = []
        for receta in resultado:
            recetas.append(cls(receta))
        return recetas
    
    @classmethod
    def get_one_with_user(cls, data):
        query  = """SELECT recetas.id, recetas.nombre, recetas.descripcion, recetas.instrucciones, recetas.fecha, recetas.tiempo_prep,
        recetas.created_at, recetas.updated_at, recetas.usuario_id, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS creador
        FROM recetas JOIN usuarios ON recetas.usuario_id = usuarios.id WHERE recetas.id = %(id)s;"""
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(result[0])

    @classmethod
    def actualizar(cls, data):
        query = """UPDATE recetas SET nombre=%(nombre)s, descripcion=%(descripcion)s, instrucciones=%(instrucciones)s,
        fecha=%(fecha)s, tiempo_prep=%(tiempo_prep)s WHERE id = %(receta_id)s;"""
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def eliminar(cls, data):
        query  = "DELETE FROM recetas WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_recipes_with_user(cls):
        query  = """SELECT recetas.nombre, recetas.descripcion, recetas.instrucciones, recetas.fecha, recetas.tiempo_prep,
        recetas.created_at, recetas.updated_at, recetas.usuario_id, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS creador FROM recetas 
        JOIN usuarios ON recetas.usuario_id = usuarios.id;"""
        resultado = connectToMySQL(cls.db_name).query_db(query)
        recetas_con_usuario = []
        for receta in resultado:
            recetas_con_usuario.append(cls(receta))
        return recetas_con_usuario

    @staticmethod
    def validar_receta(receta):
        is_valid = True
        #VALIDACION NOMBRE
        if len(receta['nombre']) < 3:
            flash("El nombre debe tener al menos 3 caracteres.")
            is_valid = False
        #VALIDACION DESCRIPCION
        if len(receta['descripcion']) < 3:
            flash("La descripción debe tener al menos 3 caracteres.")
            is_valid = False
        #VALIDACION INSTRUCCIONES
        if len(receta['instrucciones']) < 3:
            flash("Las instrucciones deben tener al menos 3 caracteres.")
            is_valid = False
        return is_valid