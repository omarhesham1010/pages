import re
from deep_translator import GoogleTranslator

# If it skipped the symbols check, this means Google Translated "= الكبير - الصغير - 1"
# into something that has NO EQUALS SIGN BEFORE OUR SCRIPT SEES IT?! No, that makes no sense, the user explicitly said the output was "Large = Small - 1". It MUST have an equals sign!
# So why did `grep INPUT trace4.txt` yield NO output?!
# The ONLY reason `grep INPUT` would fail to print is:
# "has_math_word and has_math_symbol" evaluated to FALSE.

# Let's write a targeted scanner of book_0.pdf that prints exactly what the text blocks are WITHOUT translation.
import fitz
doc = fitz.open("book_0.pdf")
translator = GoogleTranslator(source='ar', target='en')

for page in doc:
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0: continue
        for line in block["lines"]:
            line_text = ""
            for span in line["spans"]:
                line_text += span["text"]
            
            line_text = line_text.strip()
            
            if "الكبير" in line_text or "الصغير" in line_text:
                print(f"FOUND IN PDF: {repr(line_text)}")
                
                # Let's manually run the conditions
                t_lower = translator.translate(line_text).lower()
                math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
                has_math_word = any(w in t_lower for w in math_words)
                has_math_symbol = any(c in t_lower for c in '=+-*/')
                
                print(f"GOOGLE ARABIC TO EN TRANSLATION: {t_lower}")
                print(f"  has_math_word: {has_math_word}")
                print(f"  has_math_symbol: {has_math_symbol}")
                print("---")
