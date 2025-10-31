#Codded by Ahmed Hatem For The ITI_Project

from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.mission}>"



@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = User.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks_page'))

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        task = request.form.get('Task')
        if task:
            new_task = User(mission=task)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('tasks_page'))
    return render_template('home.html')

@app.route('/tasks')
def tasks_page():
    tasks = User.query.all()
    return render_template('Tasks_Page.html', tasks=tasks)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
