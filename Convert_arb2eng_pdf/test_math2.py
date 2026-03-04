import re
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='ar', target='en')

texts = [
    "الكبير - الصغير + 1",
    "الصغير + 1 = الكبير",
    "= الكبير - الصغير + 1",
    "1 + minor = major"
]

for text in texts:
    print(f"Original: {text}")
    try:
        translated = translator.translate(text)
        print(f"Translated: {translated}")
    except:
        print("Translation failed")
    
    # Try the existing fix_math logic from the script
    if translated and '=' in translated and sum(1 for c in translated if c in '0123456789=+-*/%()') > len(translated) * 0.2:
        fixed = " ".join(reversed(translated.split()))
        print(f"fix_math outputs: {fixed}")
    else:
        print("fix_math would skip this because it lacks '=' or enough math chars.")
        
    print("---")
