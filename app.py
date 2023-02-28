from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable = False)
    title = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"


with app.app_context():
    db.create_all()



@app.route("/",methods =['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        quest = Task(title = title,desc = desc)
        db.session.add(quest)
        db.session.commit()

    allQuests = Task.query.all()


    return render_template("index.html",allQuests=allQuests)


@app.route("/show")
def showAllQuests():
    allQuests = Task.query.all()
    print(allQuests)
    return '<h1>All Quests</h1>'


@app.route("/delete/<int:id>")
def deleteQuest(id):
    quest = Task.query.filter_by(id=id).first()
    db.session.delete(quest)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:id>",methods =['GET','POST'])
def updateQuest(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        quest = Task.query.filter_by(id=id).first()
        quest.title = title
        quest.desc = desc
        db.session.add(quest)
        db.session.commit()
        return redirect('/')
    
    quest = Task.query.filter_by(id=id).first()
    return render_template('update.html',quest=quest)

if __name__ == "__main__":
    app.run(debug=True,port=8080)
