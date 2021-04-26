from flask import Flask, render_template, redirect, request
from werkzeug.exceptions import abort
from project.data import db_session
from project.data.users import User
from project.data.book import Book
from project.data.avtor import Avtor
from project.data.genre import Genre
from project.forms.register import RegisterForm
import datetime
from project.forms.add_book import BooksForm
from project.forms.login import LoginForm
from flask import Flask, url_for, render_template, redirect
from flask_login import LoginManager, logout_user, login_required
from flask_login import login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main():
    print(1)
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    # print(jobs)
    #
    avtors = db_sess.query(Avtor).all()
    # print(us)
    return render_template("board_of_books.html", title='Книжная Полка', avtors=avtors, books=books)


@app.route('/account')
def account():
    print(1)
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    # print(jobs)
    #
    avtors = db_sess.query(Avtor).all()
    # print(us)
    return render_template("account.html", title='Книжная Полка', avtors=avtors, books=books)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addbook', methods=['GET', 'POST'])
@login_required
def add_books():
    db_sess = db_session.create_session()
    avt = [(x.surname, x.surname) for x in db_sess.query(Avtor).all()]
    g = [(x.title, x.title) for x in db_sess.query(Genre).all()]
    form = BooksForm()
    form.content1.choices = avt
    form.content5.choices = g
    if form.validate_on_submit():
        books = Book()
        a = form.content1.data
        print(a)
        b = db_sess.query(Avtor).filter(Avtor.surname == a).first()
        print(b)
        books.id_avt = b.id
        books.title = form.content2.data
        books.year = form.content3.data
        books.publish = form.content4.data
        a = form.content5.data
        b = db_sess.query(Genre).filter(Genre.title == a).first()
        books.id_genre = b.id
        if form.content6.data:  # Если получена фотография.
            fname = form.content6.data.filename
            print(fname)  # Получение имени.
            form.content6.data.save(
                "static/img/" + fname)
        books.name_foto = fname if form.content6.data else ""
        books.book_creater = current_user
        db_sess.merge(books)
        db_sess.commit()
        return redirect('/')
    return render_template('addbook.html', title='Добавление книги',
                           form=form)


# @app.route('/jobs/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_news(id):
#     form = WorksForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         print(current_user)
#         if current_user.id == 1:
#             jobs = db_sess.query(Jobs).first()
#         else:
#             jobs = db_sess.query(Jobs).filter(Jobs.id == id,
#                                               Jobs.user == current_user
#                                               ).first()
#         if jobs:
#             form.content2.data = jobs.team_leader
#             form.content1.data = jobs.job
#             form.content3.data = jobs.work_size
#             form.content4.data = jobs.collaborators
#             form.content5.data = jobs.is_finished
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         jobs = db_sess.query(Jobs).filter(Jobs.id == id,
#                                           Jobs.user == current_user
#                                           ).first()
#         if jobs:
#             jobs.team_leader = form.content2.data
#             jobs.job = form.content1.data
#             jobs.work_size = form.content3.data
#             jobs.collaborators = form.content4.data
#             jobs.is_finished = form.content5.data
#             #current_user.jobs.append(jobs)
#             db_sess.commit()
#             return redirect('/')
#         else:
#             abort(404)
#     print(4)
#     return render_template('addj.html',
#                            title='Редактирование новости',
#                            form=form
#                            )


# @app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def news_delete(id):
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).filter(Jobs.id == id,
#                                       Jobs.user == current_user
#                                       ).first()
#     if jobs:
#         db_sess.delete(jobs)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/')

if __name__ == '__main__':
    db_session.global_init("db/books.db")
    app.run(port=5000, host='127.0.0.1')
