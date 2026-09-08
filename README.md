# Kakuyomu Web Novel Translator (Japanese -> Vietnamese)

Tool tự động cào (crawl), dịch thuật ngữ cảnh cao cấp bằng **Gemini AI** (kèm Fallback Engine thông minh) và tự động đóng gói tiểu thuyết thành file **EPUB** có mục lục hoàn chỉnh.

---

## Tính năng nổi bật

- **Cào tự động (Crawler)**: Tải toàn bộ danh sách chương, tiêu đề và nội dung nguyên tác từ [Kakuyomu](https://kakuyomu.jp) theo ID truyện.
- **Dịch thuật AI chuẩn Light Novel**: Sử dụng các model Gemini tiên tiến (`gemini-3.5-flash-lite`, `gemini-flash-latest`,...) để chuyển ngữ mượt mà sang tiếng Việt.
- **Bảo mật bí mật cá nhân**: API Key và System Prompt riêng được cách ly hoàn toàn khỏi Git qua `.gitignore`.
- **Semantic Masking (Chống chặn nội dung)**: Tự động xử lý các từ khóa nhạy cảm học đường để tránh kích hoạt nhầm bộ lọc an toàn của Google.
- **Cơ chế Model Pool & Auto-Fallback**:
  - Tự động luân chuyển model khi gặp giới hạn hạn mức (Rate Limit / Quota).
  - Tự động kích hoạt Fallback Translator khi bị AI từ chối, đảm bảo không bị sót bất kỳ chương nào.
- **Tính năng Resume**: Tự động nhận diện các chương đã dịch sẵn để nạp tiếp mà không tốn thêm quota.
- **Xuất file chuẩn**: Tự động lưu từng chương thành file `.md` và đóng gói toàn bộ tác phẩm thành file `.epub` có mục lục chuẩn.

---

## Cài đặt & Hướng dẫn sử dụng

### 1. Cài đặt môi trường

Yêu cầu Python 3.10+:

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
# Trên Windows:
.venv\Scripts\activate
# Trên Linux/macOS:
source .venv/bin/activate

# Cài đặt thư viện phụ thuộc
pip install -r requirements.txt
```

### 2. Cấu hình API Key & System Prompt riêng

1. **Cấu hình API Key**:
   Sao chép file `.env.example` thành `.env` và điền key của bạn:
   ```bash
   cp .env.example .env
   ```
   Mở file `.env` và dán Gemini API Key từ [Google AI Studio](https://aistudio.google.com):
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

2. **(Tùy chọn) Cấu hình System Prompt riêng**:
   - Nếu muốn dùng văn phong, quy tắc dịch hoặc quy định xưng hô riêng, bạn chỉ cần tạo/chỉnh sửa file:
     ```bash
     cp system_prompt.example.txt system_prompt.txt
     ```
   - Chỉnh sửa nội dung prompt trong `system_prompt.txt`.
   - Khi chạy, tool sẽ tự động ưu tiên nạp nội dung từ `system_prompt.txt`.

### 3. Chạy chương trình

```bash
python main.py
```

Nhập ID tác phẩm (chuỗi số trong URL `https://kakuyomu.jp/works/<WORK_ID>`), chọn khoảng chương cần dịch và để tool tự động hoàn thành!

---

## Cấu trúc thư mục

```text
├── .env                     # Chứa API Key cá nhân 
├── .env.example             # File mẫu cấu hình biến môi trường
├── system_prompt.txt        # System Prompt riêng của bạn
├── system_prompt.example.txt# File mẫu System Prompt công khai trên Git
├── .gitignore               # Danh sách file và thư mục loại trừ khỏi Git
├── config.py                # Cấu hình nạp key, model, prompt tự động và glossary
├── crawler.py               # Module cào dữ liệu từ Kakuyomu
├── translator.py            # Module dịch thuật Gemini + Fallback Engine
├── exporter.py              # Module lưu file Markdown & đóng gói EPUB
├── main.py                  # Điểm khởi chạy chương trình (CLI)
└── requirements.txt         # Danh sách thư viện cần thiết
```
