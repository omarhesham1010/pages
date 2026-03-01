import os
import win32com.client

def convert_word_to_pdf(input_path, output_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    doc = word.Documents.Open(os.path.abspath(input_path))
    doc.SaveAs(os.path.abspath(output_path), FileFormat=17)  # 17 = PDF
    doc.Close()

    word.Quit()

    print("تم التحويل إلى PDF ✅")


# مثال استخدام
input_file = "book_01.docx"
output_file = "book_03.pdf"

convert_word_to_pdf(input_file, output_file)