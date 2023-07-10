from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import BASE_DE_DATOS

class Subscription:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.magazine_id = data["magazine_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create_subscription(cls, user_id, magazine_id):
        query = """
            INSERT INTO subscriptions (user_id, magazine_id)
            VALUES (%(user_id)s, %(magazine_id)s);
        """
        data = {
            'user_id': user_id,
            'magazine_id': magazine_id
        }
        subscription_id = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        return subscription_id

    @classmethod
    def get_subscriptions_by_user(cls, user_id):
        query = """
            SELECT *
            FROM subscriptions
            WHERE user_id = %(user_id)s;
        """
        data = {
            'user_id': user_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        subscriptions = []
        for row in result:
            subscription = Subscription(row)
            subscriptions.append(subscription)
        return subscriptions

    @classmethod
    def get_subscriptions_by_magazine(cls, magazine_id):
        query = """
            SELECT *
            FROM subscriptions
            WHERE magazine_id = %(magazine_id)s;
        """
        data = {
            'magazine_id': magazine_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        subscriptions = []
        for row in result:
            subscription = Subscription(row)
            subscriptions.append(subscription)
        return subscriptions

    @classmethod
    def get_subscribers_by_magazine_id(cls, magazine_id):
        from flask_app.models.model_users import User
        query = """
            SELECT users.*
            FROM users
            JOIN subscriptions ON subscriptions.user_id = users.id
            WHERE subscriptions.magazine_id = %(magazine_id)s;
        """
        data = {
            'magazine_id': magazine_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        subscribers = []
        for row in result:
            subscriber = User(row)
            subscribers.append(subscriber)
        return subscribers
    
    @classmethod
    def is_subscribed(cls, user_id, magazine_id):
        query = """
            SELECT *
            FROM subscriptions
            WHERE user_id = %(user_id)s AND magazine_id = %(magazine_id)s;
        """
        data = {
            'user_id': user_id,
            'magazine_id': magazine_id
        }
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)
        return len(result) > 0