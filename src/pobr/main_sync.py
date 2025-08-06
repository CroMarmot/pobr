import json
import logging
import re
from pathlib import Path

from paddleocr import PaddleOCR


def append_urls_to_json(urls: list[str], file_path: str) -> None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
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

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(updated_urls, ensure_ascii=False, indent=2))


def main() -> None:
    pocr = PaddleOCR(
        lang="ch",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )

    def ocr_scan(image_path: str | Path):
        return list(pocr.predict(str(image_path))[0]["rec_texts"])

    def ocr_and_extract_links():
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
                yield ocr_scan(str(img_path))  # 直接调用，无需 await
            except Exception:
                logging.exception("Error")

    # 使用普通 for 循环替代 async for
    for new_links in ocr_and_extract_links():
        print(f"{len(new_links)=}")
        append_urls_to_json(new_links, "bug.json")
        print("append success")


if __name__ == "__main__":
    main()  # 直接调用 main，无需 asyncio.run