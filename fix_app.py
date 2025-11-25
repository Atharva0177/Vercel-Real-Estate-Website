#!/usr/bin/env python3
"""Fix app.py for Vercel deployment by wrapping os.makedirs in try-except"""

# Read the original file
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and modify the problematic section
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Look for the "# Create upload directories" comment
    if i < len(lines) - 3 and '# Create upload directories' in line:
        # Add the comment and try block
        new_lines.append('# Create upload directories (Vercel read-only filesystem safe)\n')
        new_lines.append('try:\n')
        i += 1
        
        # Add the three os.makedirs lines with proper indentation
        for _ in range(3):
            if i <len(lines) and 'os.makedirs' in lines[i]:
                new_lines.append('    ' + lines[i])
                i += 1
        
        # Add except block
        new_lines.append('except (OSError, PermissionError):\n')
        new_lines.append('    pass  # Read-only filesystem on Vercel\n')
    else:
        new_lines.append(line)
        i += 1

# Write the fixed file
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed app.py successfully!")
