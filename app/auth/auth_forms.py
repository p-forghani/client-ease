from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

# Uncomment this import for production
# from flask import current_app
# import re
# from wtforms import ValidationError

# Uncomment This function for production
# def validate_password(form, field):
#     min_length = current_app.config.get('USER_PASSWORD_LENGTH', 8)

#     if len(field.data) < min_length:
#         raise ValidationError(
#             f'Password must be at least {min_length} characters long.'
#         )

#     if not re.search(r'[A-Z]', field.data) or \
#        not re.search(r'[a-z]', field.data):
#         raise ValidationError(
#             'Password must contain both uppercase and lowercase characters.'
# )


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Reset Password')
