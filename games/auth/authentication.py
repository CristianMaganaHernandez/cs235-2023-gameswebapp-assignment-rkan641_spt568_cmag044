from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from password_validator import PasswordValidator
from functools import wraps

from games.auth import services
import games.adapters.repository as repo


authentication_blueprint = Blueprint('auth_bp', __name__, url_prefix="/authentication")


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def user_register():
    form = RegistrationForm(request.form)
    user_name_not_unique = None

    if form.validate_on_submit():
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)
            flash('Thanks for registering')
            return redirect(url_for('auth_bp.user_login'))

        except services.NameNotUniqueException:
            flash('This username is already taken')
            user_name_not_unique = 'That user name is already taken - please supply another'

    return render_template(
        'auth/user_register.html',
        form=form,
        user_name_error_message=user_name_not_unique
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm(request.form)
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    if form.validate_on_submit():

        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            user_name_not_recognised = 'Username not recognised'

        except services.AuthenticationException:
            # Authentication failed
            password_does_not_match_user_name = 'Password does not match supplied user name - please check and try again'

    return render_template(
        'auth/user_login.html',
        form=form,
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
    )


@authentication_blueprint.route('/logout', methods=['GET', 'POST'])
def user_logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('auth_bp.user_login'))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 4 characters, and contain an upper case letter, \
                        a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(4) \
            .has().digits() \
            .has().uppercase() \
            .has().lowercase()

        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        [
            DataRequired(message='Your username is required'),
            Length(min=4, max=25,message='Your username is too short')
        ]
    )

    # email = StringField('Email', [
    #     DataRequired(message="Your email is required")
    # ])

    password = PasswordField(
        'New Password',
        [
            DataRequired(message='Your password is required'),
            Length(min=4, max=25, message='Your password is too short'),
            PasswordValid(),
            EqualTo('confirm_password', message='Passwords must match')
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        [
            DataRequired(message='Repeat password'),
        ]
    )

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        [
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired()
        ]
    )

    submit = SubmitField('Login')
