import argparse
import asyncio
from pathlib import Path
import platform
import sys

from . import downloader, network
from .logger import setup_logger

def create_arg_parser() -> argparse.ArgumentParser:
    """
    Membuat dan mengonfigurasi parser untuk argumen baris perintah.
    """
    parser = argparse.ArgumentParser(
        description="Unduh video dari tautan Videq, Vidoza, dan host serupa lainnya dengan mudah melalui baris perintah.",
        epilog="Contoh: python -m vidoza_downloader.main https://videq.fit/e/z40jeu954mk5 -o VideoSaya",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "tautan",
        nargs='+',
        help="Satu atau lebih tautan video. Pisahkan dengan spasi atau koma.\nContoh: tautan1 tautan2,tautan3"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path.cwd(),
        help="Direktori keluaran untuk menyimpan video. Default: direktori saat ini."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Aktifkan mode verbose untuk menampilkan log debug."
    )
    return parser

async def main():
    """
    Fungsi asinkron utama untuk menjalankan aplikasi.
    """
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    log = setup_logger(args.verbose)

    all_urls = []
    for item in args.tautan:
        all_urls.extend(u.strip() for u in item.split(',') if u.strip())
    
    if not all_urls:
        log.error("Tidak ada tautan valid yang diberikan.")
        sys.exit(1)

    log.info(f"Ditemukan {len(all_urls)} tautan untuk diproses.")
    log.info(f"Direktori unduhan diatur ke: {args.output.resolve()}")

    async with await network.get_session() as session:
        videq_dl = downloader.VideqDownloader(
            session=session, 
            download_path=args.output,
            logger=log
        )
        try:
            await videq_dl.process_urls(all_urls)
        except Exception as e:
            log.error(f"Terjadi kesalahan yang tidak terduga di level atas: {e}")
    
    log.info("Semua proses telah selesai.")

def run():
    """Wrapper untuk menjalankan loop asyncio."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh pengguna.")
        sys.exit(0)

if __name__ == "__main__":
    run()