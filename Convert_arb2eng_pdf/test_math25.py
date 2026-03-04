import sys
import glob

# The user is probably running full_convert.py against some PDF which produces "Large = Small - 1".
# But book_0.pdf has no "الكبير" in it according to our scan.
# Maybe checking the text that full_convert actually outputs into the final pdf is a good hint?
import fitz

doc = fitz.open("book_002.pdf")
found = False

for page_num, page in enumerate(doc):
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0: continue
        for line in block["lines"]:
            line_text = "".join(span["text"] for span in line["spans"]).strip()
            
            # Print any line that has "Large" or "Small" in it from the generated english PDF
            if "Large" in line_text or "Small" in line_text:
                print(f"OUTPUT PDF LINE: {repr(line_text)}")
                found = True

if not found:
    print("NO TEXT FOUND IN OUTPUT PDF EITHER.")

