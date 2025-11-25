# Quick Fix for Vercel Deployment

The crash is happening because `app.py` tries to create directories on line 35-37.

Vercel has a **READ-ONLY filesystem**, so this crashes immediately.

##Fix

Open `app.py` and find these lines (around line 34-37):

```python
# Create upload directories
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'], exist_ok=True)
```

**Replace them with:**

```python
# Create upload directories (wrap in try-except for Vercel's read-only filesystem)
try:
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
except (OSError, PermissionError):
    # Read-only filesystem (Vercel) - this is expected
    pass
```

Then deploy again:
```bash
npx vercel --prod
```

That's it! The site should work after this.
