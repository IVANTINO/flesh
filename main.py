from flask import Flask, render_template, request, flash
import sqlite3

con = sqlite3.connect('1.db', check_same_thread=False)

cursor = con.cursor()

app = Flask(__name__)


@app.route('/register/')
def web():
    return render_template('register.html')


@app.route('/main/', methods=['POST', 'GET'])
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
    return 'ok'


@app.route('/add/')
def add_page():
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
    return render_template('all_postss.html' posts=posts)


@app.route('/login/', methods=['POST', 'GET'])
def obrabotka():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        return f'вы ввели логин {login} и пароль {password}'
    return 'Вы уже авторизироваись'


app.run(debug=True)
