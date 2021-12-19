from flask import Flask,jsonify,request,json
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=None
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80),nullable=False)
    def __str__(self):
        return f'{self.id} {self.content}'

def serializer(todo):
    return{
        'id':todo.id,
        'content':todo.content
    }

@app.route('/api')
def index():
    return jsonify( [*map(serializer, Todo.query.all())] )



@app.route('/addTodo', methods=['POST','GET'])
def addTodo():
    request_data=json.loads(request.data)
    todo = Todo(content=request_data['content'])
    db.session.add(todo)
    db.session.commit()
    return {'201':'todo created'}

@app.route('/item/<int:id>')
def show(id):
    return jsonify([*map(serializer, Todo.query.filter_by(id=id) )])



if __name__ == '__main__':
    app.run(debug=True)