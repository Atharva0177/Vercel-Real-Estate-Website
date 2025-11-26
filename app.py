from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import zipfile
import io
from datetime import datetime, timedelta
from config import Config
from models import db, Property, PropertyImage, PropertyVideo, PropertyDocument, Enquiry, Admin, User, Favorite, PropertyAlert, Booking, ActivityLog
from forms import PropertyForm, EnquiryForm, LoginForm, UserRegistrationForm, UserLoginForm, PropertyAlertForm, BookingForm
from functools import wraps
from flask_mail import Mail
from helpers.notifications import send_email  # use send_email helper
try:
    import vercel_blob
except ImportError:
    vercel_blob = None  # Will use local storage if not available

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and mail
db.init_app(app)
mail = Mail(app)


# Make datetime and other utilities available to all templates
@app.context_processor
def inject_globals():
    return {
        'datetime': datetime,
        'now': datetime.now(),
        'timedelta': timedelta
    }

# Expose app config to templates (used for GOOGLE_MAPS_API_KEY checks)
@app.context_processor
def inject_config():
    return {'config': app.config}

# Create upload directories (Vercel read-only filesystem safe)
try:
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
except (OSError, PermissionError):
    pass  # Read-only filesystem on Vercel

# Login required decorators
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this feature.', 'warning')
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, subfolder='images'):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        # Try Vercel Blob first (for production)
        if vercel_blob and os.environ.get('BLOB_READ_WRITE_TOKEN'):
            try:
                file_content = file.read()
                blob_filename = f"{subfolder}/{filename}"
                response = vercel_blob.put(blob_filename, file_content, options={'access': 'public'})
                return response['url']
            except Exception as e:
                print(f"Vercel Blob upload failed: {e}")
                file.seek(0)  # Reset file pointer for fallback
        
        # Fallback to local storage (for development)
        try:
            target_dir = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
            os.makedirs(target_dir, exist_ok=True)
            filepath = os.path.join(target_dir, filename)
            file.save(filepath)
            return f'uploads/{subfolder}/{filename}'
        except (OSError, PermissionError):
            return None
    return None

def log_activity(action, description='', user_type='guest', user_id=None):
    """Local activity logger for convenience (separate from helper)."""
    try:
        log = ActivityLog(
            action=action,
            description=description,
            user_type=user_type,
            user_id=user_id,
            ip_address=request.remote_addr if request else None
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()

# Initialize database tables (for Vercel serverless - runs on module load)
with app.app_context():
    try:
        db.create_all()
        print("Database tables initialized")
    except Exception as e:
        print(f"Database initialization: {e}")

# PUBLIC ROUTES
@app.route('/')
def index():
    try:
        featured_properties = Property.query.filter_by(featured=True, status='Available').limit(9).all()
        recent_properties = Property.query.filter_by(status='Available').order_by(Property.created_at.desc()).limit(9).all()
        return render_template('index.html', featured=featured_properties, recent=recent_properties)
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"Error: {e}", 500

@app.route('/properties')
def properties():
    try:
        page = request.args.get('page', 1, type=int)
        property_type = request.args.get('type', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        location = request.args.get('location', '')
        sort_by = request.args.get('sort', 'recent')
        
        query = Property.query.filter_by(status='Available')
        
        if property_type:
            query = query.filter_by(property_type=property_type)
        if min_price is not None:
            query = query.filter(Property.price >= min_price)
        if max_price is not None:
            query = query.filter(Property.price <= max_price)
        if location:
            query = query.filter(Property.location.contains(location))
        
        if sort_by == 'price_low':
            query = query.order_by(Property.price.asc())
        elif sort_by == 'price_high':
            query = query.order_by(Property.price.desc())
        elif sort_by == 'area_low':
            query = query.order_by(Property.area.asc())
        elif sort_by == 'area_high':
            query = query.order_by(Property.area.desc())
        else:
            query = query.order_by(Property.created_at.desc())
        
        properties = query.paginate(page=page, per_page=app.config['PROPERTIES_PER_PAGE'], error_out=False)
        
        return render_template('properties.html', properties=properties)
    except Exception as e:
        print(f"Error in properties route: {e}")
        return f"Error: {e}", 500

@app.route('/property/<int:id>')
def property_detail(id):
    try:
        property = Property.query.get_or_404(id)
        
        # Increment views
        property.views += 1
        db.session.commit()
        
        # Check if favorited by current user
        is_favorited = False
        if 'user_id' in session:
            is_favorited = Favorite.query.filter_by(user_id=session['user_id'], property_id=id).first() is not None
        
        form = EnquiryForm()
        booking_form = BookingForm()
        related_properties = Property.query.filter(
            Property.id != id,
            Property.property_type == property.property_type,
            Property.status == 'Available'
        ).limit(3).all()
        
        log_activity('view_property', f'Viewed property: {property.title}', 
                     'user' if 'user_id' in session else 'guest',
                     session.get('user_id'))
        
        return render_template('property_detail.html', 
                               property=property, 
                               form=form, 
                               booking_form=booking_form,
                               related=related_properties,
                               is_favorited=is_favorited,
                               datetime=datetime)
    except Exception as e:
        print(f"Error in property_detail route: {e}")
        return f"Error: {e}", 500

# ENQUIRIES
@app.route('/enquiry', methods=['POST'])
def submit_enquiry():
    form = EnquiryForm()
    if form.validate_on_submit():
        enquiry = Enquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data,
            property_id=request.form.get('property_id', type=int)
        )
        db.session.add(enquiry)
        db.session.commit()

        log_activity('submit_enquiry', f'Enquiry from {form.name.data}', 'user')

        # Notify Admin (email)
        send_email(
            mail,
            subject=f"New Property Enquiry #{enquiry.id}",
            recipients=[app.config['MAIL_DEFAULT_SENDER']],
            body=f"""New enquiry received:

Name: {enquiry.name}
Email: {enquiry.email}
Phone: {enquiry.phone}
Property: {enquiry.property.title if enquiry.property else 'General'}
Message:
{enquiry.message}

Login to admin panel to respond.""",
            category='enquiry'
        )
        # Acknowledge User (email)
        send_email(
            mail,
            subject="We received your enquiry",
            recipients=[enquiry.email],
            body=f"Hi {enquiry.name},\n\nThank you for contacting Premium Estate. We will respond shortly.\n\nRegards,\nPremium Estate Team",
            category='enquiry'
        )

        flash('Thank you for your enquiry! We will contact you soon.', 'success')
        return redirect(request.referrer or url_for('index'))
    flash('Please fill all required fields correctly.', 'error')
    return redirect(request.referrer or url_for('index'))

@app.route('/contact')
def contact():
    form = EnquiryForm()
    return render_template('contact.html', form=form)

# USER AUTHENTICATION ROUTES
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))
    
    form = UserRegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('user_login'))
        
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        log_activity('user_register', f'New user registered: {user.email}', 'user', user.id)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('user_login'))
    
    return render_template('user/register.html', form=form)

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))
    
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            
            log_activity('user_login', f'User logged in: {user.email}', 'user', user.id)
            
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('user/login.html', form=form)

