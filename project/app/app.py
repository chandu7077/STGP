from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import json
import os
from flask_cors import CORS
UPLOAD_FOLDER = 'storage/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    name=db.Column(db.String, primary_key = True)
    style=db.Column(db.Integer)

    def __init__(self,name,style):
        self.name=name
        self.style=style
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if request.method=="POST":
        dic={}
        dic["upload successful GO BACK"]="l"
        uploaded_files = request.files.getlist("images")
        for i,file in zip(range(1,len(uploaded_files)+1),uploaded_files):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],request.form["username"]+str(i)))
        return json.dumps(dic)
@app.route("/style",methods=["POST","GET"])
def style():
    if request.method=="POST":
        data=request.json
        name,style=data["name"],data["index"]
        user=User(name,style)
        db.session.add(user)
        db.session.commit()
        return render_template("view.html")
if __name__ == '__main__':
    db.create_all()
    app.run()
