from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Regexp, EqualTo, Email
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField()
    submit = SubmitField('登陆')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能为字母、数字、下划线')])
    password = PasswordField('密码', validators=[Required(), EqualTo('password_confirm', message='密码必须相等')])
    password_confirm = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')
