import re
from deep_translator import GoogleTranslator

# So Google translates text and then we run fix_math.
# What does Google actually output for "= الكبير - الصغير - 1 = 99 - 3 - 1 = 95"?
translator = GoogleTranslator(source='ar', target='en')
txt = "95 = 1 - 3 - 99 = 1 - الصغير - الكبير ="
res_g = translator.translate(txt)
print(f"Google translated ({txt}):\n{res_g}")

txt2 = "= الكبير - الصغير - 1 = 99 - 3 - 1 = 95"
res_g2 = translator.translate(txt2)
print(f"Google translated ({txt2}):\n{res_g2}")

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')

    if has_math_word and has_math_symbol:
        # Instead of replacing everything to lower case 'large'/'small', we use 'Large' / 'Small'
        t = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t = t.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')

        # Sometimes Google Translate corrupts "= الكبير - الصغير" into "Major = - Minor"
        # We must repair this before parsing:
        t = re.sub(r'Large\s*=\s*-\s*Small', '= Large - Small', t)
        t = re.sub(r'Small\s*=\s*-\s*Large', '= Small - Large', t)

        # PyMuPDF extracts things completely backward.
        # So "95 = 1 - 3 - 99 = 1 - الصغير - الكبير =" translates to "95 = 1 - 3 - 99 = 1 - Small - Large =" (if we just translated the words)
        # Google actually translated it to: "95 = 1 - 3 - 99 = 1 - Small - Large ="
        # This completely backward version HAS to be reversed for English.
        # But "= الكبير - الصغير - 1" is NOT completely backward in Arabic reading direction (RTL -> LTR is a mess here).
        
        # We need to rely securely on reversing IF AND ONLY IF it looks like a backward formula.
        # Backward formula ends with "=", e.g., "95 = 1 - 3 - 99 = 1 - Small - Large ="
        
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t) if tok.strip()]
        
        if t.strip().startswith('='):
            # This means it's already in a good format, e.g. "= Large - Small - 1 ..."
            return " ".join(tokens)
        else:
            # We reverse it
            tokens.reverse()
            return " ".join(tokens)
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

print("---")
# Test user's exact input case
test_case = translator.translate("= الكبير - الصغير - 1 = 99 - 3 - 1 = 95")
# Or what if it was extracted backwards by pymupdf?
# "95 = 1 - 3 - 99 = 1 - الصغير - الكبير =" is what PyMuPDF likely extracts.
mocked_pdf_extract = "95 = 1 - 3 - 99 = 1 - الصغير - الكبير ="
translated_mock = translator.translate(mocked_pdf_extract)
print(f"PDF extraction back-translated:\n{translated_mock}")
print(f"fix_math outputs:\n{fix_math(translated_mock)}")

