import fitz
import re

doc = fitz.open("/run/media/omar-h/38029BDD029B9E86/Repos/pages/Convert_arb2eng_pdf/book_0.pdf")
for page_num, page in enumerate(doc):
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if "محمد" in span["text"] or "ترتيب" in span["text"] or "40" in span["text"]:
                    print(f"Page {page_num}: {span['text']}")

