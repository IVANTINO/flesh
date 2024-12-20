from flask import Flask, render_template, request, flash
import sqlite3

con = sqlite3.connect('1.db', check_same_thread=False)

cursor = con.cursor()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    cursor.execute('SELECT * FROM posts')
    data = cursor.fetchall()


    return render_template('index.html',data=data)



@app.route('/register/')
def web():
    titel=request.form['titel']
    image=request.form['image']
    description=request.form['description']
    cursor.execute(
        f"INSERT INTO posts (titel, image, description) VALUES (?,?,?)",
    [titel, image, description])



@app.route('/add/')
def add_page():

    return render_template('add.html')

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
    return render_template('main.html')





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
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        return f'вы ввели логин {login} и пароль {password}'
    return 'Вы уже авторизироваись'


app.run(debug=True)
