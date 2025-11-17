import re

# Read the file
with open('template_generator.py', 'r') as f:
    content = f.read()

# Fix the problematic lines
fixes = [
    (r"'Here\\'s why'", "'Here is why'"),
    (r"you\\'ve been waiting for", "you have been waiting for"),
    (r"you\\'re ready", "you are ready"),
]

for old, new in fixes:
    content = content.replace(old, new)

# Write back
with open('template_generator.py', 'w') as f:
    f.write(content)

print("Fixed f-string backslash issues")
