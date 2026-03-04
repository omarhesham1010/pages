import re

texts = [
    "الكبير - الصغير + 1",
    "الصغير + 1 = الكبير",
    "= الكبير - الصغير + 1"
]

for t in texts:
    print(f"Original: {t}")
    # Google Translate behavior mock (approximate):
    translated = t.replace("الكبير", "major").replace("الصغير", "minor")
    print(f"Mock translated: {translated}")
    
    # Try the existing fix_math logic from the script
    if '=' in translated and sum(1 for c in translated if c in '0123456789=+-*/%()') > len(translated) * 0.2:
        fixed = " ".join(reversed(translated.split()))
        print(f"fix_math outputs: {fixed}")
    else:
        print("fix_math would skip this because it lacks '=' or enough math chars.")
        
    print("---")
