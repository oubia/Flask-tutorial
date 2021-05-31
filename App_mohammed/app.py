from flask import Flask , render_template ,request ,redirect 
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db=SQLAlchemy(app)

class Items(db.Model):
     _id= db.Column("id", db.Integer,primary_key=True)
     designation = db.Column(db.String(100))
     quantity = db.Column(db.Integer)
     price=db.Column(db.Integer)
     # save a data

@app.route('/',methods=["POST","GET"])
def home():
    if request.method == "POST":
        form_name = request.form["form-name"]
        if form_name == "Add_form":
            db.create_all()
            qu = request.form["Quantity"]
            pr = request.form["Price"]
            items_instance = Items(designation=request.form["designation"],quantity=qu,price=pr)
            db.session.add(items_instance)
            db.session.commit()
        elif form_name == "Delete_form":
            Items.query.filter_by(designation=request.form["select_Delete_item"]).delete()
            db.session.commit()
        elif form_name == "Update_form":
            updated_item = Items.query.filter_by(designation=request.form['select_Update_item']).first()
            updated_item.quantity = int(request.form['Update_Quantity'])
            db.session.commit()
        return redirect('/items')
    return render_template('index.html',items = Items.query.all())

@app.route('/items')
def items():
    return render_template('items.html',data=Items.query.all())



# @app.route('/<name>')
# def user(name):
#     return F'{name} page'


if __name__ == '__main__':
    app.run(debug=True)