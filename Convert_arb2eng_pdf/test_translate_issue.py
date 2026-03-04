import fitz
import re
from deep_translator import GoogleTranslator

doc = fitz.open("/home/omar-h/Repos/pages/Convert_arb2eng_pdf/book_0.pdf")
translator = GoogleTranslator(source='ar', target='en')

found_text = None

for page_num, page in enumerate(doc):
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if "محمد" in text and "ترتيب" in text and ("40" in text or "50" in text):
                    found_text = text
                    print(f"--- Found on page {page_num} ---")
                    print("Raw extracted text:", repr(text))
                    
                    # Also try translating it to see what happens
                    translated = translator.translate(text)
                    print("Translated default:", repr(translated))
                    
                    # Applying the arabic to english numbers translation just to see
                    ar_to_en = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
                    text_num_en = text.translate(ar_to_en)
                    print("With english numbers:", repr(text_num_en))

if not found_text:
    print("Could not find the target text in the PDF.")
