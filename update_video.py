#!/usr/bin/env python3
"""Update index.html to use local video file"""

# Read the file
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the CDN video URL with local path
old_video = '<source src="https://cdn.pixabay.com/video/2022/01/12/104374-665224279_large.mp4" type="video/mp4">'
new_video = '<source src="{{ url_for(\'static\', filename=\'uploads/videos/video.mp4\') }}" type="video/mp4">'

content = content.replace(old_video, new_video)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html to use local video!")
