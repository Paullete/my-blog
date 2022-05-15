from . import auth
from app import db
from flask import render_template, request, flash, redirect, url_for
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('A user with this email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('Pick a username that is greater than 2 characters.', category='error')
        elif len(password1) < 7:
            flash('Use a stronger password that is more than 7 characters long.', category='error')
        elif password1 != password2:
            flash('Passwords did not match!!!', category='error')
        else:
            # create a new user if form is valid
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully!', category='success')
                login_user(user)
                return redirect(url_for('main.home'))
            else:
                flash('You entered wrong credentials', category='error')
        else:
            flash('No user with such details exists', category='error')

    return render_template('register.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))