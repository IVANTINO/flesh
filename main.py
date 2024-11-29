from flask import Flask, render_template, request, flash
import sqlite3

con = sqlite3.connect('1.db', check_same_thread=False)
cursor = con.cursor()

app = Flask(__name__)


@app.route('/')
def web():
    return render_template('register.html')


@app.route('/save_register/', methods=['POST', 'GET'])
def save():
    last_name = request.form['last_name']
    name = request.form['name']
    patronymic = request.form['patronymic']
    gender = request.form['gender']
    email = request.form['email']
    username=request.form['username']
    password = request.form['password']
    cursor.execute(f"INSERT INTO users (last_name, name, patronymic, gender, email, username, password) VALUES (?,?,?,?,?,?,?)",
                   [last_name,name,patronymic,gender,email,username,password])
    con.commit()
    return 'ok'


@app.route('/login/', methods=['POST', 'GET'])
def obrabotka():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        return f'вы ввели логин {login} и пароль {password}'
    return 'Вы уже авторизироваись'


app.run(debug=True)