@app.route('/user/logout')
def user_logout():
    user_id = session.get('user_id')
    log_activity('user_logout', 'User logged out', 'user', user_id)
    
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/user/dashboard')
@user_login_required
def user_dashboard():
    user = User.query.get(session['user_id'])
    favorites = Favorite.query.filter_by(user_id=session['user_id']).all()
    alerts = PropertyAlert.query.filter_by(user_id=session['user_id']).all()
    bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.created_at.desc()).all()
    
    return render_template('user/dashboard.html', 
                           user=user, 
                           favorites=favorites, 
                           alerts=alerts,
                           bookings=bookings)

# FAVORITES ROUTES
@app.route('/favorite/toggle/<int:property_id>', methods=['POST'])
@user_login_required
def toggle_favorite(property_id):
    property = Property.query.get_or_404(property_id)
    favorite = Favorite.query.filter_by(user_id=session['user_id'], property_id=property_id).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        log_activity('remove_favorite', f'Removed favorite: {property.title}', 'user', session['user_id'])
        return jsonify({'status': 'removed', 'message': 'Removed from favorites'})
    else:
        favorite = Favorite(user_id=session['user_id'], property_id=property_id)
        db.session.add(favorite)
        db.session.commit()
        log_activity('add_favorite', f'Added favorite: {property.title}', 'user', session['user_id'])
        return jsonify({'status': 'added', 'message': 'Added to favorites'})

@app.route('/user/favorites')
@user_login_required
def user_favorites():
    favorites = Favorite.query.filter_by(user_id=session['user_id']).all()
    return render_template('user/favorites.html', favorites=favorites)

