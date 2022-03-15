from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), unique=True, nullable=False)
  content = db.Column(db.String(120), unique=True, nullable=False)
  status = db.Column(db.String(120), unique=True, nullable=False)

  def __init__(self, title, content, status="draft"):
    self.title = title
    self.content = content
    self.status = status

db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
  tasks = []
  for task in db.session.query(Task).all():
    del task.__dict__['_sa_instance_state']
    tasks.append(task.__dict__)
  return jsonify(tasks)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
  task = Task.query.get(id)
  del task.__dict__['_sa_instance_state']
  return jsonify(task.__dict__)

@app.route('/tasks', methods=['POST'])
def create_task():
  body = request.get_json()
  db.session.add(Task(body['title'], body['content'], body['status']))
  db.session.commit()
  return "task created"

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
  body = request.get_json()
  db.session.query(Task).filter_by(id=id).update(
    dict(title=body['title'], content=body['content'], status=body['status']))
  db.session.commit()
  return "task updated"

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
  db.session.query(Task).filter_by(id=id).delete()
  db.session.commit()
  return "task deleted"

@app.route('/tasks/done', methods=['PUT'])
def update_task_done(id):
  body = request.get_json()
  db.session.query(Task).filter_by(id=id).update(
    dict(status="done"))
  db.session.commit()
  return "task updated"

@app.route('/tasks/draft', methods=['PUT'])
def update_task_draft(id):
  body = request.get_json()
  db.session.query(Task).filter_by(id=id).update(
    dict(status="draft"))
  db.session.commit()
  return "task updated"