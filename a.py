from flask import Flask,redirect,request ,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class Grade(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(64))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey(Grade.id))

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('nm')
        password = request.form.get('paw')
        u1 = Student.query.filter(Student.name==name,Student.password==password).first()
        if u1:
            return redirect(url_for('a'))
        else:
            return '登录失败！！'

@app.route('/index/',methods=['GET','POST'],endpoint='a')
def index():
    if request.method == 'GET':
        gg = Grade.query.all()
        ss = Student.query.all()
        return render_template('index.html',gg = gg, ss=ss)
    else:
        return render_template('index.html')

@app.route('/add_l/',methods=['GET','POST'])
def add_l():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        classname = request.form.get('ca')
        name = request.form.get('nm')
        email = request.form.get('em')
        password = request.form.get('paw')
        u1 = Grade.query.filter(Grade.name==classname).first()
        if u1:
            u2 = Student(name=name,email=email,password=password,role_id=u1.id)
            db.session.add(u2)
            db.session.commit()
            return redirect(url_for('a'))
        else:
            u3 = Grade(name=classname)
            db.session.add(u3)
            db.session.commit()
            u4 = Student(name=name, email=email, password=password, role_id=u3.id)
            db.session.add(u4)
            db.session.commit()
            return redirect(url_for('a'))

@app.route('/delete_l/<id>',methods=['GET','POST'])
def delete_l(id):
    u5 = Student.query.filter(Student.id == id).first()
    if u5:
        db.session.delete(u5)
        db.session.commit()
        return redirect(url_for('a'))
    else:
        return redirect(url_for('a'))


@app.route('/update_l/<a_id><b_id>',methods=['GET','POST'])
def update_l(a_id,b_id):
    g1 = Grade.query.filter(Grade.id == b_id).first()
    s1 = Student.query.filter(Student.id == a_id).first()
    if request.method == 'GET':
        return render_template('update.html',s1=s1,g1=g1)
    else:
        classname = request.form.get('ca')
        name = request.form.get('nm')
        email = request.form.get('em')
        password = request.form.get('paw')
        if classname == Grade.name:
            pass
        else:
            g1.name = classname
        if name == None:
            pass
        else:
            s1.name = name
        if email == None:
            pass
        else:
            s1.email = email
        if password == None:
            pass
        else:
            s1.password = password
        db.session.add_all([s1,g1])
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/paw_l/<id>',methods=['GET','POST'])
def paw_l(id):
    s1 = Student.query.filter(Student.id == id).first()
    if request.method == 'GET':
        return render_template('paw.html')
    else:
        paw1 = request.form.get('paw1')
        paw2 = request.form.get('paw2')
        paw3 = request.form.get('paw3')
        u1 = Student.query.filter(Student.password == paw1).first()
        if u1 and paw2 == paw3:
            s1.password = paw2
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('paw.html')



if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    s1 = Grade(name="一班")
    s2 = Grade(name="二班")
    s3 = Grade(name="三班")
    db.session.add_all([s1, s2, s3])
    db.session.commit()

    s4 = Student(name="谢一", password="1262115", email="448995656@163.com", role_id=s1.id)
    s5 = Student(name="谢二", password="1515336", email="44899565@163.com", role_id=s2.id)
    s6 = Student(name="张三", password="5157162", email="448995165@163.com", role_id=s3.id)
    s7 = Student(name="李四", password="5145162", email="448979565@163.com", role_id=s2.id)
    s8 = Student(name="王五", password="5151262", email="448929565@163.com", role_id=s3.id)
    db.session.add_all([s4, s5, s6, s7, s8])
    db.session.commit()
    app.run(debug=True)