#!/usr/bin/env python3
"""Integrate Vercel Blob into app.py"""

import re

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add vercel_blob import after the other imports
import_addition = """from helpers.notifications import send_email  # use send_email helper
try:
    import vercel_blob
except ImportError:
    vercel_blob = None  # Will use local storage if not available"""

content = content.replace(
    "from helpers.notifications import send_email  # use send_email helper",
    import_addition
)

# 2. Replace the save_uploaded_file function
old_function = """def save_uploaded_file(file, subfolder='images'):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        target_dir = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(target_dir, exist_ok=True)
        filepath = os.path.join(target_dir, filename)
        file.save(filepath)
        return f'uploads/{subfolder}/{filename}'
    return None"""

new_function = """def save_uploaded_file(file, subfolder='images'):
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
    return None"""

content = content.replace(old_function, new_function)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Integrated Vercel Blob successfully!")
