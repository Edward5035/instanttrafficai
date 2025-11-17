# Fix all quote issues by replacing problematic strings
with open('template_generator.py', 'r') as f:
    content = f.read()

# Replace all instances of '10x'd' which cause quote issues  
content = content.replace("'10x'd'", "'10xed'")
content = content.replace("'tripled', 'doubled', '10x'd'", "'tripled', 'doubled', '10xed'")

with open('template_generator.py', 'w') as f:
    f.write(content)

print("Fixed quote issues")
