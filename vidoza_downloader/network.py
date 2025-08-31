import aiohttp
from fake_useragent import UserAgent

ua = UserAgent()

def get_default_headers() -> dict:
    """
    Mengembalikan header standar untuk permintaan awal, meniru browser.
    Logika ini diambil dari skrip run.py untuk konsistensi.
    """
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "DNT": "1",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Mode": "navigate",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": ua.random,
    }

def get_embed_headers(video_id: str) -> dict:
    """
    Mengembalikan header yang diperlukan untuk mengakses halaman embed.
    """
    headers = get_default_headers()
    headers.update({
        "Referer": f"https://videq.fit/", # Sesuaikan domain Referer ini jika terjadi error 403 (Forbidden).
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Dest": "iframe",
        "Host": "embed.video-src.com",
    })
    return headers

def get_download_headers() -> dict:
    """
    Mengembalikan header yang diperlukan untuk mengunduh file video.
    """
    return {
        "Accept-Language": "id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://embed.video-src.com/",
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Host": "img.video-src.com",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Dest": "video",
        "Sec-Fetch-Mode": "no-cors",
        "Connection": "keep-alive",
        "User-Agent": ua.random,
        "Range": "bytes=0-",
    }

async def get_session() -> aiohttp.ClientSession:
    """
    Membuat dan mengembalikan aiohttp.ClientSession.
    """
    return aiohttp.ClientSession()