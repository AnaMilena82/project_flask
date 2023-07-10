from flask import render_template, session, request, redirect, flash, url_for
from flask_app import app
from flask_app.models.model_users import User
from flask_app.models.model_magazines import Magazines
from flask_app.models.model_subscriptions import Subscription


def subscribe(user_id, magazine_id):
    user = User.get_one_with_id({'id': user_id})
    magazine = Magazines.get_one_magazine({'id': magazine_id})

    if user and magazine:
        if not Subscription.is_subscribed(user.id, magazine.id):
            magazine.add_subscriber(user.id)
            
       
            
    else:
        flash('Invalid user or magazine.', 'error_subscribe')

def get_subscribers(magazine_id):
    subscribers = Subscription.get_subscribers_by_magazine_id(magazine_id)
    return subscribers
