from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import send_from_directory

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

# api.add_resource(HelloApiHandler, '/flask/hello')


app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://pxjvdkbmidsdcg:68047a03bdfcd39f0a9d0a5a5cf70048b6ba129974a5e072a2a760b2d956a497@ec2-44-198-80-194.compute-1.amazonaws.com:5432/d1n7a2n9qi5ipu"
db = SQLAlchemy(app)


def todo_serializer(todo):
    return {
        'id': todo.id,
        'spl': todo.spl,
        'skill': todo.skill,
        'task': todo.task,
        'cat': todo.cat,
        'start': todo.start,
        'end': todo.end,
        'status':todo.status
            }

def todo_task(todo):
    return todo.status

@app.route("/")
def serve():
    return send_from_directory(app.static_folder,'index.html')


@app.route('/home')
def home():
    return "home"

def getSkill(val):
    return jsonify([*map(todo_task, Todo.query.filter_by(id=val))])

# @app.route('/create')
# def create():
#     return "create"

@app.route('/api', methods=['GET'])
def index():
    return jsonify([*map(todo_serializer, Todo.query.all())])

@app.route('/create', methods=["POST"])
def create():
    # checkValue = jsonify([*map(todo_serializer, Todo.query.all())])
    # if checkValue == None:
    #     db.create_all()
    request_data = json.loads(request.data)
    added_todo = Todo()
    added_todo.spl = request_data['spl']
    added_todo.skill = request_data['skill']
    added_todo.task = request_data['task']
    added_todo.cat = request_data['cat']
    added_todo.start = request_data['start']
    added_todo.end = request_data['end']
    added_todo.status = request_data['status']
    #getSkillValues = getSkill(request_data['skill'])
    db.session.add(added_todo)
    db.session.commit()
    return {'201': 'task created successfully'}

@app.route('/change_status' , methods=["POST"])
def changeStatus():
    request_data = json.loads(request.data)
    admin = Todo.query.get(request_data['id'])
    admin.status = request_data['status']
    db.session.commit()
    return {"100": "Status Updated"}

@app.route('/api/<int:id>', methods=["POST"])
def delete(id):
    request_data = json.loads(request.data)
    Todo.query.filter_by(id=request_data["id"]).delete()

    db.session.commit()
    return request_data
    #return { '204': "Deleted Successfully"}

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spl = db.Column(db.Text, nullable=False)
    skill = db.Column(db.Text, nullable=False)
    task = db.Column(db.PickleType, nullable=False)
    cat = db.Column(db.Text, nullable=False)
    start = db.Column(db.Text, nullable=False)
    end = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)


    def __str__(self):
        return f'{self.id} {self.spl} {self.skill} {self.task} {self.cat} {self.start} {self.end} {self.status}'

    # if getSkillValues == None:
    #     db.session.add(added_todo)
    #     db.session.commit()
    #     return {'201': 'Skill created successfully'}

    # else:
    #     admin = Todo.query.filter_by(skill=request_data['skill']).first()
    #     admin.task = request_data['task'] +","+admin.task
    #     db.session.commit()
    #     return {'100': 'Task Added'}
    

# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///skill.db"
# db = SQLAlchemy(app)


# def todo_serializer(todo):
#     return {
#         'id': todo.id,
#         'skill': todo.skill,
#         'task': todo.task
#             }

# def todo_task(todo):
#     return todo.task
            

# # @app.route('/')
# # def hello_world():
# #     return "hello world"

# @app.route('/api', methods=['GET'])
# def index():
#     return jsonify([*map(todo_serializer, Todo.query.all())])
    
# @app.route('/api/create', methods=["POST"])
# def create():
#     request_data = json.loads(request.data)
#     added_todo = Todo()
#     added_todo.skill = request_data['skill']
#     added_todo.task = request_data['task']
#     #getSkillValues = getSkill(request_data['skill'])
#     db.session.add(added_todo)
#     db.session.commit()
#     return {'201': 'Task created successfully'}
#     # if getSkillValues == None:
#     #     db.session.add(added_todo)
#     #     db.session.commit()
#     #     return {'201': 'Skill created successfully'}

#     # else:
#     #     admin = Todo.query.filter_by(skill=request_data['skill']).first()
#     #     admin.task = request_data['task'] +","+admin.task
#     #     db.session.commit()
#     #     return {'100': 'Task Added'}
    

# def getSkill(val):
#     return jsonify([*map(todo_task, Todo.query.filter_by(skill=val))])

# @app.route('/api/<int:id>')
# def show(id):
#     return jsonify([*map(todo_serializer, Todo.query.filter_by(id=id))])

# @app.route('/api/<int:id>', methods=["POST"])
# def delete(id):
#     request_data = json.loads(request.data)
#     Todo.query.filter_by(id=request_data["id"]).delete()

#     db.session.commit()

#     return { '204': "Deleted Successfully"}



# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     skill = db.Column(db.Text, nullable=False)
#     task = db.Column(db.PickleType, nullable=False)


#     def __str__(self):
#         return f'{self.id} {self.skill} {self.task}'


db.create_all()
todo_skill = Todo()
todo_skill.spl = "Frontend Development"
todo_skill.skill = "ReactJS"
todo_skill.task = "redux"
todo_skill.cat = "Theory"
todo_skill.start = "27/8/2021"
todo_skill.end = "27/9/2021"
todo_skill.status = "Todo"
db.session.add(todo_skill)
db.session.commit()



if __name__ == "__main__":
    app.run(debug=True)

# print(Todo.query.get(5))
# admin = Todo.query.get(5)
# admin.status = "Done"
# db.session.commit()
# print(admin.status)