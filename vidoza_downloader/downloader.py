import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from logging import Logger
from urllib.parse import urlparse

import aiohttp
from tqdm.asyncio import tqdm

from . import network, parser, utils

class VideqDownloader:
    """
    Kelas utama untuk menangani logika pengunduhan video dari Videq.
    Menggunakan aiohttp untuk permintaan asinkron dan tqdm untuk progress bar.
    """

    def __init__(self, session: aiohttp.ClientSession, download_path: Path, logger: Logger):
        """
        Inisialisasi downloader.

        Args:
            session (aiohttp.ClientSession): Sesi klien HTTP untuk digunakan.
            download_path (Path): Objek Path menuju direktori unduhan.
            logger (Logger): Instance logger yang telah dikonfigurasi.
        """
        self.session = session
        self.download_path = download_path
        self.logger = logger
        self.download_path.mkdir(parents=True, exist_ok=True)

    async def process_urls(self, urls: List[str]) -> None:
        """
        Memproses daftar URL secara konkuren.

        Args:
            urls (List[str]): Daftar string URL video yang akan diunduh.
        """
        tasks = [self.download_video_from_url(url) for url in urls]
        await asyncio.gather(*tasks)

    async def download_video_from_url(self, url: str) -> None:
        """
        Orkestrasi lengkap untuk mengunduh satu video dari URL yang diberikan.
        """
        self.logger.info(f"Memulai proses untuk tautan: {url}")

        video_id = self._extract_id_from_url(url)
        if not video_id:
            self.logger.error(f"Gagal mengekstrak ID video dari tautan: {url}")
            return

        self.logger.info(f"ID Video terdeteksi: {video_id}")

        info_url = self._construct_info_url(url, video_id)
        video_info = await self._get_video_info(info_url)

        object_key = await self._get_object_key(video_id, url)
        if not object_key:
            self.logger.error(f"Tidak dapat mengambil kunci objek untuk ID: {video_id}. Melewatkan unduhan.")
            return
        
        base_filename = video_info.get('title') if video_info else video_id

        if base_filename and base_filename.lower().endswith('.mp4'):
            base_filename = base_filename[:-4]

        sanitized_filename = utils.sanitize_filename(f"{base_filename}.mp4")
        file_path = self.download_path / sanitized_filename

        if file_path.exists():
            self.logger.warning(f"Berkas '{sanitized_filename}' sudah ada. Melewatkan unduhan.")
            return

        download_url = f"https://img.video-src.com/{object_key}"
        await self._stream_download(download_url, file_path)

    def _extract_id_from_url(self, url: str) -> Optional[str]:
        """Mengekstrak ID dari path URL."""
        try:
            return Path(urlparse(url).path).name
        except Exception:
            return None

    def _construct_info_url(self, original_url: str, video_id: str) -> str:
        """Membuat URL halaman informasi ('/d/') dari URL asli."""
        parsed_url = urlparse(original_url)

        info_path = f"/d/{video_id}"
        return parsed_url._replace(path=info_path).geturl()

    async def _get_video_info(self, url: str) -> Dict[str, Any]:
        """Mengambil dan mem-parsing metadata video."""
        self.logger.debug(f"Mengambil informasi dari: {url}")
        try:
            async with self.session.get(url, headers=network.get_default_headers(), allow_redirects=True) as response:
                if response.status == 200:
                    content = await response.text()
                    info = parser.parse_video_info(content)
                    if info:
                        self.logger.debug(f"Informasi video ditemukan: {info}")
                        return info
                self.logger.warning(f"Gagal mendapatkan informasi video dari {url} (Status: {response.status})")
        except aiohttp.ClientError as e:
            self.logger.error(f"Kesalahan jaringan saat mengambil info video: {e}")
        return {}

    async def _get_object_key(self, video_id: str, original_url: str) -> Optional[str]:
        """Mengambil objectKey dari halaman embed."""
        embed_url = f"https://embed.video-src.com/vplayer?id={video_id}"
        self.logger.debug(f"Mengambil objectKey dari: {embed_url}")
        try:
            headers = network.get_embed_headers(video_id)
            parsed_original = urlparse(original_url)
            headers.update({"Referer": f"{parsed_original.scheme}://{parsed_original.netloc}/"})
            async with self.session.get(embed_url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    key = parser.extract_object_key(content)
                    if key:
                        self.logger.debug(f"ObjectKey ditemukan: {key}")
                        return key
                self.logger.warning(f"Gagal mendapatkan objectKey (Status: {response.status})")
        except aiohttp.ClientError as e:
            self.logger.error(f"Kesalahan jaringan saat mengambil objectKey: {e}")
        return None

    async def _stream_download(self, url: str, file_path: Path) -> None:
        """Mengunduh file secara stream dengan progress bar."""
        self.logger.info(f"Mengunduh ke: {file_path.name}")
        try:
            headers = network.get_download_headers()
            async with self.session.get(url, headers=headers) as response:
                if response.status not in (200, 206):
                    self.logger.error(f"Gagal memulai unduhan. Server merespons dengan status {response.status}")
                    return

                total_size = int(response.headers.get('content-length', 0))
                
                with open(file_path, 'wb') as f, tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=file_path.name,
                    ncols=80
                ) as bar:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        bar.update(len(chunk))
            
            self.logger.success(f"Video '{file_path.name}' berhasil diunduh.")
        except aiohttp.ClientError as e:
            self.logger.error(f"Terjadi kesalahan jaringan saat mengunduh '{file_path.name}': {e}")
            if file_path.exists():
                os.remove(file_path)
        except Exception as e:
            self.logger.error(f"Terjadi kesalahan tak terduga saat mengunduh '{file_path.name}': {e}")
            if file_path.exists():
                os.remove(file_path)