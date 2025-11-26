#!/usr/bin/env python3
"""Optimize hero video loading"""

file_path = 'templates/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and optimize the video tag
for i, line in enumerate(lines):
    # Add preload="metadata" and poster
    if '<video autoplay muted loop playsinline id="heroVideo">' in line:
        lines[i] = '''        <video 
            autoplay 
            muted 
            loop 
            playsinline 
            id="heroVideo"
            preload="metadata"
            poster="{{ url_for('static', filename='uploads/videos/video-poster.jpg') }}"
        >\r\n'''

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Video optimized!")
print("   - preload='metadata' (loads only metadata, not full video)")
print("   - poster image added (shows before video loads)")
print("")
print("⚠️  Next step: Create a poster image from your video!")
print("   Save first frame as: static/uploads/videos/video-poster.jpg")
