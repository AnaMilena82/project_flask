from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app,BASE_DE_DATOS
from flask import flash


class Magazines:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.description = db_data['description']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.subscribers = []

    
    @classmethod
    def new_magazine(cls,data):
        query = """INSERT INTO magazines (title,description,user_id)
                 VALUES (%(title)s,%(description)s, %(user_id)s);"""
        id_magazine = connectToMySQL(BASE_DE_DATOS).query_db(query,data)
        return id_magazine

    @classmethod
    def get_allmagazines_with_user(cls):
        from flask_app.models.model_users import User
        query = """
                SELECT * 
                FROM magazines m JOIN users u
                ON m.user_id = u.id;    
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query)
        list_magazines = []
        for row in result:
            magazine = Magazines(row)
            data_user = {
                "id":row['u.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['u.created_at'],
                "updated_at":row['u.updated_at']
            }
            user = User(data_user)
            magazine.user = user
            list_magazines.append(magazine)
        return list_magazines

    @classmethod  
    def show_one_magazine(cls, data):
        query = """
                SELECT * 
                FROM magazines 
                WHERE id = %(id)s;     
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        magazine = Magazines (result [0])
        return magazine

    @classmethod
    def show_one_magazine_with_user(cls, data):
        from flask_app.models.model_users import User
        query = """
                SELECT * 
                FROM magazines m JOIN users u
                ON m.user_id = u.id
                WHERE m.id = %(id)s;     
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        row = result [0]
        magazine = Magazines (row)
        data_user = {
                "id":row['u.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['u.created_at'],
                "updated_at":row['u.updated_at']
        }
        magazine.user = User(data_user)
        return magazine 

    @staticmethod
    def get_magazines_by_user_id(user_id):
        query = """
                SELECT *
                FROM magazines
                WHERE user_id = %(user_id)s;
                """
        data = {
            'user_id': user_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        magazines = []
        for row in result:
            magazine = Magazines(row)
            magazines.append(magazine)
        return magazines 

    @staticmethod
    def get_user_id_by_magazine_id(magazine_id):
        query = """
                SELECT user_id
                FROM magazines
                WHERE id = %(magazine_id)s;
                """
        data = {
            'magazine_id': magazine_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        if result:
            return result[0]['user_id']
        return None


    @classmethod
    def delete_one_magazine(cls, data):
        query_delete_subscriptions = """
            DELETE FROM subscriptions
            WHERE magazine_id = %(id)s;
        """
        connectToMySQL(BASE_DE_DATOS).query_db(query_delete_subscriptions, data)

        query = """
                DELETE 
                FROM magazines 
                WHERE id = %(id)s;    
                """
        return connectToMySQL(BASE_DE_DATOS).query_db(query, data)

    @classmethod
    def get_one_magazine(cls, data):
        query = """
            SELECT *
            FROM magazines
            WHERE id = %(id)s;
        """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        if len(result) == 0:
            return None
        else:
            return cls(result[0])


    @staticmethod
    def validate_magazine(data):
        is_valid = True

        if len( data['title'] ) < 2:
            is_valid = False
            flash( "Title should be at least 2 characters.", "error_title" )
        if len( data['description'] ) < 10:
            is_valid = False
            flash( "Description should be at least 10 characters long.", "error_description" )
       
        return is_valid
    
    def get_subscribers(self):
        from flask_app.models.model_users import User
        query = """
            SELECT u.*
            FROM users AS u
            JOIN subscriptions AS s ON u.id = s.user_id
            WHERE s.magazine_id = %(magazine_id)s;
        """
        data = {
            'magazine_id': self.id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        subscribers = []
        for row in result:
            subscriber = User(row)
            subscribers.append(subscriber)
        self.subscribers = subscribers

    def add_subscriber(self, user_id):
        from flask_app.models.model_users import User
        query = """
            INSERT INTO subscriptions (user_id, magazine_id)
            VALUES (%(user_id)s, %(magazine_id)s);
        """
        data = {
            'user_id': user_id,
            'magazine_id': self.id
        }
        connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        self.get_subscribers()

    def remove_subscriber(self, user_id):
        query = """
            DELETE FROM subscriptions
            WHERE user_id = %(user_id)s AND magazine_id = %(magazine_id)s;
        """
        data = {
            'user_id': user_id,
            'magazine_id': self.id
        }
        connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        self.get_subscribers()
