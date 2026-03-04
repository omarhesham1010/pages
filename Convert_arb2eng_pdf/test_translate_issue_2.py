import fitz
import re

doc = fitz.open("/home/omar-h/Repos/pages/Convert_arb2eng_pdf/book_0.pdf")

for page_num, page in enumerate(doc):
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if "بينهما" in text or "طالب" in text or "فكم" in text:
                    print(f"--- Found on page {page_num} ---")
                    print("Raw extracted text:", repr(text))
