from pdf2docx import Converter

pdf_file = "book_0.pdf"
docx_file = "book_01.docx"

cv = Converter(pdf_file)
cv.convert(docx_file)
cv.close()

print("تم التحويل إلى Word ✅")