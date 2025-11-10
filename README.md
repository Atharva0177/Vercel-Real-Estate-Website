# 🏡 Real Estate Website - Complete Property Management Platform

![Real Estate Banner](static/images/home.png)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.0.5-red.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A full-featured real estate property management platform built with Flask, featuring property listings, user authentication, booking system, file uploads, alerting, email notifications, analytics, and a comprehensive admin dashboard.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [API](#-api-routes) • [Architecture](#-architecture--internals) • [Analytics](#-admin-analytics--reporting) • [Changelog](#-changelog--whats-new) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Highlights](#-key-highlights)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Architecture & Internals](#-architecture--internals)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Database Models](#-database-models)
- [API Routes](#-api-routes)
- [Admin Panel](#-admin-panel)
- [Admin Analytics & Reporting](#-admin-analytics--reporting)
- [User Features](#-user-features)
- [Security & Validation](#-security--validation)
- [Email Notification System](#-email-notification-system)
- [Activity Logging](#-activity-logging)
- [Customization](#-customization)
- [Testing](#-testing)
- [Deployment & Scaling](#-deployment--scaling)
- [Changelog / What's New](#-changelog--whats-new)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)
- [Project Stats](#-project-stats)

---

## 🌟 Overview

This **Real Estate Website** is a comprehensive property management platform designed for real estate agencies, property dealers, and individual sellers. It enables property listing, browsing, booking site visits, user favorites, property alerts, enquiry management, document handling, video embedding, analytics visualization, and administrative control.

### 🎯 Key Highlights

- **Dual Interface**: Separate portals for administrators and end-users.
- **Full Lifecycle Property Management**: Images, videos, documents, status changes, featured flags, views & shares tracking.
- **User Engagement Tools**: Favorites, alerts with automatic email triggering, booking system.
- **Real-Time Admin Insights**: Property type distribution, monthly additions, top viewed properties, aggregated counters.
- **Robust Upload Handling**: Timestamped secure filenames, multi-file support.
- **Email Notifications**: Enquiries, bookings, status changes, alert matches, admin test.
- **Activity Auditing**: Every critical action logged with IP & user context.
- **Configurable Performance**: Pagination controls for properties, users, admin lists.
- **Extensible Design**: Modular models and forms, structured configuration for environment overrides.

---

## ✨ Features

### 🏠 Property Features
- ✅ CRUD operations for properties
- ✅ Multiple property categories (Residential Plot, Commercial Plot, Agricultural Land, Industrial Plot)
- ✅ Featured property highlighting & badge
- ✅ Status workflow: Available → Reserved → Sold
- ✅ View counter (auto-increment on detail view)
- ✅ Share counter (via `/share/<id>` route)
- ✅ Multiple image uploads with primary image auto-selection
- ✅ YouTube/Vimeo video embedding (multi-URL input)
- ✅ Document attachments (PDF, DOC, DOCX) with stored size metadata
- ✅ GPS coordinates (latitude / longitude)
- ✅ Advanced filtering (type, min/max price, location substring, sort by price/area/date)
- ✅ Pagination support (configurable)
- ✅ Secure file naming with timestamp + sanitized original name

### 👥 User Features
- ✅ Registration (password hashing, uniqueness validation)
- ✅ Login / logout sessions
- ✅ Dashboard (favorites, alerts, bookings summary)
- ✅ Favorite management (toggle endpoint)
- ✅ Property alerts (min/max price, type, location match)
- ✅ Automatic alert email when new property matches criteria
- ✅ Site visit booking with date + time slot & visitor info
- ✅ Booking cancellation
- ✅ Enquiry submission (linked optionally to a property)
- ✅ Document downloads (with activity logging)
- ✅ Basic activity visibility (e.g., favorites/bookings history)

### 🔐 Admin Features
- ✅ Secure login (session flag `admin_logged_in`)
- ✅ Dashboard KPIs (properties, users, bookings, enquiries, views, shares)
- ✅ Property add/edit/delete (with file lifecycle cleanup)
- ✅ Inline video list replacement on edit
- ✅ Image & document selective deletion endpoints
- ✅ Booking management (status: Pending, Confirmed, Cancelled, Completed)
- ✅ Enquiry management (status: New, Contacted, Closed)
- ✅ User list view
- ✅ Analytics panel (distributions & trends)
- ✅ Email test utility
- ✅ Activity log capture for every admin event

### 📊 Analytics & Reporting
- ✅ Total entities: properties, users, bookings, enquiries
- ✅ Property type distribution grouped counts
- ✅ Monthly additions (last ~6 months bucketed by year-month)
- ✅ Top viewed properties (limit configurable)
- ✅ Global view + share aggregations
- ✅ Recent activity stream (last N actions)

### 📧 Email Notification Use Cases
- Enquiry received (admin + user)
- Booking created (admin + visitor)
- Booking status changed (visitor)
- Enquiry status changed (enquirer)
- Property alert triggered (matching user)
- Admin test email endpoint

### 🧾 Logging & Auditing
- ActivityLog model stores: action, description, user_type (admin/user/guest/system), user_id, IP, timestamp.

---

## 🛠 Technology Stack

### Backend
- **Flask 2.3.3**
- **SQLAlchemy 3.0.5**
- **Flask-WTF / WTForms**
- **Werkzeug 2.3.7** (security, utilities)
- **Flask-Mail** (transactional emails)
- **Python-dotenv** (env configuration)
- **SQLite** (default; interchangeable with PostgreSQL/MySQL)

### Frontend
- **HTML5 / Jinja2 Templates**
- **CSS3 / Bootstrap 5**
- **JavaScript (Vanilla)**
- **Font Awesome Icons**

### Security
- Password hashing (Werkzeug)
- CSRF protection via Flask-WTF
- Session lifetime control
- Filename sanitization & extension validation

---

## 🧱 Architecture & Internals

| Layer | Responsibility |
|-------|----------------|
| `app.py` | Route definitions, decorators, helper utilities, upload handling, email dispatch, business logic orchestration |
| `models.py` | ORM models: Property, PropertyImage, PropertyVideo, PropertyDocument, Enquiry, User, Favorite, PropertyAlert, Booking, Admin, ActivityLog |
| `forms.py` | WTForms definitions with validation constraints |
| `config.py` | Environment-driven configuration (DB, uploads, mail, pagination, admin credentials) |
| `seed_data.py` | One-time seeding script creating sample properties (images/videos), demo users, admin credentials output |
| `templates/` | Segregated admin/user/public HTML templates |
| `static/uploads/` | Runtime persisted assets (images/videos/documents) |
| `static/images/` | Project and UI assets |
| Activity Logging | Centralized via `log_activity()` helper in `app.py` |
| Alert Matching | `check_and_send_alerts(property)` executes matching & notifications after property creation |

### Data Flow Example: Add Property
1. Admin submits form (images/videos/documents).
2. Server validates & persists Property row.
3. Uploads saved with timestamped names → PropertyImage / PropertyVideo / PropertyDocument rows.
4. `log_activity('add_property', ...)` persists activity.
5. `check_and_send_alerts(property)` finds active alerts & emails matched users.
6. Redirect with success flash.

---

## 📁 Project Structure

```
Real-Estate-Website/
│
├── app.py
├── config.py
├── models.py
├── forms.py
├── seed_data.py
├── requirements.txt
├── .env
├── .gitignore
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   ├── favicon.ico
│   └── uploads/
│       ├── images/
│       ├── videos/
│       └── documents/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── properties.html
│   ├── property_detail.html
│   ├── contact.html
│   ├── 404.html
│   ├── admin/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── properties.html
│   │   ├── add_property.html
│   │   ├── edit_property.html
│   │   ├── enquiries.html
│   │   ├── bookings.html
│   │   ├── users.html
│   │   └── analytics.html
│   └── user/
│       ├── register.html
│       ├── login.html
│       ├── dashboard.html
│       ├── favorites.html
│       └── create_alert.html
│
└── instance/
    └── realestate.db
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Step 1: Clone

```bash
git clone https://github.com/Atharva0177/Real-Estate-Website.git
cd Real-Estate-Website
```

### Step 2: Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Step 3: Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt`:
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-WTF==1.1.1
WTForms==3.0.1
Flask-Login==0.6.2
email-validator==2.0.0
Pillow==10.0.0
python-dotenv==1.0.0
Werkzeug==2.3.7
```

### Step 4: Environment Variables (.env)

```env
SECRET_KEY=qwertyuiop
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
DATABASE_URL=sqlite:///realestate.db

# Optional mail settings (override config defaults)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_password
MAIL_DEFAULT_SENDER=your_email@example.com
```

Change all secrets for production.

### Step 5: Seed Database

```bash
python seed_data.py
```

Creates:
- Tables
- 9 sample properties
- 2 demo users
- Outputs admin + user credentials

### Step 6: Run App

```bash
python app.py
```

Access at: `http://localhost:8000`

---

## ⚙️ Configuration

`config.py` excerpt:

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///realestate.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','mp4','webm','ogg','pdf','doc','docx'}

    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    PROPERTIES_PER_PAGE = int(os.getenv('PROPERTIES_PER_PAGE', 9))
    ADMIN_PAGE_SIZE = int(os.getenv('ADMIN_PAGE_SIZE', 20))
    USER_PAGE_SIZE = int(os.getenv('USER_PAGE_SIZE', 12))

    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
```

### Production Checklist
- [ ] Replace `SECRET_KEY`
- [ ] Rotate admin credentials
- [ ] Switch to PostgreSQL/MySQL
- [ ] Configure proper SMTP credentials
- [ ] Serve behind HTTPS
- [ ] Offload static/uploads to CDN or S3
- [ ] Enable backups & monitoring
- [ ] Set `DEBUG=False` when deploying

---

## 📖 Usage

### Admin Login
```
URL: http://localhost:8000/admin/login
Username: admin
Password: admin123
```

### Demo User
```
Email: demo@example.com
Password: demo123
```

### Atharva User
```
Email: atharva@example.com
Password: atharva123
```

---

## 📸 Screenshots

### Homepage
![Homepage](static/images/home.png)
*Featured properties and search*

### Property Listings
![Property Listings](static/images/listings.png)
*Filters & pagination*

### Property Details
![Property Details](static/images/details.png)
*Gallery, videos, booking form*

### Admin Dashboard
![Admin Dashboard](static/images/admin.png)
*KPIs & recent items*

### User Dashboard
![User Dashboard](static/images/user.png)
*Favorites & alerts overview*

---

## 🗄️ Database Models

### Property
```
id, title, description, property_type, price, area,
location, address, latitude, longitude,
status, featured, views, shares,
created_at, updated_at
Relationships: images, videos, documents, favorites, bookings
```

### User
```
id, name, email (unique), phone, password_hash, created_at
Relationships: favorites, alerts, bookings
```

### Booking
```
id, user_id, property_id,
booking_date, booking_time,
visitor_name, visitor_email, visitor_phone,
number_of_visitors, message, status, created_at
```

### Other
- PropertyImage (primary flag)
- PropertyVideo (url + type)
- PropertyDocument (name, url, type, size)
- Enquiry (name, email, phone, message, status)
- Favorite (user ↔ property)
- PropertyAlert (criteria, active flag)
- ActivityLog (action, description, user_type, user_id, ip, timestamp)
- Admin (username/password hash)

---

## 🔗 API Routes

### Public
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage (featured + recent) |
| GET | `/properties` | Listings (filters & sort) |
| GET | `/property/<id>` | Property detail (views++) |
| POST | `/enquiry` | Submit enquiry |
| GET | `/contact` | Contact form |
| POST | `/share/<id>` | Increment share counter |
| GET | `/document/download/<doc_id>` | Download property document |

### User Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/user/register` | Register |
| GET/POST | `/user/login` | Login |
| GET | `/user/logout` | Logout |
| GET | `/user/dashboard` | Dashboard |

### User Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/favorite/toggle/<property_id>` | Toggle favorite |
| GET | `/user/favorites` | Favorites list |
| GET/POST | `/alert/create` | Create alert |
| POST | `/alert/delete/<alert_id>` | Delete alert |
| POST | `/booking/create/<property_id>` | Create booking |
| POST | `/booking/cancel/<booking_id>` | Cancel booking |

### Admin Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/admin/login` | Admin login |
| GET | `/admin/logout` | Admin logout |

### Admin Core
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/dashboard` | KPI overview |
| GET | `/admin/properties` | Manage properties |
| GET/POST | `/admin/property/add` | Add property |
| GET/POST | `/admin/property/edit/<id>` | Edit property |
| POST | `/admin/property/delete/<id>` | Delete property |
| POST | `/admin/image/delete/<id>` | Delete image |
| POST | `/admin/document/delete/<id>` | Delete document |
| GET | `/admin/enquiries` | Enquiry list |
| POST | `/admin/enquiry/status/<id>` | Update enquiry status |
| POST | `/admin/enquiry/delete/<id>` | Delete enquiry |
| GET | `/admin/bookings` | Booking list |
| POST | `/admin/booking/status/<id>` | Update booking status |
| POST | `/admin/booking/delete/<id>` | Delete booking |
| GET | `/admin/users` | User list |
| GET | `/admin/analytics` | Analytics panel |
| GET | `/admin/test-email` | Send test email |

---

## 🔐 Admin Panel

Navigate: `http://localhost:8000/admin/login`

Features:
- Dashboard metrics & recent items
- Property CRUD with media & alerts trigger
- Enquiry triage (status transitions)
- Booking lifecycle management
- User overview
- Analytics visualization
- Email system test
- Activity logging trail

---

## 📈 Admin Analytics & Reporting

Metrics:
- Counts: total properties/users/bookings/enquiries
- Availability breakdown (available/reserved/sold)
- Aggregated views & shares
- Distribution: property_type grouped counts
- Monthly addition trend (last 6 months)
- Top viewed properties (top 5)
- Recent activities (latest 10)

All computed via SQLAlchemy queries (grouped, ordered, aggregated functions).

---

## 👤 User Features

Dashboard includes:
- Favorites (quick access + toggle)
- Alerts (criteria & activation)
- Bookings (status & cancellation)
- Potential activity actions like downloads tracked

Alert Trigger Logic:
- When new property added:
  - Matches if (type matches OR alert type empty) AND
    min_price <= property.price <= max_price (if provided) AND
    location substring match (case-insensitive) AND
    alert is active.
  - Sends email with property summary & direct link.

---

## 🛡 Security & Validation

- WTForms validators: length, email format, numeric ranges
- Password hashing (generate/check functions)
- CSRF tokens on forms
- Secure filename handling (`secure_filename`) + timestamp prefix to avoid collisions
- Extension whitelist enforced from `Config.ALLOWED_EXTENSIONS`
- Session-based auth gates (`@admin_login_required`, `@user_login_required`)
- Size-limited uploads (`MAX_CONTENT_LENGTH = 50MB`)
- Document size stored (human readable KB/MB string)

---

## ✉️ Email Notification System

Events & Templates (plain text):
- Enquiry received (admin + user acknowledgment)
- Booking created (admin + visitor confirmation)
- Booking status change (visitor)
- Enquiry status change (enquirer)
- Alert triggered (matching users)
- Admin test email

Environment-dependent:
- Requires `MAIL_SERVER`, `MAIL_PORT`, TLS/SSL flags, credentials, and default sender.
- Graceful fallback if mail settings incomplete (error flashes).

---

## 🧾 Activity Logging

`ActivityLog` schema:
```
id, action, description, user_type, user_id, ip_address, created_at
```
Examples of logged actions:
- `user_register`, `user_login`, `add_property`, `edit_property`, `delete_property`
- `create_booking`, `cancel_booking`
- `create_alert`, `delete_alert`
- `submit_enquiry`, `update_enquiry_status`
- `update_booking_status`, `share_property`, `download_document`
- `admin_login`, `admin_logout`, `test_email`
Used for audit, debugging, analytics, potential future security anomaly detection.

---

## 🎨 Customization

### Branding / Theme
Edit `static/css/` (create theme variables or modify existing CSS):
```css
:root {
  --primary-color: #3498db;
  --secondary-color: #2ecc71;
  --danger-color: #e74c3c;
}
```

### Property Types
Extend choices in `forms.py > PropertyForm` & `PropertyAlertForm`.

### Pagination
Adjust in `.env`:
```
PROPERTIES_PER_PAGE=12
ADMIN_PAGE_SIZE=30
USER_PAGE_SIZE=15
```

---

## 🧪 Testing

Install test libs:
```bash
pip install pytest pytest-flask
```

Run:
```bash
pytest
```

Manual Checklist:
- [x] User register/login
- [x] Admin login
- [x] Property add with images/videos/documents
- [x] Alert creation & trigger (add matching property)
- [x] Booking create/cancel/status update
- [x] Enquiry submit & status change
- [x] Favorite toggle
- [x] Document download
- [x] Share counter increment
- [x] Analytics renders without error
- [x] Email sending flows (with real creds)
- [x] Mobile responsiveness

---

## ☁ Deployment & Scaling

| Aspect | Recommendation |
|--------|---------------|
| WSGI Server | Gunicorn / uWSGI behind Nginx |
| DB | PostgreSQL for concurrency & indexing |
| File Storage | S3 / GCS + signed URLs |
| Caching | Redis (sessions, activity feed, analytics precompute) |
| Background Tasks | Celery or RQ for email & alert processing |
| Monitoring | Prometheus + Grafana / APM (New Relic) |
| Security | HTTPS termination, secure cookie flags, rate limiting |
| Migrations | Alembic for schema evolution |
| Containerization | Dockerfile + multi-stage build |
| Scaling | Horizontal (stateless app) + CDN for static assets |

Performance Opportunities:
- Pre-calculate monthly stats nightly
- Add composite indexes (e.g., `property_type`, `status`, `created_at`)
- Offload heavy email bursts to async queue

---

## 🗂 Changelog / What's New

Latest Enhancements (from code analysis compared to initial conceptual README):
- Added share counter & route (`/share/<property_id>`)
- Activity logging system (IP + user context)
- Document metadata (size string, download endpoint)
- Video embedding multi-URL support (YouTube/Vimeo autodetection)
- Alert trigger emailing after property creation
- Booking status update notifications
- Enquiry status change notifications
- Admin test email endpoint
- Image/document selective deletion routes
- Configurable pagination for properties/admin/users
- Extended analytics: top viewed, monthly addition trend, distribution
- Centralized helper for alert matching `check_and_send_alerts`
- Timestamped secure uploads with cleaned filenames
- Improved multi-file validation for images/documents

(If you maintain semantic versioning, start a `CHANGELOG.md` and tag releases.)

---

## 🎯 Future Enhancements

- [ ] SMS alerts for bookings
- [ ] Virtual property tours (360° view)
- [ ] Chat system (user ↔ admin)
- [ ] Multi-language support (Flask-Babel)
- [ ] Advanced analytics with charts (Chart.js)
- [ ] Social media integration
- [ ] Async task queue + retry logic

---

## 📝 License

MIT License

```
MIT License

Copyright (c) 2025 Atharva

Permission is hereby granted, free of charge, to any person obtaining a copy
...
```

See [LICENSE](LICENSE) for full text.

---

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Unsplash](https://unsplash.com/) (placeholder images)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

## 📊 Project Stats

![Language Stats](https://img.shields.io/github/languages/top/Atharva0177/Real-Estate-Website)
![Code Size](https://img.shields.io/github/languages/code-size/Atharva0177/Real-Estate-Website)
![Last Commit](https://img.shields.io/github/last-commit/Atharva0177/Real-Estate-Website)

**Composition:**
- HTML: 54%
- CSS: 20.5%
- Python: 19%
- JavaScript: 6.5%

---


### ✅ Quick Start (TL;DR)

```bash
git clone https://github.com/Atharva0177/Real-Estate-Website.git
cd Real-Estate-Website
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed_data.py
python app.py
# Visit http://localhost:8000
```

---

