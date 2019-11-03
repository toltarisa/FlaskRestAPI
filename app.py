from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, title, description):
        self.title = title
        self.description = description


class ToDoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')


todo_schema = ToDoSchema()
todos_schema = ToDoSchema(many=True)


@app.route('/todo/add', methods=['POST'])
def create_todo():
    title = request.json['title']
    description = request.json['description']

    todo = ToDo(title, description)
    db.session.add(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)


@app.route('/todos', methods=['GET'])
def get_all_todos():
    todos = ToDo.query.all()
    response = todos_schema.dump(todos)
    return jsonify(response)


@app.route('/todos/<id>', methods=['GET'])
def get_todo(id):
    todo = ToDo.query.get(id)
    return todo_schema.jsonify(todo)


@app.route('/todo/update/<id>', methods=['PUT'])
def update_todo(id):
    todo = ToDo.query.get(id)

    title = request.json['title']
    description = request.json['description']

    todo.title = title
    todo.description = description

    db.session.commit()
    return todo_schema.jsonify(todo)


@app.route('/todo/delete/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = ToDo.query.get(id)
    db.session.delete(todo)
    return jsonify({'message': 'The todo of id: '+id+' is deleted'})


if __name__ == '__main__':
    app.run(debug=True)
