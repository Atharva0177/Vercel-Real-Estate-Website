from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String(50), default='Available')
    featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('PropertyImage', backref='property', lazy=True, cascade='all, delete-orphan')
    videos = db.relationship('PropertyVideo', backref='property', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('PropertyDocument', backref='property', lazy=True, cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='property', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='property', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Property {self.title}>'

class PropertyImage(db.Model):
    __tablename__ = 'property_images'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PropertyImage {self.id}>'

class PropertyVideo(db.Model):
    __tablename__ = 'property_videos'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)
    video_type = db.Column(db.String(50), default='youtube')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PropertyVideo {self.id}>'

class PropertyDocument(db.Model):
    __tablename__ = 'property_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    document_name = db.Column(db.String(200), nullable=False)
    document_url = db.Column(db.String(500), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # PDF, DOC, etc.
    file_size = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PropertyDocument {self.document_name}>'

class Enquiry(db.Model):
    __tablename__ = 'enquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='New')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    property = db.relationship('Property', backref='enquiries')
    
    def __repr__(self):
        return f'<Enquiry {self.name} - {self.email}>'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('PropertyAlert', backref='user', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Favorite User:{self.user_id} Property:{self.property_id}>'

class PropertyAlert(db.Model):
    __tablename__ = 'property_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # new_property, price_drop, etc.
    property_type = db.Column(db.String(100))
    min_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    location = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PropertyAlert {self.alert_type} for User:{self.user_id}>'

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    booking_time = db.Column(db.String(20), nullable=False)
    visitor_name = db.Column(db.String(100), nullable=False)
    visitor_email = db.Column(db.String(120), nullable=False)
    visitor_phone = db.Column(db.String(20), nullable=False)
    number_of_visitors = db.Column(db.Integer, default=1)
    message = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')  # Pending, Confirmed, Cancelled, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.visitor_name}>'

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_type = db.Column(db.String(50))  # admin, user, guest
    user_id = db.Column(db.Integer)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ActivityLog {self.action}>'