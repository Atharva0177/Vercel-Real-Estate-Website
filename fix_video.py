#!/usr/bin/env python3
"""Fix video background in index.html"""

# Read the file
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the video URLs
old_video_section = '''    <div class="hero-video">
        <video autoplay muted loop playsinline id="heroVideo">
            <source src="static\\uploads\\videos\\video.mp4" type="video/mp4">
            <source src="static\\uploads\\videos\\video.mp4" type="video/mp4">
            <!-- Fallback video -->
            <source src="static\\uploads\\videos\\video.mp4" type="video/mp4">
        </video>
    </div>'''

new_video_section = '''    <div class="hero-video">
        <video autoplay muted loop playsinline id="heroVideo">
            <source src="https://cdn.pixabay.com/video/2022/01/12/104374-665224279_large.mp4" type="video/mp4">
            <!-- Fallback: Real estate aerial video -->
            Your browser does not support the video tag.
        </video>
    </div>'''

content = content.replace(old_video_section, new_video_section)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed video background successfully!")
