# ==================
# STANDARD IMPORTS
# ==================
import re
from flask_app import app
from flask import render_template, request, redirect, session

# ==================
# MODEL IMPORTS
# ==================
from flask_app.models.message import Message

# ==================
# BCRYPT IMPORTS
# ==================
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ==================
# REDIRECT ATTRIBUTES FOR FLASH MESSAGES
# ==================
from flask import flash



# ==================
# CREATE MESSAGE ROUTE
# ==================

# POST
@app.route("/chatter/create-message", methods=['POST'])
def new_message():

    # Validating info
    if not Message.validate_message(request.form):
        return redirect('/chatter/dashboard')

    # pass back data
    data = {
        "subject" : request.form["subject"],
        "content" : request.form["content"],
        "user_id" : request.form["user_id"]
    }
    Message.save(data)

    return redirect("/chatter/dashboard")