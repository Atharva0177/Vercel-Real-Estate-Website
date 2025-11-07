from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, SelectField, BooleanField, PasswordField, MultipleFileField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])
    property_type = SelectField('Property Type', 
                               choices=[('Residential Plot', 'Residential Plot'),
                                       ('Commercial Plot', 'Commercial Plot'),
                                       ('Agricultural Land', 'Agricultural Land'),
                                       ('Industrial Plot', 'Industrial Plot')],
                               validators=[DataRequired()])
    price = FloatField('Price (₹)', validators=[DataRequired(), NumberRange(min=0)])
    area = FloatField('Area (sq ft)', validators=[DataRequired(), NumberRange(min=0)])
    location = StringField('Location/City', validators=[DataRequired(), Length(max=200)])
    address = TextAreaField('Full Address', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    status = SelectField('Status',
                        choices=[('Available', 'Available'),
                                ('Reserved', 'Reserved'),
                                ('Sold', 'Sold')],
                        validators=[DataRequired()])
    featured = BooleanField('Featured Property')
    images = MultipleFileField('Property Images', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    video_urls = TextAreaField('Video URLs (one per line, YouTube or Vimeo)', validators=[Optional()])
    documents = MultipleFileField('Property Documents', validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Documents only!')])

class EnquiryForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class UserRegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class UserLoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class PropertyAlertForm(FlaskForm):
    property_type = SelectField('Property Type', 
                               choices=[('', 'Any Type'),
                                       ('Residential Plot', 'Residential Plot'),
                                       ('Commercial Plot', 'Commercial Plot'),
                                       ('Agricultural Land', 'Agricultural Land'),
                                       ('Industrial Plot', 'Industrial Plot')],
                               validators=[Optional()])
    min_price = FloatField('Min Price (₹)', validators=[Optional(), NumberRange(min=0)])
    max_price = FloatField('Max Price (₹)', validators=[Optional(), NumberRange(min=0)])
    location = StringField('Location', validators=[Optional(), Length(max=200)])

class BookingForm(FlaskForm):
    booking_date = DateField('Visit Date', validators=[DataRequired()], format='%Y-%m-%d')
    booking_time = SelectField('Visit Time',
                              choices=[('09:00-10:00', '09:00 AM - 10:00 AM'),
                                      ('10:00-11:00', '10:00 AM - 11:00 AM'),
                                      ('11:00-12:00', '11:00 AM - 12:00 PM'),
                                      ('12:00-13:00', '12:00 PM - 01:00 PM'),
                                      ('14:00-15:00', '02:00 PM - 03:00 PM'),
                                      ('15:00-16:00', '03:00 PM - 04:00 PM'),
                                      ('16:00-17:00', '04:00 PM - 05:00 PM'),
                                      ('17:00-18:00', '05:00 PM - 06:00 PM')],
                              validators=[DataRequired()])
    visitor_name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    visitor_email = StringField('Email Address', validators=[DataRequired(), Email()])
    visitor_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    number_of_visitors = IntegerField('Number of Visitors', validators=[DataRequired(), NumberRange(min=1, max=10)], default=1)
    message = TextAreaField('Additional Notes', validators=[Optional(), Length(max=500)])