# PROPERTY ALERTS ROUTES
@app.route('/alert/create', methods=['GET', 'POST'])
@user_login_required
def create_alert():
    form = PropertyAlertForm()
    if form.validate_on_submit():
        alert = PropertyAlert(
            user_id=session['user_id'],
            alert_type='new_property',
            property_type=form.property_type.data,
            min_price=form.min_price.data,
            max_price=form.max_price.data,
            location=form.location.data
        )
        db.session.add(alert)
        db.session.commit()
        
        log_activity('create_alert', 'Created property alert', 'user', session['user_id'])
        
        flash('Alert created successfully! You will receive notifications for matching properties.', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('user/create_alert.html', form=form)

@app.route('/alert/delete/<int:alert_id>', methods=['POST'])
@user_login_required
def delete_alert(alert_id):
    alert = PropertyAlert.query.get_or_404(alert_id)
    if alert.user_id != session['user_id']:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('user_dashboard'))
    
    db.session.delete(alert)
    db.session.commit()
    
    log_activity('delete_alert', 'Deleted property alert', 'user', session['user_id'])
    
    flash('Alert deleted successfully.', 'success')
    return redirect(url_for('user_dashboard'))

def check_and_send_alerts(property):
    """Notify users whose alerts match the new property (email + activity)."""
    alerts = PropertyAlert.query.filter_by(is_active=True).all()
    for alert in alerts:
        match = True
        if alert.property_type and alert.property_type != property.property_type:
            match = False
        if alert.min_price and property.price < alert.min_price:
            match = False
        if alert.max_price and property.price > alert.max_price:
            match = False
        if alert.location and alert.location.lower() not in (property.location or '').lower():
            match = False

        if match:
            user = User.query.get(alert.user_id)
            if user and user.email:
                send_email(
                    mail,
                    subject="New property matches your alert",
                    recipients=[user.email],
                    body=f"""Hi {user.name},

A new property matches your alert:

Title: {property.title}
Type: {property.property_type}
Location: {property.location}
Area: {property.area} sq ft
Price: ₹{property.price:,.0f}

View: {url_for('property_detail', id=property.id, _external=True)}

You can manage alerts in your dashboard.
""",
                    category='alert'
                )
            log_activity('alert_triggered', f'Alert triggered for user {alert.user_id}: {property.title}', 'system')

# BOOKING ROUTES
@app.route('/booking/create/<int:property_id>', methods=['POST'])
@user_login_required
def create_booking(property_id):
    property = Property.query.get_or_404(property_id)
    form = BookingForm()
    
    if form.validate_on_submit():
        booking = Booking(
            user_id=session['user_id'],
            property_id=property_id,
            booking_date=form.booking_date.data,
            booking_time=form.booking_time.data,
            visitor_name=form.visitor_name.data,
            visitor_email=form.visitor_email.data,
            visitor_phone=form.visitor_phone.data,
            number_of_visitors=form.number_of_visitors.data,
            message=form.message.data
        )
        db.session.add(booking)
        db.session.commit()
        
        log_activity('create_booking', f'Booking for {property.title}', 'user', session['user_id'])

        # Email notifications
        # Admin
        send_email(
            mail,
            subject=f"New Site Visit Booking #{booking.id}",
            recipients=[app.config['MAIL_DEFAULT_SENDER']],
            body=f"""New site visit booked:

Visitor: {booking.visitor_name}
Email: {booking.visitor_email}
Phone: {booking.visitor_phone}
Property: {property.title}
Date: {booking.booking_date.strftime('%d %b %Y')}
Time Slot: {booking.booking_time}
Visitors: {booking.number_of_visitors}
Message: {booking.message or '(none)'}""",
            category='booking'
        )
        # User
        send_email(
            mail,
            subject="Your site visit booking is pending confirmation",
            recipients=[booking.visitor_email],
            body=f"Hi {booking.visitor_name},\n\nThanks for booking a site visit for '{property.title}' on {booking.booking_date.strftime('%d %b %Y')} at {booking.booking_time}. We will confirm soon.\n\nRegards,\nPremium Estate Team",
            category='booking'
        )
        
        flash('Site visit booked successfully! We will confirm shortly.', 'success')
        return redirect(url_for('property_detail', id=property_id))
    
    flash('Please fill all required fields correctly.', 'error')
    return redirect(url_for('property_detail', id=property_id))

@app.route('/booking/cancel/<int:booking_id>', methods=['POST'])
@user_login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != session['user_id']:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('user_dashboard'))
    
    booking.status = 'Cancelled'
    db.session.commit()
    
    log_activity('cancel_booking', f'Cancelled booking #{booking_id}', 'user', session['user_id'])

    # Notify user (self-notification optional)
    send_email(
        mail,
        subject=f"Booking #{booking.id} Cancelled",
        recipients=[booking.visitor_email],
        body=f"Hi {booking.visitor_name},\n\nYour booking for '{booking.property.title}' has been cancelled as requested.\n\nRegards,\nPremium Estate Team",
        category='booking'
    )
    
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('user_dashboard'))


