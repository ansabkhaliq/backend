import os
import logging
from flask import Blueprint, request, jsonify, session

router = Blueprint('router', __name__)


# Using router controller to manage all path

@router.route('/login')
def login():
    if validate_login_session():
        return main.index()
    return "login page here", 200


@router.route('/')
def index():
    return "index.html", 200


@router.route('/order')
def order_page():
    return "Order", 200


@router.route('/create_user')
def create_user():
    """
    WARNING: NEVER RUN THIS
    """
    user_resource.create_user("user1", "squizz")
    return "ok", 200



