from datetime import datetime
import json
import os

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileform
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    # get all the frame data and pass it to the index
    my_file_path = os.path.dirname(__file__)
    frame_data_dir = os.path.join(my_file_path, 'frame_data')
    frame_files = os.listdir(frame_data_dir)
    # print("characters: %s" % " ".join(frame_files))
    characters = [x.replace('.json', '') for x in frame_files]

    # for char in frame_files:
    #     data_file = os.path.join(frame_data_dir, char)
    #     # print("full path to file: %s" % " ".join(data_file))
    #     with open(data_file, 'r') as f:
    #         data = json.load(f) 
    #     character_name = char.replace('.json', "")
    #     entry = {
    #         "name": character_name,
    #         "data": data
    #     }
    #     characters.append(entry)
    # character_names = [x.replace(".json", "") for x in characters]
        
    # user = {'username': 'Oliver'}
    # posts = [
    #     {
    #         "author": {"username": "John"},
    #         "body": "Beautiful day in Portland"
    #     },
    #     {
    #         "author": {'username': 'Susan'},
    #         "body": 'The Avengers movie was so cool!'
    #     }
    # ]

    return render_template('index.html', title="Home Page", characters=characters)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are not a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post 1'},
        {'author': user, 'body': 'Test post 1'}
    ]
    return render_template('user.html', user=user, posts=posts)

def extract_data(char_name):
    # get all the frame data and pass it to the index
    my_file_path = os.path.dirname(__file__)
    frame_data_dir = os.path.join(my_file_path, 'frame_data')
    frame_files = os.listdir(frame_data_dir)
    characters = [x.replace('.json', '') for x in frame_files]
    
    for char in frame_files:
        data_file = os.path.join(frame_data_dir, char)
        # print("full path to file: %s" % " ".join(data_file))
        with open(data_file, 'r') as f:
            data = json.load(f) 
        character_name = char.replace('.json', "")
        entry = {
            "name": character_name,
            "data": data
        }
        characters.append(entry)
    char_data_file = os.path.join(frame_data_dir, "%s.json" % char_name)
    if os.path.exists(char_data_file):
        with open(char_data_file, 'r') as f:
            char_data = json.load(f)
        return char_data
    else:
        raise IOError("Could not find data for character: %s" % char_name)


@app.route('/character/<char_name>')
def character(char_name):
    # in reality this is where the data should be gathered rather than index
    # character = {
    #     "data": [
    #         {
    #             "": "",
    #             "input": "5P",
    #             "damage": "26",
    #             "guard": "All",
    #             "startup": "6",
    #             "active": "5",
    #             "recovery": "9",
    #             "onBlock": "-2",
    #             "onHit": "+1",
    #             "riscGain": "",
    #             "level": "1",
    #             "invuln": "none",
    #             "prorate": "80%"
    #         },
    #         {
    #             "": "",
    #             "input": "5K",
    #             "damage": "30",
    #             "guard": "All",
    #             "startup": "8",
    #             "active": "5",
    #             "recovery": "9",
    #             "onBlock": "-2",
    #             "onHit": "+1",
    #             "riscGain": "",
    #             "level": "1",
    #             "invuln": "none",
    #             "prorate": "90%"
    #         },
    #         {
    #             "": "",
    #             "input": "c.S",
    #             "damage": "42",
    #             "guard": "All",
    #             "startup": "7",
    #             "active": "7",
    #             "recovery": "14",
    #             "onBlock": "-2",
    #             "onHit": "+1",
    #             "riscGain": "",
    #             "level": "4",
    #             "invuln": "none",
    #             "prorate": "100%"
    #         }
    #     ],
    #     "name": char_name
    # }

    character = {
        "name": char_name,
        "data": extract_data(char_name)
    }
    return render_template('character.html', character=character)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileform(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data 
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.before_request 
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()