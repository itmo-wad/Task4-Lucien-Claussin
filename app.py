from flask import Flask, render_template, send_from_directory, request, redirect
from pymongo import MongoClient


app = Flask(__name__)

app.secret_key = 'key'

logged = False

client = MongoClient('mongodb://localhost:27017')
db = client.wadDB

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form['user']
        password = request.form['pwd']
        result = db.info.find_one({"user": user})
        try:
            if password == result["password"]:
                logged = True
                return redirect('cabinet')
        except:
            e = "login or password wrong"
    else:
        return render_template('login.html')
    return render_template('login.html')

@app.route('/cabinet')
def cabinet():
    if logged == True:
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/img/<path:path>')
def index2(path):
    return send_from_directory('static/images', path)


@app.route('/static/<path:path>')
def index3(path):
    return app.send_static_file(path)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/createUser', methods=['POST'])
def createUser():
    email = request.form['email']
    pwd = request.form['pwd']
    user = request.form['user']
    db.info.insert({"user": user, "password": pwd, "email": email})
    return render_template('login.html',user = user)


if __name__ == '__main__':
    app.run(threaded=True, port='5000')
