from flask import Flask ,session, render_template ,redirect, request,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db=SQLAlchemy(app)


class Items(db.Model):
     _id= db.Column("id", db.Integer,primary_key=True)
     designation = db.Column(db.String(100))
     quantity = db.Column(db.Integer)
     price=db.Column(db.Integer)
     # save a data
     def __init__(self, designation,quantity,price):
         self.designation=designation
         self.quantity=quantity
         self.price=price
         

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        # session.permanent=True
        form_name = request.form['form-name']
        if form_name == 'Add_form':
            db.create_all()
            designation=request.form["designation"]
            quantity = request.form["Quantity"]
            price = request.form["Price"]
            session['designation'] =designation
            session['quantity'] =quantity
            session['price'] =price
            items_instance = Items(designation,quantity,price)
            db.session.add(items_instance)
            db.session.commit()
            print("hiii",session['designation'])
            return redirect(url_for('items'))


        elif form_name == 'Delete_form':
            Items.query.filter_by(designation=request.form["Delete_item"]).delete()
            db.session.commit()
            return redirect(url_for('items'))
            
        elif form_name == 'Update_form':
            update_item = Items.query.filter_by(designation=request.form["Update_item"]).first()
            update_item.quantity = int(request.form["Update_Quantity"])
            db.session.commit()
            return redirect(url_for('items'))

    else:
        return render_template('index.html',items=Items.query.all())

@app.route('/items', methods=['GET', 'POST'])
def items():
    if 'designation' in session:
        designation=session['designation']
        print('inside',designation)
        return render_template('items.html',items=Items.query.all())
    else:
        return render_template('index.html')

# @app.route('/<name>')
# def user(name):
#     return f'{name} page'


if __name__ == '__main__':
    app.run(debug=True)