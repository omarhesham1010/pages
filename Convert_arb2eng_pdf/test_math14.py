import re

text = "Large - Small - 1 = 50 35 - 1 = 14" # The original equation
print("User says output was: Small - Large - 1 = 50 - 35 - 1 = 14")

def fix_math(t):
    # What PyMuPDF produces for "الكبير - الصغير - 1 = - 50 35 - 1 = 14":
    # Probably produces right-to-left: "14 = 1 - 35 50 - = 1 - الصغير - الكبير"
    # Wait, the user EXACTLY said:
    # "الكبير – الصغير - 1 = – 50 35 - 1 = 14"
    # مكتوبه "Small - Large - 1 = 50 - 35 - 1 = 14"
    
    # If the script outputted "Small - Large - 1 = 50 35 - 1 = 14", it means PyMuPDF
    # extracted it as "14 = 1 - 35 50 - = 1 - الكبير - الصغير" originally (backward from how we read it),
    # And my script reversed it to:
    # "الصغير - الكبير - 1 = - 50 35 - 1 = 14" -> "Small - Large - 1 = 50 35 - 1 = 14".
    
    # Let's test the token reversals carefully
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')

        t_new = t_new.replace('–', '-')

        # Force the math logic to be right:
        # We always want "Large (operator) Small" in standard subtraction.
        # But maybe the easiest logic is simply enforcing standard english LTR order.
        # So "Small - Large" becomes "Large - Small".
        # Why not just forcefully swap "Small - Large" IF it is physically written?
        
        t_new = re.sub(r'Small\s*-\s*Large', 'Large - Small', t_new)
        
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        # Determine if we should reverse based on the position of the equals sign or layout
        if t_new.strip().startswith('='):
            return " ".join(tokens)
        else:
            tokens.reverse()
            reversed_t = " ".join(tokens)
            
            # Google translates the messy extraction as "95 = 1 - 3 - 99 = 1 - Minor - = Major"
            reversed_t = re.sub(r'Large\s*=\s*-\s*Small', '= Large - Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*-\s*Large', '= Small - Large', reversed_t)
            reversed_t = re.sub(r'Large\s*=\s*\+\s*Small', '= Large + Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*\+\s*Large', '= Small + Large', reversed_t)
            
            # Force mathematical sanity: "Small - Large" is almost always meant to be "Large - Small" in these arabic textbooks
            reversed_t = re.sub(r'Small\s*-\s*Large', 'Large - Small', reversed_t)
            
            return reversed_t
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

print(fix_math("14 = 1 - 35 50 - = 1 - الكبير - الصغير"))
