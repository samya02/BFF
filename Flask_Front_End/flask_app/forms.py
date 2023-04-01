from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_app.models import User
from flask_login import current_user
import string
# import email_validator
# from flask_pagedown.fields import PageDownField


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Name"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    profile_pic = FileField('Your Profile Photo')
    submit = SubmitField('Update Account details')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            
class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update password')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UploadImgForm(FlaskForm):
    pic = FileField('Upload Img here')
    submit = SubmitField('Check copyright')

class Add_Legal_Advisor(FlaskForm):
    pic = FileField('Your Profile Photo')
    profile = StringField('LinkedIn Profile Link',
                        validators=[DataRequired()])
    description = StringField('Job Description',
                        validators=[DataRequired()])
    city = StringField('City',
                        validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    country = StringField('Country',
                        validators=[DataRequired()])
    role = StringField('Role (Legal Advisor)',
                        validators=[DataRequired()])
    awards = IntegerField('Awards',
                        validators=[DataRequired()])
    cases = IntegerField('Cases',
                        validators=[DataRequired()])
    advised = IntegerField('Advised',
                        validators=[DataRequired()])
    union = IntegerField('Union',
                        validators=[DataRequired()])
    year = IntegerField('Year of Experience',
                        validators=[DataRequired()])
    submit = SubmitField('Submit Application')

class Brand_Name(FlaskForm):
    input = StringField('Input a phrase regarding your startup',
                        validators=[DataRequired()])
    submit = SubmitField('Generate Brand Name')

class CheckImgForm(FlaskForm):
    pic = FileField('Upload Img here')
    submit = SubmitField('Check Img Copyright Status')

class CheckMP4Form(FlaskForm):
    input = StringField('Input movie name',
                        validators=[DataRequired()])
    submit = SubmitField('Check movie, generate URLs')

class CheckMP3Form(FlaskForm):
    input = StringField('Input movie name',
                        validators=[DataRequired()])
    submit = SubmitField('Check movie, generate URLs')