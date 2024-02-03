from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Todo(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(400),nullable=False)
    desc=db.Column(db.String(600),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.title}-{self.sno}"

@app.route('/',methods=['GET','POST'])
def hello():
    if request.method =='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('hello'))  

    
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todel= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todel)
    db.session.commit()
    alltodo=Todo.query.all()

    return redirect(url_for('hello'))  
    
@app.route("/update/<int:sno>",methods=['GET','POST'])
def updateInfo(sno):
     todel= Todo.query.filter_by(sno=sno).first()
     
     if request.method =='POST':

        title=request.form['titleUpdate']
        desc=request.form['descUpdate']
        todel= Todo.query.filter_by(sno=sno).first()

        todel.title=title
        todel.desc=desc
        db.session.add(todel)
        db.session.commit()
        return redirect(url_for('hello'))  
     
     return render_template('update.html',todo=todel)


if not os.path.exists('todo.db'):
    with app.app_context():
        db.create_all()

if __name__=='__main__':
    app.run(debug=True,port=7540)




