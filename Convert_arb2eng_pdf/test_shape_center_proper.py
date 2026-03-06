import fitz

doc = fitz.open("book_0.pdf")
page = doc[0]

paths = page.get_drawings()
print(f"Found {len(paths)} drawing paths on page 1")

shapes = []
for p in paths:
    r = p["rect"]
    if r.width < page.rect.width * 0.9 and r.width > 5 and r.height > 5:
        shapes.append(r)

print(f"Filtered down to {len(shapes)} probable boxes/shapes.")

def center_rect_in_shape(text_width, text_height, shape_rect):
    new_x0 = shape_rect.x0 + (shape_rect.width / 2.0) - (text_width / 2.0)
    new_y0 = shape_rect.y0 + (shape_rect.height / 2.0) - (text_height / 2.0)
    return fitz.Rect(new_x0, new_y0, new_x0 + text_width, new_y0 + text_height)

text_dict = page.get_text("dict")
for block in text_dict["blocks"]:
    if block["type"] != 0: continue
    for line in block["lines"]:
        for span in line["spans"]:
            txt = span["text"].strip()
            if txt in ["A", "B", "C", "D"] or "Legend" in txt or "training" in txt.lower():
                r = fitz.Rect(span["bbox"])
                print(f"Target Text: '{txt}' at {r}")
                for s in shapes:
                    if r.intersects(s):
                        print(f"  -> Hits shape: {s}")
                        print(f"  -> Centered pos: {center_rect_in_shape(fitz.get_text_length(txt, fontname='Times-Roman', fontsize=span['size']), span['size'], s)}")
