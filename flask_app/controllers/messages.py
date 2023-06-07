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
# SHOW ALL MESSAGES ROUTE
# ==================
@app.route("/chatter/allmessages")
def all_messages():
    if "user_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")
    
    user_id = session["user_id"]

    messages = Message.get_all_mesages()

    return render_template("allmessages.html", loggedin_userId = user_id, messages=messages)


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