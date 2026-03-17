from PyPDF2 import PdfReader, PdfWriter

# اسم الملف الأصلي
input_pdf = "trail.pdf"

# اسم الملف الناتج
output_pdf = "test.pdf"

reader = PdfReader(input_pdf)
writer = PdfWriter()

# إضافة أول صفحة
writer.add_page(reader.pages[0])

# حفظ الملف
with open(output_pdf, "wb") as f:
    writer.write(f)

print("First page saved successfully.")