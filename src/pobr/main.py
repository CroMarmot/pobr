import asyncio
import json
import logging
import re
from pathlib import Path

import aiofiles
from paddleocr import PaddleOCR


async def append_urls_to_json(urls: list[str], file_path: str) -> None:
    try:
        async with aiofiles.open(file_path, encoding="utf-8") as f:
            content = await f.read()
            if content.strip():  # 文件不为空
                existing_urls = json.loads(content)
                if not isinstance(existing_urls, list):
                    existing_urls = []
            else:  # 文件为空
                existing_urls = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_urls = []

    print(f"{len(existing_urls)=}")
    updated_urls = existing_urls + [url for url in urls if url not in existing_urls]
    print(f"{len(updated_urls)=}")

    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(updated_urls, ensure_ascii=False, indent=2))


async def main() -> None:
    pocr = PaddleOCR(
        lang="ch",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )

    def ocr_scan(image_path: str | Path):
        return list(pocr.predict(str(image_path))[0]["rec_texts"])

    async def ocr_and_extract_links():
        current_dir = Path()
        files = [
            p
            for p in current_dir.iterdir()
            if p.is_file() and re.fullmatch(r"shot_.*\.png", p.name)
        ]
        print(f"{len(files)=}")

        for idx, img_path in enumerate(files, start=1):
            print(f"OCR {idx}/{len(files)} {img_path}")
            try:
                yield await asyncio.to_thread(ocr_scan, str(img_path))
            except Exception:
                logging.exception("Error")

    async for new_links in ocr_and_extract_links():
        print(f"{len(new_links)=}")
        await append_urls_to_json(new_links, "bug.json")
        print(f"append success")


if __name__ == "__main__":
    asyncio.run(main())
