import fitz

doc = fitz.open("book_30.pdf")
page = doc[0]

print("--- Translated Page Streams ---")
for xref in page.get_contents():
    print(doc.xref_stream(xref)[:500])

print("\n--- Form XObjects ---")
for xo in page.get_xobjects():
    xref = xo[0]
    name = xo[1]
    if doc.xref_is_stream(xref):
        print(f"XObject {name} (xref {xref}):")
        stream = doc.xref_stream(xref)
        if stream:
            print(stream[:500])
