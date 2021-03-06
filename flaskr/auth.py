import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        with db.cursor() as cursor:
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            else:
                cursor.execute(
                    'SELECT id FROM users WHERE username = %s', (username,)
                )
                user = cursor.fetchone()
                if user is not None:
                    error = f"User {username} is already registered."

            if error is None:
                cursor.execute(
                    'INSERT INTO users (username, password) VALUES (%s, %s)',
                    (username, generate_password_hash(password))
                )
                db.commit()
                return redirect(url_for('auth.login'))

            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE username = %s', (username,)
            )
            user = cursor.fetchone()

            if user is None:
                error = 'Incorrect username.'
            else:
                user_id, user_username, user_password = user
                if not check_password_hash(user_password, password):
                    error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user_id
                return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with get_db().cursor() as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE id = %s', (user_id,)
            )
            user = cursor.fetchone()
            user_id, user_username, user_password = user
            g.user = {
                "id": user_id,
                "username": user_username,
                "password": user_password,
            }


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
