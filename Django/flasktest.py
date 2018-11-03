from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    GetBack0 = '<link rel="shortcut icon" href="{{ url_for("static", filename="favicon.ico") }}">'
    GetBack1 = '<form><select name="cars"><option value="volvo">Volvo</option><option value="saab">Saab</option><option value="fiat" selected="selected">Fiat</option><option value="audi">Audi</option></select></form>'
    GetBack2 = '<select>  <option value ="volvo">Volvo</option>  <option value ="saab">Saab</option><option value="opel">Opel</option><option value="audi">Audi</option></select>'
    GetBack3 = '<button type="button">Click Me!</button>'
    return GetBack1 + GetBack2 + GetBack3 + GetBack0


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
       <p><input name="username"></p>
       <p><input name="password" type="password"></p>
       <p align="right"><button type="submit">Sign In</button></p>
       </form>'''


@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    return hello_world()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
