from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.model_magazines import Magazines
from flask_app import BASE_DE_DATOS, EMAIL_REGEX


class User:
    def __init__( self, data ):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.password = data["password"]
        self.email = data["email"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.magazines = []

    @classmethod
    def new_one_user( cls, data ):
        query = """
                INSERT INTO users ( first_name, last_name, email, password )
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );
                """
        result = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        return result
    
    @classmethod
    def get_one_with_email( cls, data ):
        query = """
                SELECT *
                FROM users
                WHERE email = %(email)s;
                """
        result = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        if len( result ) == 0:
            return None
        else:
            return User( result[0] )


    @classmethod  
    def show_one_user(cls, data):
        query = """
                SELECT * 
                FROM users 
                WHERE id = %(id)s;     
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        user = User (result [0])
        return user

    @classmethod  
    def update_one_user(cls, data):
        query = """
                UPDATE users 
                SET first_name = %(first_name)s,last_name = %(last_name)s,email = %(email_account)s 
                WHERE id = %(id)s;
                """
        return connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        

    @classmethod
    def get_one_with_id(cls, data):
        query = """
            SELECT *
            FROM users
            WHERE id = %(id)s;
        """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        if len(result) == 0:
            return None
        else:
            return cls(result[0])


    @staticmethod
    def validate_register( data ):
        is_valid = True

        if len( data['first_name'] ) < 3:
            is_valid = False
            flash( "You need to provide your name.", "error_firstname" )
        if len( data['last_name'] ) < 3:
            is_valid = False
            flash( "You need to provide your lastname..", "error_lastname" )
        if len( data['password'] ) < 8:
            is_valid = False
            flash( "Your password needs to be at least 8 characters.", "error_password" )
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash( "The passwords do not match.", "error_password" )
        if not EMAIL_REGEX.match( data['email'] ):
            is_valid = False
            flash( "Please provide a valid email", "error_email" )
        if data['email'] != " " and User.check_email_exists(data['email']):
            is_valid = False
            flash("This email is already registered.", "error_email")

        return is_valid
    
    @staticmethod
    def validate_update( data ):
        is_valid = True

        if len( data['first_name'] ) < 3:
            is_valid = False
            flash( "You need to provide your name.", "error_firstname" )
        if len( data['last_name'] ) < 3:
            is_valid = False
            flash( "You need to provide your lastname..", "error_lastname" )
        if data['email_account'] != "":
            user = User.get_one_with_email({'email': data['email_account']})
            if user is not None and data['email_account'] != user.email:
                if not EMAIL_REGEX.match(data['email_account']):
                    is_valid = False
                    flash("Please provide a valid email", "error_email_account")
                if User.check_email_exists(data['email_account']):
                    is_valid = False
                    flash("This email is already registered.", "error_email_account")
        else:
            is_valid = False
            flash("Email field cannot be empty.", "error_email_account")
        return is_valid
    
    @staticmethod
    def check_email_exists(email):
        query = """
                SELECT id
                FROM users
                WHERE email = %(email)s;
                """
        data = {
            'email': email
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        if result:
            return True
        return False

    @staticmethod
    def validate_login( data ):
        is_valid = True
        if data == None:
            flash( "This email does not exist.", "error_email_login" )
            is_valid = False
        
        return is_valid
    
    @staticmethod 
    def validate_sesion():
        if 'user_id' in session:
            return True
        else:
            return False
        
    @staticmethod
    def get_subscribed_magazines(user_id):
        from flask_app.models.model_magazines import Magazines
        query = """
            SELECT m.*
            FROM magazines AS m
            INNER JOIN subscriptions AS s ON s.magazine_id = m.id
            WHERE s.user_id = %(user_id)s;
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