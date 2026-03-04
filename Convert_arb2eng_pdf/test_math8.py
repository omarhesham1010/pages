import re
from deep_translator import GoogleTranslator

# If the PDF extracts exactly "= الكبير - الصغير - 1 = 99 - 3 - 1 = 95"
text_extracted = "= الكبير - الصغير - 1 = 99 - 3 - 1 = 95"

translator = GoogleTranslator(source='ar', target='en')
translated = translator.translate(text_extracted)
print("Google Translated:\n", translated)

# So google translated is: "Major = - Minor - 1 = 99 - 3 - 1 = 95"
# We need to take this and fix it into "= large - small - 1 = 99 - 3 - 1 = 95"

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')

    if has_math_word and has_math_symbol:
        # Instead of tokenizing everything purely by math symbol after a bad translation
        # Lets restore "Major =" to "= Major" first
        # Because Google translates " = الكبير " as "Major ="
        
        t = t.replace('الكبير', 'large').replace('الأكبر', 'large').replace('big', 'large').replace('major', 'large').replace('Major', 'large').replace('كبير', 'large')
        t = t.replace('الصغير', 'small').replace('الأصغر', 'small').replace('minor', 'small').replace('Minor', 'small').replace('صغير', 'small')
        
        # Google made it: "large = - small - 1 = ..." but it should be "= large - small - 1"
        # Since Google is moving the equals sign from the left side of Major to the right side
        t = re.sub(r'large\s*=\s*-\s*small', '= large - small', t)
        t = re.sub(r'large\s*=\s*-\s*small', '= large - small', t)
        
        # Let's do purely regex parsing:
        # Instead of replacing, let's tokenize and see
        return t

res = fix_math(translated)
print("Fix Math:\n", res)

