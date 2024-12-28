from cachelib import FileSystemCache
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_session import Session
from datetime import timedelta
import sqlite3

con = sqlite3.connect('1.db', check_same_thread=False)
cursor = con.cursor()

app = Flask(__name__)
app.secret_key = '1234'
app.config['SESSION_TYPE'] = 'cachelib'
app.config['SESSION_CACHELIB'] = FileSystemCache(cache_dir='flask_session', threshold=500)
Session(app)




@app.route('/', methods=['POST', 'GET'])
def main():
    cursor.execute('SELECT * FROM posts')
    data = cursor.fetchall()
    return render_template('index.html',data=data)



@app.route('/register/')
def register_page():
    return render_template('register.html')

@app.route('/save_register/', methods=['POST', 'GET'])
def save():
    last_name = request.form['last_name']
    name = request.form['name']
    patronymic = request.form['patronymic']
    gender = request.form['gender']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    cursor.execute(
        f"INSERT INTO users (last_name, name, patronymic, gender, email, username, password) VALUES (?,?,?,?,?,?,?)",
        [last_name, name, patronymic, gender, email, username, password])
    con.commit()
    return render_template('login.html')

@app.route('/add/')
def add_page():
    if 'login' not in session:
        flash('Необходима авторизация', 'danger')
        return redirect(url_for('obrabotka'))
    return render_template('add.html')


@app.route('/upload/', methods=['POST', 'GET'])
def save_post():
    image = request.files.get('image')
    titel = request.form['title']
    file_name = f'static/uploads/{image.filename}'
    description = request.form['description']
    image.save(file_name)
    cursor.execute(f"INSERT INTO posts (titel, file_name, description) VALUES {titel, file_name, description}")
    con.commit()
    return 'ok'

@app.route('/all_posts/', methods=['POST', 'GET'])
def get_posts():
    posts=cursor.execute("SELECT file_name FROM posts")
    data = cursor.fetchall()
    return render_template('all_postss.html')


@app.route('/login/', methods=['POST', 'GET'])
def obrabotka():
    return render_template('login.html')

@app.route('/authorization/', methods=['POST'])
def authorization():
    login=request.form['username']
    password=request.form['password']
    cursor.execute('SELECT username, password FROM users WHERE username=(?)', [login])
    data=cursor.fetchall()
    if not data:
        flash('Неверный логин', 'danger')
        return redirect(url_for('obrabotka'))
    if password==data[0][1]:
        session['login']=True
        session['username']=login
        session.permanent=False
        app.permanent_session=timedelta(minutes=1)
        session.modified=True
        flash('Вы успешно авторизовались', 'success')
        return redirect(url_for('main'))
    flash('Неверный пароль', 'danger')
    return redirect(url_for('obrabotka'))
@app.route("/logout/")
def logout():
    session.clear()
    flash(':D','danger')
    return  redirect(url_for('main'))




app.run(debug=True)
