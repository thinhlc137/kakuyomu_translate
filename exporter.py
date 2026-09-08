import os
from ebooklib import epub

def save_markdown(output_dir: str, chapter_idx: int, content: str):
    """Lưu từng chương thành file markdown."""
    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"Nội dung chương {chapter_idx} không hợp lệ hoặc rỗng (kiểu: {type(content).__name__}). Không thể lưu file.")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"chuong_{chapter_idx:03d}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

def build_epub(novel_title: str, chapters_data: list, output_filepath: str):
    """Đóng gói danh sách chương thành file EPUB có mục lục hoàn chỉnh."""
    book = epub.EpubBook()
    book.set_identifier(f"id_{abs(hash(novel_title))}")
    book.set_title(novel_title)
    book.set_language("vi")

    spine = ["nav"]
    toc = []

    for idx, chap in enumerate(chapters_data, start=1):
        c = epub.EpubHtml(
            title=chap["title"],
            file_name=f"chap_{idx:03d}.xhtml",
            lang="vi"
        )
        
        # Chuyển đổi đoạn văn bản sang định dạng HTML
        html_paragraphs = "".join([f"<p>{p}</p>" for p in chap["content"].split("\n") if p.strip()])
        c.content = f"<h2>{chap['title']}</h2>{html_paragraphs}"
        
        book.add_item(c)
        spine.append(c)
        toc.append(c)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine

    epub.write_epub(output_filepath, book, {})
    print(f"\n[Thành công] Đã xuất file sách EPUB: {output_filepath}")