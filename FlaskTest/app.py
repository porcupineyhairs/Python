from flask import Flask
from flask_bootstrap import Bootstrap
from Config import *

from flask import render_template, request, flash

# 导入tf扩展的表单类
from flask_wtf import FlaskForm

# 导 入自定义表单需要的字段
from wtforms import SubmitField, StringField, PasswordField, RadioField, SelectField

# 导入wtf扩展提供的表单验证
from wtforms.validators import DataRequired, EqualTo


hostIp = '0.0.0.0'
hostPort = 8099
hostInfo = hostIp + str(hostPort)

app = Flask(__name__)
app.secret_key = '1234567'
bootstrap = Bootstrap(app)

SetRoute(app=app, hostInfo=hostInfo)


def get_month():
	return [('201910', '2019-10'), ('201911', '2019-11')]


# 自定义表单类、文本字段、密码字段、提交按钮
# 使用WTF实现表单 需要自定义一个表单类
class LoginForm(FlaskForm):
	monthList = get_month()

	# StringField/PasswordField是区别文本框类型， 用户名/密码是指定label值， validators 就是指明要验证哪些项

	username = StringField('用户名:')
	password = PasswordField('密码:')
	password2 = PasswordField('确认密码:')
	submit = SubmitField('提交')

	monthSelect = SelectField('选择年月', choices=monthList, validators=[DataRequired()])


# 定义根路由视图函数，生成表单对象，获取表单数据，进行表单数据验证
@app.route('/form', methods=['GEt', 'POST'])
def login():
	# 由RegisterForm类生成一个表实例
	login_form = LoginForm()

	# login_form.monthSelect = SelectField('选择年月', choice=[('aa', 'aa'), ('bb', 'bb')], validators=[DataRequired()])
	
	# 逻辑处理
	if request.method == 'POST':
		
		# 获取请求的参数
		# username = request.form.get('username')
		# password = request.form.get('password')
		# password2 = request.form.get('password2')

		
		# 调用validation_on_submit方法，可以一次性执行完所有验证函数的逻辑
		# if login_form.validate_on_submit():
		# 	# 进入这里就表示所有的逻辑都验证成功
		# 	print(username)
		# 	return 'success'
		#
		# else:
		# 	# message = login_form.get('password2')[0]
		# 	# flash(message)
		# 	return '参数有误'

		monthSelect = request.form.get('monthSelect')

		print(monthSelect)
	
	# 把实例化后的register_form传入到页面wtf.html中
	return render_template('test1.html', form=login_form)


if __name__ == '__main__':
	app.run(host=hostIp, port=hostPort, debug=True, threaded=False)
