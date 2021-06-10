from flask import Flask , render_template , request,url_for , redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///stack.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100))
    question = db.relationship('Question' , backref = 'user')
    answer1 = db.relationship('Answer' , backref = 'user')

    def __repr__(self):
        return self.name

class Question(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    que = db.Column(db.String(120))
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    answer = db.relationship('Answer' , backref = 'ques')

    def __repr__(self):
        return f'{self.que}'

class Answer(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    ans = db.Column(db.String(120))
    que_id = db.Column(db.Integer , db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.ans}'

@app.route('/stack')
def stack_view():
    ans = Answer.query.all()
    que = Question.query.all()
    data = zip(que , ans)

    return render_template('stack.html',ans = ans , que = que , data = data)

@app.route('/addans/<int:que_id>', methods = ['GET' , 'POST'])
def addans_view(que_id):
    user = User.query.all()
    que = Question.query.get(que_id)
    u_user = request.form.get('user')
    f_user = User.query.filter_by(name = u_user).first()
    if request.method == 'POST':
        ans = Answer(ans = request.form.get('answer'), ques = que , user = f_user)
        db.session.add(ans)
        db.session.commit()
        return redirect('/stack')

    return render_template('create_ans.html',user = user , que = que)


@app.route('/addque' , methods = ['GET' , 'POST'])
def addque_view():
    user = User.query.all()
    que = Question.query.get('ques')
    u_user = request.form.get('user')
    f_user = User.query.filter_by(name = u_user).first()
    if request.method == 'POST':
            que = Question(que = request.form.get('question'), user = f_user)
            db.session.add(que)
            db.session.commit()
            return redirect('/stack')

    return render_template('create_que.html' , user = user , ques = que )


@app.route('/update/<int:id>' , methods = ['GET' , 'POST'])
def update_que_view(id):
    obj = Question.query.get(id)
    if request.method == "POST":

        obj.que = request.form.get("question")


        try:
            db.session.commit()
            return redirect('/stack')

        except:
            return 'There is problem while updating object to the database'

    return render_template("update.html" , obj = obj)

@app.route('/delete/<int:id>')
def delete_student_view(id):
    que = Question.query.get(id)

    try:
        db.session.delete(que)
        db.session.commit()

    except:
        return 'There is problem while deleting object from the database'

    return redirect('/stack')

@app.route('/update_ans/<int:id>' , methods = ['GET' , 'POST'])
def update_ans_view(id):
    obj = Answer.query.get(id)
    if request.method == "POST":

        obj.ans = request.form.get("answer")


        try:
            db.session.commit()
            return redirect('/stack')

        except:
            return 'There is problem while updating object to the database'

    return render_template("update_ans.html" , obj = obj)


@app.route('/delete_ans/<int:id>')
def delete_ans_view(id):
    ans = Answer.query.get(id)

    try:
        db.session.delete(ans)
        db.session.commit()

    except:
        return 'There is problem while deleting object from the database'

    return redirect('/stack')


@app.route("/relation")
def relarionship_view():
    langs = Language.query.all()
    return render_template("relationship.html", langs = langs)

@app.route('/search', methods = ['GET','POST'])
def search_view():
    print(request.form)
    if request.method == "POST":
        que = request.form.get('search')
        quest = Question.query.filter_by(que = que).first()
        print(quest.answer)
        ans = quest.answer

        return render_template('search.html', quest = quest,ans = ans)

    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug = True)
