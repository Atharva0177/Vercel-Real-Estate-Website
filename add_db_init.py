#!/usr/bin/env python3
"""Add database initialization to app.py AFTER the os.makedirs fix"""

import re

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the position after "db.session.rollback()" in the log_activity function
# We'll add the db.create_all() code after this function

insertion_point = content.find('        db.session.rollback()\n\n# PUBLIC ROUTES')

if insertion_point == -1:
    print("ERROR: Could not find insertion point!")
    exit(1)

# Insert the database initialization code
db_init_code = """        db.session.rollback()

# Initialize database tables (for Vercel serverless - runs on module load)
with app.app_context():
    try:
        db.create_all()
        print("Database tables initialized")
    except Exception as e:
        print(f"Database initialization: {e}")

# PUBLIC ROUTES"""

new_content = content.replace('        db.session.rollback()\n\n# PUBLIC ROUTES', db_init_code)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Added database initialization successfully!")
