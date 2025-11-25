#!/usr/bin/env python3
"""Fix hero overlay to show video background"""

# Read the file
with open('static/css/main.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the hero-overlay CSS
old_overlay = """.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /* background: linear-gradient(135deg, rgba(161, 221, 120, 0.8), rgba(52, 73, 94, 0.7)); */
    z-index: 1;
}"""

new_overlay = """.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(44, 62, 80, 0.6), rgba(52, 73, 94, 0.6));
    z-index: 1;
}"""

content = content.replace(old_overlay, new_overlay)

# Write back
with open('static/css/main.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed hero overlay successfully!")
