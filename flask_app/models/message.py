# ==================
# STANDARD IMPORTS
# ==================
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

# ==================
# REDIRECT ATTRIBUTES FOR FLASH MESSAGES
# ==================
from flask import flash

# ==================
# REGEX IMPORTS
# ==================
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# ==================
# BCRYPT IMPORTS
# ==================
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ==================
# MESSAGE MODEL
# ==================
class Message: 
    def __init__(self, data):
        self.id = data['id']
        self.subject = data['subject']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # ==================
    # VALIDATIONS
    # ==================
    @staticmethod
    def validate_message(data):
        is_valid = True
        if len(data['subject']) < 3:
            flash("Subject must be at least 3 characters long!")
            is_valid = False
        if len(data['content']) < 3:
            flash("Content must be at least 3 characters long!")
            is_valid = False
        return is_valid

    # ==================
    # GET ALL MESSAGES
    # ==================
    @classmethod
    def get_all_mesages(cls):
        query = "SELECT * FROM messages;"
        results = connectToMySQL('chatter').query_db(query)
        for i in results:
            print(i)
        return results
    

    # ==================
    # SAVE/CREATE METHOD
    # ==================
    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (subject, content, user_id, created_at, updated_at) VALUES (%(subject)s, %(content)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL("chatter").query_db(query, data)
        