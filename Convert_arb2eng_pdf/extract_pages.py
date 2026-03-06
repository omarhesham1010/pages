import fitz  # PyMuPDF
import os

# ===== إعدادات =====
INPUT_PDF = os.path.join(os.path.dirname(__file__), "original_book.pdf")
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "Statistics_Book.pdf")

# رينج الصفحات (ابتداءاً من 1)
START_PAGE = 179   # أول صفحة
END_PAGE   = 206   # آخر صفحة


# ====================

def extract_pages(input_path: str, output_path: str, start: int, end: int):
    """
    Extract pages [start..end] (1-indexed, inclusive) from input_path
    and write them to output_path.
    """
    doc = fitz.open(input_path)
    total = doc.page_count

    # Validate range
    if start < 1 or end > total or start > end:
        raise ValueError(
            f"Invalid page range {start}-{end}. "
            f"The PDF has {total} pages (1-{total})."
        )

    # Convert to 0-indexed
    pages = list(range(start - 1, end))

    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=pages[0], to_page=pages[-1])
    new_doc.save(output_path)
    new_doc.close()
    doc.close()

    print(f"✅ تم حفظ الصفحات {start} → {end} في: {output_path}")
    print(f"   عدد الصفحات المستخرجة: {end - start + 1}")


if __name__ == "__main__":
    extract_pages(INPUT_PDF, OUTPUT_PDF, START_PAGE, END_PAGE)