# BULK DOCUMENT DOWNLOAD
@app.route('/property/<int:property_id>/documents/download-all')
def download_all_documents(property_id):
    """Bulk download all documents for a property as ZIP"""
    property = Property.query.get_or_404(property_id)
    
    if not property.documents:
        flash('No documents available for this property.', 'warning')
        return redirect(url_for('property_detail', id=property_id))
    
    # Create in-memory ZIP file (serverless-safe)
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for document in property.documents:
            file_path = os.path.join('static', document.document_url)
            if os.path.exists(file_path):
                zf.write(file_path, arcname=document.document_name)
    
    memory_file.seek(0)
    
    log_activity('download_all_documents', f'Downloaded all documents for property: {property.title}',
                 'user' if 'user_id' in session else 'guest',
                 session.get('user_id'))
    
    # Generate safe filename
    safe_title = "".join(c for c in property.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    download_name = f"{safe_title[:50]}_Documents.zip"
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=download_name
    )

# MAP VIEW ROUTES
@app.route('/map')
def map_view():
    """Interactive map view of all properties"""
    return render_template('map_view.html')

@app.route('/api/properties')
def api_properties():
    """JSON API endpoint for properties (used by map)"""
    try:
        # Get filter parameters
        property_type = request.args.get('type', '')
        max_price = request.args.get('max_price', type=float)
        status = request.args.get('status', 'Available')
        
        # Build query
        query = Property.query
        if status:
            query = query.filter_by(status=status)
        if property_type:
            query = query.filter_by(property_type=property_type)
        if max_price:
            query = query.filter(Property.price <= max_price)
        
        properties = query.all()
        
        # Convert to JSON-friendly format
        properties_data = []
        for prop in properties:
            # Get first image URL if available
            image_url = ''
            if prop.images:
                image_url = prop.images[0].image_url
            
            properties_data.append({
                'id': prop.id,
                'title': prop.title,
                'property_type': prop.property_type,
                'price': prop.price,
                'area': prop.area,
                'location': prop.location,
                'address': prop.address,
                'latitude': prop.latitude,
                'longitude': prop.longitude,
                'status': prop.status,
                'image_url': image_url
            })
        
        return jsonify(properties_data)
    except Exception as e:
        print(f"Error in API properties: {e}")
        return jsonify([]), 500

# COMPARISON ROUTE
@app.route('/compare')
def compare_properties():
    """Property comparison page"""
    return render_template('compare.html')

# SOCIAL SHARING ROUTES
@app.route('/share/<int:property_id>')
def share_property(property_id):
    property = Property.query.get_or_404(property_id)
    property.shares += 1
    db.session.commit()
    
    log_activity('share_property', f'Shared property: {property.title}')
    
    return jsonify({'success': True, 'shares': property.shares})

# DOCUMENT DOWNLOAD ROUTE
@app.route('/document/download/<int:doc_id>')
def download_document(doc_id):
    document = PropertyDocument.query.get_or_404(doc_id)
    file_path = os.path.join('static', document.document_url)
    
    log_activity('download_document', f'Downloaded: {document.document_name}',
                 'user' if 'user_id' in session else 'guest',
                 session.get('user_id'))
    
    return send_file(file_path, as_attachment=True, download_name=document.document_name)

# ADMIN ROUTES
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == app.config['ADMIN_USERNAME'] and form.password.data == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            session['admin_username'] = form.username.data
            
            log_activity('admin_login', 'Admin logged in', 'admin')
            
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    log_activity('admin_logout', 'Admin logged out', 'admin')
    
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Successfully logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_login_required
def admin_dashboard():
    try:
        # Statistics
        total_properties = Property.query.count()
        available_properties = Property.query.filter_by(status='Available').count()
        sold_properties = Property.query.filter_by(status='Sold').count()
        new_enquiries = Enquiry.query.filter_by(status='New').count()
        total_users = User.query.count()
        pending_bookings = Booking.query.filter_by(status='Pending').count()
        total_views = db.session.query(db.func.sum(Property.views)).scalar() or 0
        total_shares = db.session.query(db.func.sum(Property.shares)).scalar() or 0

        # Recent data
        recent_properties = Property.query.order_by(Property.created_at.desc()).limit(5).all()
        recent_enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).limit(5).all()
        recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
        recent_activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all()

        stats = {
            'total': total_properties,
            'available': available_properties,
            'sold': sold_properties,
            'enquiries': new_enquiries,
            'users': total_users,
            # Used on dashboard as "Pending Visits"
            'bookings': pending_bookings,
            'views': total_views,
            'shares': total_shares
        }

        return render_template(
            'admin/dashboard.html',
            stats=stats,
            properties=recent_properties,
            enquiries=recent_enquiries,
            bookings=recent_bookings,
            activities=recent_activities
        )
    except Exception as e:
        print(f"Error in admin_dashboard route: {e}")
        return f"Error: {e}", 500

