import fitz
from deep_translator import GoogleTranslator

doc = fitz.open("book_0.pdf")
translator = GoogleTranslator(source='ar', target='en')

# Look through EVERYTHING to find where the heck "Large = Small - 1" comes from.
found = False
for page_num, page in enumerate(doc):
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0: continue
        for line in block["lines"]:
            line_text = "".join(span["text"] for span in line["spans"]).strip()
            
            if "الكبير" in line_text or "الصغير" in line_text:
                print(f"PAGE {page_num} FOUND ARABIC LINE: {repr(line_text)}")
                trans = translator.translate(line_text)
                print(f"GOOGLE TRANSLATED: {repr(trans)}")
                found = True
        
if not found:
    print("NO ARABIC LINES FOUND WITH الكبير or الصغير!")

