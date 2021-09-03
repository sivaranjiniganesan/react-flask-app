from flask import Flask, jsonify, request, json, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import send_from_directory

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
# CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

# api.add_resource(HelloApiHandler, '/flask/hello')


app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://pxjvdkbmidsdcg:68047a03bdfcd39f0a9d0a5a5cf70048b6ba129974a5e072a2a760b2d956a497@ec2-44-198-80-194.compute-1.amazonaws.com:5432/d1n7a2n9qi5ipu"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
   
    def __int__(self, name, email):
        self.name = name
        self.email = email

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == 'POST':
        data = request.form
        name = data["name"]
        email = data["email"]
        new_data = User(name, email)
        db.session.add(new_data)
        db.session.commit()

        user_data = User.query.all()

        return render_template("index.html", user_data = user_data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)