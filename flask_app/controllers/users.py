# ==================
# STANDARD IMPORTS
# ==================
import re
from flask_app import app
from flask import render_template, request, redirect, session

# ==================
# MODEL IMPORTS
# ==================
from flask_app.models.user import User

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
# REDIRECT ROUTE
# ==================
@app.route("/")
def redirectIndex():
    return redirect("/register")




# ==================
# REGISTER ROUTE
# ==================
@app.route("/register")
def register():
    return render_template("register.html")

# ==================
# REGISTER POST ROUTE
# ==================
@app.route("/post-user", methods=['POST'])
def postUser():
    
    # Basic Validations
    if not User.validate_user(request.form):
        return redirect("/register")

    # Check if Email in DB
    verify_for_existing_email = {
        "email" : request.form["email"]
    }
    if User.get_by_email(verify_for_existing_email):
        flash("Email already exists. Please use different email to complete registration")
        return redirect('/register')

    # Hashing Password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    # Pass Data to Model
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "age" : request.form["age"],
        "password" : pw_hash
    }   

    new_user = User.save(data)

    # save user to session
    session["user_id"] = new_user
    print(session["user_id"])

    return redirect("/chatter/dashboard")



# ==================
# LOGIN ROUTE
# ==================
@app.route("/login")
def login():
    return render_template("login.html")


# ==================
# LOGIN POST ROUTE
# ==================
@app.route("/login-user", methods=["POST"])
def loginUser():

    # check for existing email
    data = {
        "email" : request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        print("email not in db")
        flash("Invalid Credentials")
        return redirect("/login")
    
    # check for matching password in db via unhashing and comparing to form
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        print("passwords do not match")
        flash("Invalid Credentials")
        return redirect("/login")

    print(user_in_db.id)
    session["user_id"] = user_in_db.id


    return redirect("/chatter/dashboard")


# ==================
# DASHBOARD ROUTE
# ==================
@app.route("/chatter/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")

    data= {
        "id" : session["user_id"]
    }
    user = User.get_one(data)

    return render_template("dashboard.html", user = user)


# ==================
# LOGOUT ROUTE
# ==================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
