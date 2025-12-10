from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"


with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form.get('content', '').strip()

        if not task_content:
            # empty aa irundha ignore pannalaam
            return redirect(url_for('index'))

        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        # Incomplete first, then completed, then by date
        tasks = Todo.query.order_by(Todo.completed, Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form.get('content', '').strip()
        if not task.content:
            return redirect(url_for('index'))

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template("update.html", task=task)


@app.route("/toggle/<int:id>")
def toggle(id):
    """Mark task as done / not done."""
    task = Todo.query.get_or_404(id)
    try:
        task.completed = not task.completed
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True)