# Optional: Admin quick test email trigger
@app.route('/admin/test-email')
@admin_login_required
def admin_test_email():
    ok = send_email(
        mail,
        subject="Test Email from Premium Estate Admin",
        recipients=[app.config['MAIL_DEFAULT_SENDER']],
        body="This is a test email generated from the admin panel."
    )
    flash("Test email sent." if ok else "Test email failed.", "success" if ok else "error")
    return redirect(url_for('admin_dashboard'))




@app.route('/admin/seed-database')
@admin_login_required
def admin_seed_database():
    try:
        # Sample properties data - 9 properties total
        properties_data = [
            {
                'title': 'Luxury Beachfront Villa Plot in Juhu',
                'description': 'Premium residential plot located in the heart of Juhu with stunning sea-facing views. Perfect for building your dream villa. The plot offers 270-degree ocean views and is surrounded by high-end amenities.',
                'property_type': 'Residential Plot',
                'price': 15000000,
                'area': 5000,
                'location': 'Mumbai',
                'address': 'Juhu Beach Road, Mumbai, Maharashtra 400049',
                'latitude': 19.0990,
                'longitude': 72.8258,
                'status': 'Available',
                'featured': True,
                'views': 245,
                'shares': 34
            },
            {
                'title': 'Prime Commercial Hub in BKC',
                'description': 'Exceptional commercial plot in Bandra Kurla Complex, Mumbai\'s premier business district. Ideal for constructing a modern office complex, retail space, or mixed-use development.',
                'property_type': 'Commercial Plot',
                'price': 25000000,
                'area': 8000,
                'location': 'Mumbai',
                'address': 'Bandra Kurla Complex, Mumbai, Maharashtra 400051',
                'latitude': 19.0626,
                'longitude': 72.8687,
                'status': 'Available',
                'featured': True,
                'views': 189,
                'shares': 28
            },
            {
                'title': 'Scenic Agricultural Land in Nashik Wine Valley',
                'description': 'Sprawling fertile agricultural land in the renowned Nashik wine region. Perfect for vineyards, organic farming, or agro-tourism ventures. Features natural water sources and rich soil.',
                'property_type': 'Agricultural Land',
                'price': 3500000,
                'area': 10000,
                'location': 'Nashik',
                'address': 'Nashik-Pune Road, Nashik, Maharashtra 422009',
                'latitude': 19.9975,
                'longitude': 73.7898,
                'status': 'Available',
                'featured': True,
                'views': 156,
                'shares': 19
            },
            {
                'title': 'Lakefront Villa Plot in Powai',
                'description': 'Exclusive residential plot with stunning Powai Lake views. Located in one of Mumbai\'s most prestigious neighborhoods, surrounded by IT parks and premium residential complexes.',
                'property_type': 'Residential Plot',
                'price': 18000000,
                'area': 4500,
                'location': 'Mumbai',
                'address': 'Hiranandani Gardens, Powai, Mumbai, Maharashtra 400076',
                'latitude': 19.1176,
                'longitude': 72.9060,
                'status': 'Available',
                'featured': True,
                'views': 287,
                'shares': 41
            },
            {
                'title': 'Tech Park Commercial Plot in Hinjewadi',
                'description': 'Premium commercial plot in Pune\'s IT hub, Hinjewadi Phase 1. Perfect for IT offices, tech parks, or co-working spaces. Located near major IT giants.',
                'property_type': 'Commercial Plot',
                'price': 12000000,
                'area': 6000,
                'location': 'Pune',
                'address': 'Hinjewadi Phase 1, Pune, Maharashtra 411057',
                'latitude': 18.5912,
                'longitude': 73.7389,
                'status': 'Available',
                'featured': True,
                'views': 312,
                'shares': 38
            },
            {
                'title': 'Hilltop Retreat Plot in Lonavala',
                'description': 'Breathtaking hilltop plot in the scenic hill station of Lonavala. Ideal for building a luxury weekend villa or boutique resort. Surrounded by lush greenery with panoramic mountain views.',
                'property_type': 'Residential Plot',
                'price': 5500000,
                'area': 4000,
                'location': 'Lonavala',
                'address': 'Old Mumbai-Pune Highway, Lonavala, Maharashtra 410401',
                'latitude': 18.7537,
                'longitude': 73.4076,
                'status': 'Available',
                'featured': False,
                'views': 178,
                'shares': 22
            },
            {
                'title': 'Strategic Industrial Plot in MIDC Pune',
                'description': 'Large industrial plot in the established MIDC Bhosari industrial area. Perfect for manufacturing units, warehouses, or logistics hubs. 24/7 power supply and excellent connectivity.',
                'property_type': 'Industrial Plot',
                'price': 8000000,
                'area': 15000,
                'location': 'Pune',
                'address': 'MIDC Bhosari, Pune, Maharashtra 411026',
                'latitude': 18.6298,
                'longitude': 73.8450,
                'status': 'Available',
                'featured': False,
                'views': 134,
                'shares': 15
            },
            {
                'title': 'Premium Gated Community Plot in Thane',
                'description': 'Well-planned residential plot in an upcoming gated community in Thane. Features include 24/7 security, landscaped gardens, clubhouse, and children\'s play area.',
                'property_type': 'Residential Plot',
                'price': 7200000,
                'area': 3500,
                'location': 'Thane',
                'address': 'Ghodbunder Road, Thane, Maharashtra 400607',
                'latitude': 19.2183,
                'longitude': 72.9781,
                'status': 'Available',
                'featured': False,
                'views': 201,
                'shares': 26
            },
            {
                'title': 'Riverside Resort Plot in Alibaug',
                'description': 'Stunning riverside plot in the coastal town of Alibaug, perfect for resort or vacation home development. Direct river access, coconut groves, and serene natural surroundings.',
                'property_type': 'Residential Plot',
                'price': 9500000,
                'area': 7500,
                'location': 'Alibaug',
                'address': 'Mandwa Road, Alibaug, Maharashtra 402201',
                'latitude': 18.6414,
                'longitude': 72.8722,
                'status': 'Available',
                'featured': True,
                'views': 223,
                'shares': 31
            }
        ]
        
        # Image URLs for each property
        property_images_list = [
            ['https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800',
             'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800',
             'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800'],
            ['https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800',
             'https://images.unsplash.com/photo-1577495508048-b635879837f1?w=800',
             'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800'],
            ['https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800',
             'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?w=800',
             'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800'],
            ['https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
             'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800',
             'https://images.unsplash.com/photo-1600210492493-0946911123ea?w=800'],
            ['https://images.unsplash.com/photo-1497366216548-37526070297c?w=800',
             'https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800',
             'https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=800'],
            ['https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800',
             'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
             'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800'],
            ['https://images.unsplash.com/photo-1565008576549-57569a49371d?w=800',
             'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800',
             'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800'],
            ['https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',
             'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800',
             'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800'],
            ['https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
             'https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=800',
             'https://images.unsplash.com/photo-1499916078039-922301b0eb9b?w=800']
        ]
        
        count = 0
        for idx, prop_data in enumerate(properties_data):
            # Check if property already exists
            existing = Property.query.filter_by(title=prop_data['title']).first()
            if not existing:
                property = Property(**prop_data)
                db.session.add(property)
                db.session.flush()
                
                # Add images
                for img_idx, img_url in enumerate(property_images_list[idx]):
                    prop_image = PropertyImage(
                        property_id=property.id,
                        image_url=img_url,
                        is_primary=(img_idx == 0)
                    )
                    db.session.add(prop_image)
                
                count += 1
        
        db.session.commit()
        flash(f'Successfully added {count} properties to the database!', 'success')
        log_activity('seed_database', f'Seeded {count} properties', 'admin')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error seeding database: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/properties')
