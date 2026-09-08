import os
from dotenv import load_dotenv

# Tự động nạp biến môi trường từ file .env
load_dotenv()

# Lấy Gemini API Key từ biến môi trường hoặc file .env (không hardcode vào mã nguồn)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model khuyến nghị: Tốc độ cao, context dài, gói free 15 requests/phút, hạn mức ngày lớn
MODEL_NAME = "gemini-3.5-flash"

# Bảng thuật ngữ cố định (Bổ sung tên nhân vật, địa danh, chiêu thức tùy theo từng bộ truyện)
GLOSSARY = {
    # "Tên tiếng Nhật": "Tên dịch tiếng Việt",
}

def load_system_prompt() -> str:
    """Tự động nạp system prompt riêng từ file system_prompt.txt (đã được giấu khỏi Git).
    Nếu không có, sẽ tự động nạp từ system_prompt.example.txt hoặc dùng prompt mặc định."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Ưu tiên biến môi trường nếu có chỉ định đường dẫn cụ thể
    env_prompt_path = os.getenv("SYSTEM_PROMPT_PATH", "")
    if env_prompt_path and os.path.exists(env_prompt_path):
        with open(env_prompt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content

    # 2. Ưu tiên file prompt riêng bí mật (nằm trong .gitignore)
    private_file = os.path.join(base_dir, "system_prompt.txt")
    if os.path.exists(private_file):
        with open(private_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
                
    # 3. Dự phòng nạp từ file mẫu public (được đẩy lên Git làm mẫu)
    example_file = os.path.join(base_dir, "system_prompt.example.txt")
    if os.path.exists(example_file):
        with open(example_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
                
    # 4. Mặc định cơ bản
    return "Bạn là một dịch giả tiếng Nhật sang tiếng Việt giàu kinh nghiệm. Hãy dịch văn bản sau sang tiếng Việt mượt mà."

# Prompt định hình văn phong
SYSTEM_PROMPT = load_system_prompt()
