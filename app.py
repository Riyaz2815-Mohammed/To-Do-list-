from flask import Flask,render_template,request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss


app =Flask(__name__)
Scss(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tododb.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return f'<Task {self.id}'
    
    
@app.route('/') 
def home():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error:{e}")
            return f'Error:{e}'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)
    
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()  
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return "Error"
    else:
        return render_template("update.html", task=task)

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)








