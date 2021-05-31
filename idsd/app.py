
from enum import EnumMeta
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idsd.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIOS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)

def getId() :
    return len(User.query.all()) + 1
    


@app.route('/', methods =["POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        newUser = User(id = getId(), password = password, email = email)
        db.session.add(newUser)
        db.session.commit()
    
    
    return redirect('/')

@app.route('/', methods =["GET"])
def indexGet():
    comptes = User.query.all()
    return render_template('index.html', comptes = comptes)

@app.route('/delete', methods =["Post"])
def delete():
    if request.method == "POST":
        email = request.form.get("emaild")
        
        try:
            mail = User.query.filter_by(email = email).first()
            db.session.delete(mail)
            db.session.commit()
            return redirect('/')
        except:
            return "<h1> not exist </h1>"
        
@app.route('/update', methods =["Post"])
def update():
    
    if request.method == "POST":
        emailUpdated = request.form.get("mailUser")
        try:
            compte = User.query.filter_by(email = emailUpdated).first()

            compte.email = request.form.get("email")
            compte.password = request.form.get("password")
            
            db.session.commit()
            return redirect('/')
        except:
            return "<h1> not exist </h1>"

    

if __name__ == "__main__":
    app.run(debug=True)