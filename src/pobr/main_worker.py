import asyncio
import json
import logging
import re
import threading
from pathlib import Path
from queue import Queue, Empty

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


class OCRWorker:
    def __init__(self):
        self._loop = asyncio.get_running_loop()
        self._input_queue = Queue()
        self.thread = threading.Thread(target=self._worker_loop, daemon=False)
        self.thread.start()

    def _worker_loop(self):
        # ✅ 在工具线程中创建 PaddleOCR 实例
        pocr = PaddleOCR(
            lang="ch",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

        while True:
            try:
                # 获取任务
                future, image_path = self._input_queue.get()
                if future is None:  # 退出信号
                    break

                # 执行 OCR（在工具线程中）
                try:
                    result = list(pocr.predict(str(image_path))[0]["rec_texts"])
                    # 使用 call_soon_threadsafe 把结果送回 asyncio 事件循环
                    self._loop.call_soon_threadsafe(future.set_result, result)
                except Exception as e:
                    self._loop.call_soon_threadsafe(future.set_exception, e)

                self._input_queue.task_done()

            except Empty:
                continue
            except Exception as e:
                logging.error(f"OCRWorker 线程异常: {e}", exc_info=True)

    def ocr_scan(self, image_path: str | Path) -> asyncio.Future:
        future = self._loop.create_future()
        self._input_queue.put_nowait((future, image_path))
        return future

    def close(self):
        self._input_queue.put_nowait((None, None))  # 发送退出信号


async def main() -> None:
    # 创建专用 OCR 工具线程
    ocr_worker = OCRWorker()

    try:
        # 定义 ocr_scan 接口，与原来一致
        async def ocr_scan(image_path: str | Path):
            return await ocr_worker.ocr_scan(image_path)

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
                    yield await ocr_scan(img_path)  
                except Exception:
                    logging.exception("Error")

        async for new_links in ocr_and_extract_links():
            print(f"{len(new_links)=}")
            await append_urls_to_json(new_links, "bug.json")
            print("append success")

    finally:
        ocr_worker.close()


if __name__ == "__main__":
    asyncio.run(main())