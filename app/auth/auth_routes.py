import sqlalchemy as sa
from flask import (current_app, flash, redirect, render_template,
                   url_for)
from flask_login import current_user, login_user, logout_user

from app import db
from app.auth.auth_forms import LoginForm, RegistrationForm
from app.models import User
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('Login route called')
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # if the user is already logged in, redirect to the index page
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    # create a new instance of the RegistrationForm
    form = RegistrationForm()
    # if the form is submitted
    if form.validate_on_submit():
        # create a new user
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        # set the password for the user
        user.set_password(form.password.data)
        # add the user to the database
        db.session.add(user)
        db.session.commit()
        # flash a message to the user
        flash('Congratulations, you are now a registered user!')
        # redirect the user to the login page
        return redirect(url_for('auth.login'))
    # render the register template
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.index'))

from app.auth import auth_routes  # noqa
