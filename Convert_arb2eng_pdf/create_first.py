from PyPDF2 import PdfReader, PdfWriter

def save_first_page(input_pdf_path, output_pdf_path):
    # اقرأ الملف
    reader = PdfReader(input_pdf_path)
    
    # اتأكد إن فيه صفحات
    if len(reader.pages) == 0:
        print("الملف لا يحتوي على صفحات")
        return
    
    # خُد أول صفحة
    first_page = reader.pages[191]
    
    # اعمل Writer جديد
    writer = PdfWriter()
    writer.add_page(first_page)
    
    # احفظ الصفحة في ملف جديد
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)
    
    print("تم حفظ أول صفحة بنجاح")

# مثال استخدام
save_first_page("original_book.pdf", "book_3.pdf")