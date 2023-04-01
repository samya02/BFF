from flask_app import app
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, request
from flask_app.models import User, Image, Legal_Advisor
from flask_app.forms import RegistrationForm, LoginForm, UploadImgForm, Add_Legal_Advisor, Brand_Name
from flask_login import login_user, current_user, logout_user, login_required
from flask_app import db, bcrypt, admin
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date
import uuid as uuid
import os

app.config['UPLOAD_FOLDER'] = '/Users/punerva/Desktop/BFF/Flask_Front_End/flask_app/static/img'

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/books', picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/')
@app.route('/home/')
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile', user_id=current_user.id))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadImgForm()
    if form.validate_on_submit():
        img = Image(
            user_id = current_user.id,
        )

        img.img = request.files['pic']
        # Grab Image Name
        pic_filename = secure_filename(img.img.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save that image
        file = request.files['pic']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
        # Change it to string to save to db
        img.img = pic_name

        db.session.add(img)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template("upload.html", form=form)

@app.route('/check')
def check():
    return render_template("check.html")

@app.route('/legal_advisor_apply', methods=['GET', 'POST'])
@login_required
def legal_advisor_apply():
    form = Add_Legal_Advisor() 
    if form.validate_on_submit():
        advisor = Legal_Advisor(
            name = current_user.name,
            email = current_user.email,
            phone = form.phone.data, 
            user = current_user.id, 
            profile = form.profile.data,
            description = form.description.data,
            city = form.city.data,
            country = form.country.data,
            role = form.role.data,
            awards = form.awards.data,
            cases = form.cases.data,
            advised = form.advised.data,
            union = form.union.data,
            year = form.year.data,
        )

        advisor.pic = request.files['pic']
        # Grab Image Name
        pic_filename = secure_filename(advisor.pic.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save that image
        file = request.files['pic']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
        # Change it to string to save to db
        advisor.pic = pic_name

        db.session.add(advisor)
        db.session.commit()
        return redirect(url_for('legal_issues'))
    return render_template("legal_advisor_apply.html", form=form)

@app.route('/legal_issues')
@login_required
def legal_issues():
    advisors = Legal_Advisor.query.all()
    return render_template("legal_issues.html", advisors=advisors)

@app.route("/brand_name", methods=['GET', 'POST'])
def brand_name():
    form = Brand_Name()
    if form.validate_on_submit():
        input = form.input.data
        import requests

        API_URL = "https://api-inference.huggingface.co/models/abdelhalim/Rec_Business_Names"
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
            
        output = query({
            "inputs": input,
        })
        print(output)
        output = output[0]["generated_text"]

        r = requests.post(
            "https://api.deepai.org/api/logo-generator",
            data={
                "text": input,
            },
            headers={'api-key': '9da50a62-c16d-4fe2-8629-1318b4675c1e'}
        )
        output_img = r.json()
        output_img = output_img['output_url']
        print(output_img)

        return render_template('brand_name.html', output=output, form=form, output_img=output_img)
    return render_template('brand_name.html', form=form)