@admin_login_required
def admin_properties():
    page = request.args.get('page', 1, type=int)
    properties = Property.query.order_by(Property.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/properties.html', properties=properties)

@app.route('/admin/property/add', methods=['GET', 'POST'])
@admin_login_required
def admin_add_property():
    form = PropertyForm()
    
    if form.validate_on_submit():
        try:
            property = Property(
                title=form.title.data,
                description=form.description.data,
                property_type=form.property_type.data,
                price=form.price.data,
                area=form.area.data,
                location=form.location.data,
                address=form.address.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                status=form.status.data,
                featured=form.featured.data
            )
            db.session.add(property)
            db.session.flush()
            
            # Handle image uploads
            if form.images.data:
                for i, image in enumerate(form.images.data):
                    if image and allowed_file(image.filename):
                        image_path = save_uploaded_file(image, 'images')
                        if image_path:
                            prop_image = PropertyImage(
                                property_id=property.id,
                                image_url=image_path,
                                is_primary=(i == 0)
                            )
                            db.session.add(prop_image)
            
            # Handle video URLs
            if form.video_urls.data:
                video_urls = form.video_urls.data.strip().split('\n')
                for url in video_urls:
                    url = url.strip()
                    if url:
                        video_type = 'youtube' if 'youtube.com' in url or 'youtu.be' in url else 'vimeo'
                        prop_video = PropertyVideo(
                            property_id=property.id,
                            video_url=url,
                            video_type=video_type
                        )
                        db.session.add(prop_video)
            
            # Handle document uploads
            if form.documents.data:
                for document in form.documents.data:
                    if document and allowed_file(document.filename):
                        doc_path = save_uploaded_file(document, 'documents')
                        if doc_path:
                            file_size = os.path.getsize(os.path.join('static', doc_path))
                            file_size_str = f"{file_size / 1024:.2f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.2f} MB"
                            
                            prop_doc = PropertyDocument(
                                property_id=property.id,
                                document_name=secure_filename(document.filename),
                                document_url=doc_path,
                                document_type=document.filename.rsplit('.', 1)[1].upper(),
                                file_size=file_size_str
                            )
                            db.session.add(prop_doc)
            
            db.session.commit()
            
            log_activity('add_property', f'Added property: {property.title}', 'admin')
            
            # Notify alerts
            check_and_send_alerts(property)
            
            flash('Property added successfully!', 'success')
            return redirect(url_for('admin_properties'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding property: {str(e)}', 'error')
            print(f"Error: {e}")
    
    return render_template('admin/add_property.html', form=form)

@app.route('/admin/property/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_required
def admin_edit_property(id):
    property = Property.query.get_or_404(id)
    form = PropertyForm(obj=property)
    
    if form.validate_on_submit():
        try:
            property.title = form.title.data
            property.description = form.description.data
            property.property_type = form.property_type.data
            property.price = form.price.data
            property.area = form.area.data
            property.location = form.location.data
            property.address = form.address.data
            property.latitude = form.latitude.data
            property.longitude = form.longitude.data
            property.status = form.status.data
            property.featured = form.featured.data
            property.updated_at = datetime.utcnow()
            
            # Handle new image uploads
            if form.images.data:
                for image in form.images.data:
                    if image and allowed_file(image.filename):
                        image_path = save_uploaded_file(image, 'images')
                        if image_path:
                            prop_image = PropertyImage(
                                property_id=property.id,
                                image_url=image_path
                            )
                            db.session.add(prop_image)
            
            # Handle video URLs (replace existing)
            if form.video_urls.data is not None:
                PropertyVideo.query.filter_by(property_id=property.id).delete()
                if form.video_urls.data.strip():
                    video_urls = form.video_urls.data.strip().split('\n')
                    for url in video_urls:
                        url = url.strip()
                        if url:
                            video_type = 'youtube' if 'youtube.com' in url or 'youtu.be' in url else 'vimeo'
                            prop_video = PropertyVideo(
                                property_id=property.id,
                                video_url=url,
                                video_type=video_type
                            )
                            db.session.add(prop_video)
            
            # Handle new document uploads
            if form.documents.data:
                for document in form.documents.data:
                    if document and allowed_file(document.filename):
                        doc_path = save_uploaded_file(document, 'documents')
                        if doc_path:
                            file_size = os.path.getsize(os.path.join('static', doc_path))
                            file_size_str = f"{file_size / 1024:.2f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.2f} MB"
                            
                            prop_doc = PropertyDocument(
                                property_id=property.id,
                                document_name=secure_filename(document.filename),
                                document_url=doc_path,
                                document_type=document.filename.rsplit('.', 1)[1].upper(),
                                file_size=file_size_str
                            )
                            db.session.add(prop_doc)
            
            db.session.commit()
            
            log_activity('edit_property', f'Edited property: {property.title}', 'admin')
            
            flash('Property updated successfully!', 'success')
            return redirect(url_for('admin_properties'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating property: {str(e)}', 'error')
            print(f"Error: {e}")
    
    # Pre-fill video URLs
    if property.videos:
        form.video_urls.data = '\n'.join([v.video_url for v in property.videos])
    
    return render_template('admin/edit_property.html', form=form, property=property)

@app.route('/admin/property/delete/<int:id>', methods=['POST'])
@admin_login_required
def admin_delete_property(id):
    property = Property.query.get_or_404(id)
    
    # Delete associated files
    for image in property.images:
        try:
            os.remove(os.path.join('static', image.image_url))
        except Exception:
            pass
    
    for document in property.documents:
        try:
            os.remove(os.path.join('static', document.document_url))
        except Exception:
            pass
    
    property_title = property.title
    db.session.delete(property)
    db.session.commit()
    
    log_activity('delete_property', f'Deleted property: {property_title}', 'admin')
    
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('admin_properties'))

@app.route('/admin/image/delete/<int:id>', methods=['POST'])
@admin_login_required
def admin_delete_image(id):
    image = PropertyImage.query.get_or_404(id)
    try:
        os.remove(os.path.join('static', image.image_url))
        os.remove(os.path.join('static', document.document_url))
    except Exception:
        pass
    db.session.delete(document)
    db.session.commit()
    
    log_activity('delete_document', f'Deleted document: {document.document_name}', 'admin')
    
    return jsonify({'success': True})

@app.route('/admin/enquiries')
@admin_login_required
def admin_enquiries():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    query = Enquiry.query
    if status:
        query = query.filter_by(status=status)
    enquiries = query.order_by(Enquiry.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/enquiries.html', enquiries=enquiries)

@app.route('/admin/enquiry/status/<int:id>', methods=['POST'])
@admin_login_required
def update_enquiry_status(id):
    enquiry = Enquiry.query.get_or_404(id)
    status = request.form.get('status')
    if status in ['New', 'Contacted', 'Closed']:
        old = enquiry.status
        enquiry.status = status
        db.session.commit()
        log_activity('update_enquiry_status', f'Updated enquiry #{id} {old} -> {status}', 'admin')

        # Notify user about status change
        send_email(
            mail,
            subject=f"Your enquiry status: {status}",
            recipients=[enquiry.email],
            body=f"Hi {enquiry.name},\n\nYour enquiry status has changed to {status}.\n\nRegards,\nPremium Estate Team",
            category='enquiry'
        )

        flash('Enquiry status updated!', 'success')
    return redirect(url_for('admin_enquiries', **request.args))

# Delete enquiry
@app.route('/admin/enquiry/delete/<int:id>', methods=['POST'])
@admin_login_required
def delete_enquiry(id):
    enquiry = Enquiry.query.get_or_404(id)
    db.session.delete(enquiry)
    db.session.commit()
    log_activity('delete_enquiry', f'Deleted enquiry #{id}', 'admin')
    flash('Enquiry deleted.', 'success')
    return redirect(url_for('admin_enquiries', **request.args))

@app.route('/admin/bookings')
@admin_login_required
def admin_bookings():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    query = Booking.query
    if status:
        query = query.filter_by(status=status)
    bookings = query.order_by(Booking.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/booking/status/<int:id>', methods=['POST'])
@admin_login_required
def update_booking_status(id):
    booking = Booking.query.get_or_404(id)
    status = request.form.get('status')
    if status in ['Pending', 'Confirmed', 'Cancelled', 'Completed']:
        old = booking.status
        booking.status = status
        db.session.commit()
        log_activity('update_booking_status', f'Updated booking #{id} {old} -> {status}', 'admin')

        # Notify user on booking status change
        send_email(
            mail,
            subject=f"Booking #{booking.id} Status Updated",
            recipients=[booking.visitor_email],
            body=f"Hi {booking.visitor_name},\n\nYour booking for '{booking.property.title}' on {booking.booking_date.strftime('%d %b %Y')} changed from {old} to {status}.\n\nRegards,\nPremium Estate Team",
            category='booking'
        )

        flash('Booking status updated!', 'success')
    return redirect(url_for('admin_bookings', **request.args))

# Delete booking
@app.route('/admin/booking/delete/<int:id>', methods=['POST'])
@admin_login_required
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    log_activity('delete_booking', f'Deleted booking #{id}', 'admin')
    flash('Booking deleted.', 'success')
    return redirect(url_for('admin_bookings', **request.args))

@app.route('/admin/users')
@admin_login_required
def admin_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users)

@app.route('/admin/analytics')
@admin_login_required
def admin_analytics():
    # Analytics data
    total_properties = Property.query.count()
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    total_enquiries = Enquiry.query.count()
    
    # Property type distribution
    property_types = db.session.query(
        Property.property_type, 
        db.func.count(Property.id)
    ).group_by(Property.property_type).all()
    
    # Monthly property additions (last 6 months)
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    monthly_properties = db.session.query(
        db.func.strftime('%Y-%m', Property.created_at),
        db.func.count(Property.id)
    ).filter(Property.created_at >= six_months_ago).group_by(
        db.func.strftime('%Y-%m', Property.created_at)
    ).all()
    
    # Most viewed properties
    top_properties = Property.query.order_by(Property.views.desc()).limit(5).all()
    
    return render_template('admin/analytics.html',
                           total_properties=total_properties,
                           total_users=total_users,
                           total_bookings=total_bookings,
                           total_enquiries=total_enquiries,
                           property_types=property_types,
                           monthly_properties=monthly_properties,
                           top_properties=top_properties)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return f"Internal Server Error: {error}", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        print("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=8000)