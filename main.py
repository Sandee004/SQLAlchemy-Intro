from flask import Flask, redirect, render_template, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
#users is the name of the database table we wil, be creating
app.permanent_session_lifetime = timedelta(minutes=5)

#these are vital for it to run
db = SQLAlchemy(app)
with app.app_context():
#define models
    class users(db.Model):
        _id = db.Column("id", db.Integer, primary_key = True)
        name = db.Column(db.String(100))
        email = db.Column(db.String(100))
    
        def __init__(self, name, email):
            self.name = name
            self.email = email


    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route('/view')
    def view():
        return render_template("view.html", values=users.query.all())
    
    @app.route('/login', methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            session.permanent = True
            user = request.form["nm"]
            session["user"] = user
            found_user = users.query.filter_by(name=user).first()
            
            if found_user:
                #checks the database and sets session email as the email found in database
                session["email"] = found_user.email
            else:
                #if no email in database add it
                usr = users(user, None)
                db.session.add(usr)
                db.session.commit()
                
            flash("Login successful", "info")
            return redirect(url_for("user"))
        else:
            if "user" in session:
                flash("Already logged in", "info")
                return redirect(url_for("user"))
            return render_template("login.html")
    
    @app.route('/user', methods=["GET", "POST"])
    def user():
        email = None
        if "user" in session:
            user = session["user"]
    
            if request.method == "POST":
                email = request.form["email"]
                session["email"] = email
                found_user = users.query.filter_by().first()
                found_user.email = email
                db.session.commit()
                flash("Email saved", "info")
            else:
                if "email" in session:
                    email = session["email"]
            return render_template("user.html",  email = email)
        else:
            flash("You are not logged in")
            return redirect(url_for("login"))
    
    """@app.route('/user')
    def user():
        if "user" in session:
            user = session["user"]
            return render_template("user.html",  user=user)
        else:
            flash("You are not logged in")
            return redirect(url_for("login"))"""
    
    @app.route('/logout')
    def logout():
        flash("Logout successful", "info")
        session.pop("user", None)
        session.pop("email", None)
        
        return redirect(url_for("login"))

    """@app.route('/view/clear')
    def erase():
        session["user"] = user
        found_user = users.query.filter_by(name=user).delete()
        for user in found_user:
            user.delete()
            db.session.commit()
        return redirect(url_for('view'))
    
    ""@app.route('/<name>')
    def user(name):
        return f"Hello {name}"
    """
    
    if __name__ == "__main__":
        db.create_all()
        app.run(host='0.0.0.0', port=81, debug= True)
