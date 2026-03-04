import re

texts = [
    "1 + minor = major",
    "= الكبير - الصغير + 1",
    "الأصغر + 1 = الأكبر",
    "١ + الصغير = الكبير",
    "= الأكبر - الأصغر + ١"
]

def process_math_phrase(text):
    # Normalize arabic text for math
    ar_to_en = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
    text = text.translate(ar_to_en)
    
    # Check if this looks like a major/minor math equation
    # Cases like: = الكبير - الصغير + 1 or 1 + الصغير = الكبير
    
    is_math_phrase = False
    if any(word in text for word in ["الكبير", "الصغير", "الأكبر", "الأصغر", "major", "minor", "large", "small"]):
        if sum(1 for c in text if c in '0123456789=+-*/%()') >= 1: # Has at least one math symbol/number
            is_math_phrase = True
            
    if not is_math_phrase:
         return text
         
    # It's a math phrase with Major/Minor. Replace Arabic terms directly to ensure they don't get lost
    replacements = {
        "الكبير": "major",
        "الأكبر": "major",
        "الصغير": "minor",
        "الأصغر": "minor"
    }
    
    processed = text
    for ar, en in replacements.items():
        processed = processed.replace(ar, en)
        
    print(f"Pre-translation processed: {processed}")
    
    # We now translate if needed (but we already replaced the key words)
    # The real issue is the order. The user wants "1 + minor = major" to become "= major - minor + 1" or similar?
    # Wait, the user said:
    # "1 + minor = major" المفروض دا مثلا تبقى ترجمة  "= الكبير - الصغير + 1"
    # فالمفروض تبقى "= large - small + 1"
    
    # It seems the text extracted is "1 + minor = major" (which is actually reverse of English: major = minor + 1)
    # The Arabic was "= الكبير - الصغير + 1". 
    # Extracted by PDF as: "1 + الصغير - الكبير =" maybe?
    
    # Let's say the extracted text is "1 + الصغير - الكبير =" or "1 + minor - major ="
    # If the text has =, +, -, minor, major... Reverse the tokens!
    
    tokens = [t for t in re.split(r'(\s+|[=+\-*/])', processed) if t.strip() or t in '=+-*/']
    
    print(f"Tokens: {tokens}")
    tokens.reverse()
    print(f"Reversed tokens: {''.join(tokens)}")
    return "".join(tokens)

for t in texts:
    print(f"Original: {t}")
    res = process_math_phrase(t)
    print(f"Result: {res}")
    print("---")

