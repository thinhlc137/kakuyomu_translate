import time
import os
import re
from crawler import get_novel_info, get_chapter_content
from translator import translate_text, ProhibitedContentError
from exporter import save_markdown, build_epub

def run():
    print("=== TOOL CÀO & DỊCH TRUYỆN KAKUYOMU ===")
    work_id = input("Nhập ID truyện (dãy số trong link https://kakuyomu.jp/works/...): ").strip()
    
    print("\nĐang tải danh sách chương từ Kakuyomu...")
    novel_title, all_chapters = get_novel_info(work_id)
    total = len(all_chapters)
    print(f"Tác phẩm: {novel_title}")
    print(f"Tổng số chương tìm thấy: {total}")

    start_chap = int(input(f"Nhập chương bắt đầu (1 -> {total}): ") or "1")
    end_chap = int(input(f"Nhập chương kết thúc ({start_chap} -> {total}): ") or str(total))

    # Làm sạch tên file/thư mục tránh ký tự đặc biệt trên Windows
    safe_title = re.sub(r'[\\/*?:"<>|]', "_", novel_title)
    novel_dir = os.path.join("output", f"{safe_title}_{work_id}")
    processed_chapters = []

    for idx in range(start_chap, end_chap + 1):
        chap_info = all_chapters[idx - 1]
        
        # 0. Kiểm tra nếu chương đã được dịch thành công từ trước (Resume feature)
        md_file = os.path.join(novel_dir, f"chuong_{idx:03d}.md")
        if os.path.exists(md_file) and os.path.getsize(md_file) > 100:
            print(f"\n[{idx}/{end_chap}] Chương {idx} đã có sẵn file trên máy, tự động nạp...")
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    translated = f.read()
                first_line = translated.split("\n")[0].replace("#", "").strip()
                processed_chapters.append({
                    "title": first_line if first_line else f"Chương {idx}",
                    "content": translated
                })
                continue
            except Exception:
                pass

        print(f"\n[{idx}/{end_chap}] Đang cào: {chap_info['title']}")
        
        # 1. Cào raw
        try:
            raw_title, raw_body = get_chapter_content(chap_info["url"])
        except Exception as e:
            print(f"Lỗi khi cào dữ liệu chương {idx}: {e}")
            continue
        if not raw_body or not raw_body.strip():
            print(f"Bỏ qua chương {idx} ({chap_info['title']}) vì không tìm thấy nội dung văn bản.")
            continue
        
        # 2. Dịch
        print(f"[{idx}/{end_chap}] Đang dịch qua Gemini API...")
        try:
            translated = translate_text(raw_title, raw_body)
        except ProhibitedContentError as e:
            print(f"⚠️ Chương {idx} bị Google chặn nội dung nhạy cảm.")
            # Ghi nhận vào file skipped_chapters.txt
            os.makedirs(novel_dir, exist_ok=True)
            skipped_file = os.path.join(novel_dir, "skipped_chapters.txt")
            with open(skipped_file, "a", encoding="utf-8") as sf:
                sf.write(f"Chương {idx}: {chap_info['title']} - {e}\n")
            
            # Tạo nội dung giữ chỗ kèm raw gốc để không hỏng cấu trúc mục lục EPUB
            translated = f"# {chap_info['title']}\n\n*(Chương này chứa nội dung bị bộ lọc Google Gemini từ chối dịch: {e})*\n\n[Raw tiếng Nhật]:\n\n{raw_body}"
        except Exception as e:
            print(f"Lỗi khi dịch chương {idx}: {e}")
            continue

        if not translated or not translated.strip():
            print(f"Cảnh báo: Bản dịch chương {idx} rỗng hoặc không hợp lệ, bỏ qua.")
            continue

        # 3. Lưu markdown
        try:
            save_markdown(novel_dir, idx, translated)
        except Exception as e:
            print(f"Lỗi khi lưu markdown chương {idx}: {e}")
            continue
        
        # Lưu dữ liệu để lát đóng gói EPUB
        first_line = translated.split("\n")[0].replace("#", "").strip()
        processed_chapters.append({
            "title": first_line if first_line else f"Chương {idx}",
            "content": translated
        })
        
        print(f"Hoàn thành chương {idx}!")
        
        # Nghỉ 4 giây giữa các chương để tôn trọng giới hạn 15 RPM của Gemini Free Tier
        if idx < end_chap:
            time.sleep(4)

    # 4. Xuất file EPUB tổng hợp
    if processed_chapters:
        epub_filename = os.path.join("output", f"{safe_title}_{start_chap}-{end_chap}.epub")
        build_epub(novel_title, processed_chapters, epub_filename)

if __name__ == "__main__":
    run()