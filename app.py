from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite3'
app.config['SECRET_KEY'] = "secret key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Employees(db.Model):
    employee_id = db.Column('employee_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer())
    position = db.Column(db.String())
    email = db.Column(db.String())

    def __init__(self, employee_id, name, age, position, email):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.position = position
        self.email = email

@app.route("/")
def landing_page():
    return'You Have Landed EEE Project-2022'

@app.route('/data')
def list_employees():
    return render_template('datalist.html', Employees = Employees.query.all())



@app.route('/data/create', methods=['GET', 'POST'])
def addEmployee():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['position'] or not request.form['age']  or not request.form['email']:
            flash('Please enter all the fields', 'error')
        else:
            employee = Employees(request.form['employee_id'],request.form['name'], request.form['age'],
                                 request.form['position'], request.form['email'])

            db.session.add(employee)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('list_employees'))
    return render_template('createpage.html')



@app.route('/update/<int:employee_id>', methods=['GET', 'POST'])
def update(employee_id):
    employees = Employees.query.filter_by(employee_id=employee_id).first()
    if request.method =='POST':
        employees.name = request.form['name']
        employees.age = request.form['age']
        employees.position =request.form['position']
        employees.email = request.form['email']
        db.session.commit()
        flash ("Employee Updated Successfully")
        return redirect (url_for('list_employees'))
    return render_template('update.html',employees = employees )



@app.route("/delete/<int:employee_id>")
def delete(employee_id):
    employee = Employees.query.filter_by(employee_id=employee_id).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/data")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)