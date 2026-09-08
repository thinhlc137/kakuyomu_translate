import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
}

def get_novel_info(work_id: str):
    """Lấy tiêu đề tác phẩm và danh sách link toàn bộ các chương."""
    work_id = work_id.strip().rstrip("/").split("/")[-1]
    
    url = f"https://kakuyomu.jp/works/{work_id}"
    res = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    
    title_el = soup.select_one("#workTitle") or soup.select_one("h1")
    novel_title = title_el.get_text(strip=True) if title_el else f"Novel_{work_id}"
    
    chapters = []
    seen_urls = set()
    
    # Danh sách các nút bấm / văn bản điều hướng của Kakuyomu cần loại trừ
    exclude_titles = {"1話目から読む", "最初から読む", "続きを読む", "最新話を読む"}

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/episodes/" in href:
            full_url = f"https://kakuyomu.jp{href}" if href.startswith("/") else href
            title = a.get_text(strip=True)
            
            # Chỉ lấy link nếu chưa trùng, có tiêu đề và không phải nút điều hướng
            if full_url not in seen_urls and title and title not in exclude_titles:
                chapters.append({
                    "title": title,
                    "url": full_url
                })
                seen_urls.add(full_url)
                    
    return novel_title, chapters

def get_chapter_content(chapter_url: str):
    """Trích xuất tiêu đề và nội dung đoạn văn của 1 chương."""
    res = httpx.get(chapter_url, headers=HEADERS, timeout=15, follow_redirects=True)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Lấy tiêu đề chương
    title_el = (
        soup.select_one(".widget-episodeTitle") or 
        soup.select_one("header h1") or 
        soup.select_one("h1")
    )
    title = title_el.get_text(strip=True) if title_el else "Không có tiêu đề"
    
    # Lấy nội dung các đoạn văn bản
    body_container = (
        soup.select_one(".widget-episodeBody") or 
        soup.select_one("[class*='widget-episodeBody']") or
        soup.select_one(".js-episode-body")
    )
    
    if body_container:
        paragraphs = [p.get_text() for p in body_container.select("p")]
    else:
        # Dự phòng quét toàn bộ thẻ p trong bài
        paragraphs = [p.get_text() for p in soup.select("p")]
        
    content = "\n".join(paragraphs)
    return title, content