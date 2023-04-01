from flask_app import app
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, request
from flask_app.models import User, Image, Legal_Advisor
from flask_app.forms import RegistrationForm, LoginForm, UploadImgForm, Add_Legal_Advisor, Brand_Name, CheckImgForm, CheckMP4Form, CheckMP3Form
from flask_login import login_user, current_user, logout_user, login_required
from flask_app import db, bcrypt, admin
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date
import uuid as uuid
import os
import cv2
# from google.colab.patches import cv2_imshow
from skimage import io
import numpy as np
import operator
import matplotlib.pyplot as plt
from serpapi import GoogleSearch
from urllib.parse import urlparse

app.config['UPLOAD_FOLDER'] = '/Users/punerva/Desktop/BFF/Flask_Front_End/flask_app/static/img'
app.config['UPLOAD_FOLDER2'] = '/Users/punerva/Desktop/BFF/Flask_Front_End/flask_app'
dir_path = os.path.dirname(os.path.realpath('/Users/punerva/Desktop/BFF/Flask_Front_End/flask_app'))

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

@app.route('/checkMP4', methods=['GET', 'POST'])
def checkMP4():
    form1 = CheckMP4Form()
    output = ""
    if form1.validate_on_submit():
        movie = form1.input.data

        params = {
        "engine": "google",
        "q": movie,
        "api_key": "5d62dc181d5d979f00fe36e1afd6fead68ee57fef3ff6b21c9904fb3209da2bf"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]
        for i in range(len(organic_results)):
            print(organic_results[i]['link'])
        for i in range(len(organic_results)):
            link = organic_results[i]['link']
            domain = urlparse(link).netloc
            print(domain)
        #List of regsitered websites
        Registered = ['www.marvel.com', 'www.imdb.com', 'www.hotstar.com', 'www.netflix.com', 'www.primevideo.com']
        unregistered_searches = []
        for i in range(len(organic_results)):
            link = organic_results[i]['link']
            domain = urlparse(link).netloc
            if(domain not in Registered):
                unregistered_searches.append(organic_results[i])
        for i in range(len(unregistered_searches)):
            output += "<a target = '_blank' href = '" + unregistered_searches[i]['link'] + "'>" + unregistered_searches[i]['link'] +  "</a> <br>"
            print(unregistered_searches[i]['link'])
        return render_template("checkMP4.html", form1=form1, output = output)
    return render_template("checkMP4.html", form1=form1)

@app.route('/checkMP3', methods=['GET', 'POST'])
def checkMP3():
    form1 = CheckMP3Form()
    output = ""
    if form1.validate_on_submit():
        song = form1.input.data

        params = {
        "engine": "google",
        "q": song,
        "api_key": "5d62dc181d5d979f00fe36e1afd6fead68ee57fef3ff6b21c9904fb3209da2bf"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]

        for i in range(len(organic_results)):
            print(organic_results[i]['link'])

        for i in range(len(organic_results)):
            link = organic_results[i]['link']
            domain = urlparse(link).netloc
            print(domain)

        #List of regsitered websites
        Registered = ['www.jamendo.com', 'www.noisetrade.com', 'www.musopen.org', 'www.wynk.com', 'www.jiosaavn.com', 'www.gaana.com', 'www.applemusic.com']  
        unregistered_searches = []

        for i in range(len(organic_results)):
            link = organic_results[i]['link']
            domain = urlparse(link).netloc
            if(domain not in Registered):
                unregistered_searches.append(organic_results[i])      

        for i in range(len(unregistered_searches)):
            output += "<a target = '_blank' href = '" + unregistered_searches[i]['link'] + "'>" + unregistered_searches[i]['link'] +  "</a> <br>"
            print(unregistered_searches[i]['link'])
        return render_template("checkMP3.html", form1=form1, output = output)
    return render_template("checkMP3.html", form1=form1)

@app.route('/checkImg', methods=['GET', 'POST'])
def checkImg():
    tmp_img = ""
    form = CheckImgForm()
    if form.validate_on_submit():
        img = request.files['pic']
        # Grab Image Name
        pic_filename = secure_filename(img.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save that image
        file = request.files['pic']
        file.save(os.path.join(app.config['UPLOAD_FOLDER2'], pic_name))
        # Change it to string to save to db
        tmp_img += pic_name
        image_url = "https://cdn.britannica.com/24/189624-050-F3C5BAA9/Mona-Lisa-oil-wood-panel-Leonardo-da.jpg"
        
        params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": "5d62dc181d5d979f00fe36e1afd6fead68ee57fef3ff6b21c9904fb3209da2bf"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        visual_matches = results["visual_matches"]

        list_of_images = []
        for i in range(len(visual_matches)):
            image_link = visual_matches[i]['thumbnail']
            list_of_images.append(image_link)
        
        print("Total Matches Found are:", len(visual_matches))

        def img_preprocessing(test):
            img2 = io.imread(test)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            img2 = cv2.resize(img2, (240, 240))
            return img2
        
        def check_similarity(img1, img2):
            h, w = img1.shape
            diff = cv2.subtract(img1, img2)
            err = np.sum(diff**2)
            mse = err/(float(h*w))
            return mse
        
        image_path = os.path.join(dir_path, tmp_img)
        
        ori_img = cv2.imread(image_path, 1)
        print(ori_img)
        ori_img = cv2.cvtColor(ori_img, 1)
        ori_img = cv2.resize(ori_img, (240, 240))

        similarity_index = {}

        for i in range(len(visual_matches)):
            test_link = visual_matches[i]['thumbnail']
            test_img = img_preprocessing(test_link)
            mse = check_similarity(ori_img, test_img)
            similarity_index[i] = mse

        sorted_similarities = dict( sorted(similarity_index.items(), key=operator.itemgetter(1),reverse=True))
        highest_matching = []
        for key in sorted_similarities.keys():
            highest_matching.append(key)
            if(len(highest_matching) == 5):
                break
        print('The matches with most similarities are: ')
        for i in range(0, 5):
            print(visual_matches[highest_matching[i]]['link'])
        return render_template("checkImg.html", form=form)
    return render_template("checkImg.html", form=form)
    

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
            headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        )
        output_img = r.json()
        output_img = output_img['output_url']
        print(output_img)

        return render_template('brand_name.html', output=output, form=form, output_img=output_img)
    return render_template('brand_name.html', form=form)