import sqlalchemy as sa
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.auth import bp
from app.auth.auth_emails import (send_reset_password_email,
                                  send_verification_email)
from app.auth.auth_forms import (ForgotPasswordForm, LoginForm,
                                 RegistrationForm, ResetPasswordForm)
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', category='warning')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully', category='success')
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
            email=form.email.data,
        )
        # set the password for the user
        user.set_password(form.password.data)
        # add the user to the database
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        # flash a message to the user
        flash('Please check your email to verify your account')
        # redirect the user to the login page
        return redirect(url_for('auth.login'))
    # render the register template
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.index'))

from app.auth import auth_routes  # noqa


@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_reset_password_email(user)
        flash((
            'If the email address you provided is associated with an account, '
            'you will receive an email with instructions on how to reset your '
            'password.'
        ))
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    # if the user is already logged in, redirect to the index page
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # decode the token
    user = User.verify_token(token, token_type='reset_password')
    # if the token is invalid
    if user is None:
        flash('Invalid or expired token', category='warning')
        return redirect(url_for('auth.login'))

    # create a new instance of the ResetPasswordForm
    form = ResetPasswordForm()
    # if the form is submitted
    if form.validate_on_submit():
        # set the password for the user
        user.set_password(form.password.data)
        # add the user to the database
        db.session.commit()
        # flash a message to the user
        flash('Your password has been reset.')
        # redirect the user to the login page
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, token=token)


@bp.route('/verify_email/<token>')
def verify_email(token):
    user = User.verify_token(token, token_type='verify_email')
    if user is None:
        flash('Invalid or expired token', category='warning')
        return redirect(url_for('auth.login'))

    if user.email_verified is True:
        flash("Your email is verified", category='info')
        return redirect(url_for('auth.login'))

    user.email_verified = True
    db.session.commit()
    flash('Your email has been verified.', category='success')
    return redirect(url_for('auth.login'))
