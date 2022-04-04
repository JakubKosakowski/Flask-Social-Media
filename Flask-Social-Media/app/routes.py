from app import app, db, bcrypt
from flask import render_template, redirect
from flask import url_for, flash
from app.moduls import User
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
@login_required
def home_page():
    return render_template('home.html')

@app.route('/link')
@login_required
def link_page():
    return render_template('link.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              born_date=form.born_date.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are  now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register_page.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and bcrypt.check_password_hash(attempted_user.password_hash, form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again!', category='danger')

    return render_template('login_page.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))

@app.route('/user')
@login_required
def user_page():
    return render_template('user_page.html')