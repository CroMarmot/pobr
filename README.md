# paddle ocr bug reproduce

TLDR: 目前25-08-16 [暂时不要在线程中操作全局的preditor](https://github.com/PaddlePaddle/PaddleOCR/issues/15621#issuecomment-2955143480) ，可以单独一个工作线程. (类似main_worker.py)

---


```bash
hatch new pobr
```

add `src/pobr/main.py`

`pyporject.toml`

```diff
- dependencies = []
+ dependencies = [
+     "paddleocr",
+     "paddlepaddle==3.1.0",
+     "setuptools>=60.0",
+     "aiofiles",
+ ]
+[tool.hatch.envs.default.scripts]
+bug = "python src/pobr/main.py"
+bug_sync = "python src/pobr/main_sync.py"
```

add `shot_.*\.png`

```bash
hatch run bug # 目前异步的会报错，概率高，但报错的图片不稳定
hatch run bug_sync
```

## Output

```
$ hatch run bug
信息: 用提供的模式无法找到文件。
C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddle\utils\cpp_extension\extension_utils.py:715: UserWarning: No ccache found. Please be aware that recompiling all source files may be required. You can download and install ccache from: https://github.com/ccache/ccache/blob/master/doc/INSTALL.md
  warnings.warn(warning_message)
Creating model: ('PP-OCRv5_server_det', None)
Using official model (PP-OCRv5_server_det), the model files will be automatically downloaded and saved in C:\Users\yexia\.paddlex\official_models.
Creating model: ('PP-OCRv5_server_rec', None)
Using official model (PP-OCRv5_server_rec), the model files will be automatically downloaded and saved in C:\Users\yexia\.paddlex\official_models.
len(files)=12
OCR 1/12 shot_20250730153228.png
len(new_links)=196
len(existing_urls)=0
len(updated_urls)=196
append success
OCR 2/12 shot_20250730153326.png
len(new_links)=49
len(existing_urls)=196
len(updated_urls)=232
append success
OCR 3/12 shot_20250730153329.png
len(new_links)=137
len(existing_urls)=232
len(updated_urls)=263
append success
OCR 4/12 shot_20250730153333.png
len(new_links)=48
len(existing_urls)=263
len(updated_urls)=291
append success
OCR 5/12 shot_20250730153337.png
[2025-07-30 16:05:48,642] [   ERROR] main.py:57 - Error
Traceback (most recent call last):
  File "C:\Users\yexia\Documents\github\pobr\src\pobr\main.py", line 55, in ocr_and_extract_links
    yield await asyncio.to_thread(ocr_scan, str(img_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\Programs\Python\Python313\Lib\asyncio\threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\Programs\Python\Python313\Lib\concurrent\futures\thread.py", line 59, in run
    result = self.fn(*self.args, **self.kwargs)
  File "C:\Users\yexia\Documents\github\pobr\src\pobr\main.py", line 41, in ocr_scan
    return list(pocr.predict(str(image_path))[0]["rec_texts"])
                ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddleocr\_pipelines\ocr.py", line 208, in predict
    return list(
        self.predict_iter(
    ...<10 lines>...
        )
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\_parallel.py", line 129, in predict
    yield from self._pipeline.predict(
    ...<3 lines>...
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\ocr\pipeline.py", line 350, in predict
    det_results = list(
        self.text_det_model(doc_preprocessor_images, **text_det_params)
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predic    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\ocr\pipeline.py", line 350, in predict
    det_results = list(
        self.text_det_model(doc_preprocessor_images, **text_det_params)
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predic  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\ocr\pipeline.py", line 350, in predict
    det_results = list(
        self.text_det_model(doc_preprocessor_images, **text_det_params)
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predic    det_results = list(
        self.text_det_model(doc_preprocessor_images, **text_det_params)
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predic    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predictor\base_predictor.py", line 211, in __call__
tor\base_predictor.py", line 211, in __call__
    yield from self.apply(input, **kwargs)
    yield from self.apply(input, **kwargs)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predic  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predictor\base_predictor.py", line 267, in apply
    prediction = self.process(batch_data, **kwargs)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\text_detect  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\text_detection\predictor.py", line 105, in process
    batch_preds = self.infer(x=x)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\common\static_infer.py", line 287, in __call__
    pred = self.infer(x)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\common\static_infer.py", line 252, in __call__
    self.predictor.run()
    ~~~~~~~~~~~~~~~~~~^^
RuntimeError: Unknown exception
OCR 6/12 shot_20250730153340.png
len(new_links)=43
len(existing_urls)=291
len(updated_urls)=314
append success
OCR 7/12 shot_20250730153344.png
[2025-07-30 16:06:03,905] [   ERROR] main.py:57 - Error
Traceback (most recent call last):
  File "C:\Users\yexia\Documents\github\pobr\src\pobr\main.py", line 55, in ocr_and_extract_links
    yield await asyncio.to_thread(ocr_scan, str(img_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\Programs\Python\Python313\Lib\asyncio\threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\Programs\Python\Python313\Lib\concurrent\futures\thread.py", line 59, in run
    result = self.fn(*self.args, **self.kwargs)
  File "C:\Users\yexia\Documents\github\pobr\src\pobr\main.py", line 41, in ocr_scan
    return list(pocr.predict(str(image_path))[0]["rec_texts"])
                ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddleocr\_pipelines\ocr.py", line 208, in predict
    return list(
        self.predict_iter(
    ...<10 lines>...
        )
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\_parallel.py", line 129, in predict
    yield from self._pipeline.predict(
    ...<3 lines>...
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\ocr\pipeline.py", line 350, in predict
    det_results = list(
        self.text_det_model(doc_preprocessor_images, **text_det_params)
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predictor\base_predictor.py", line 211, in __call__
    yield from self.apply(input, **kwargs)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predictor\base_predictor.py", line 267, in apply
    prediction = self.process(batch_data, **kwargs)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\text_detection\predictor.py", line 105, in process
    batch_preds = self.infer(x=x)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\common\static_infer.py", line 287, in __call__
    pred = self.infer(x)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\common\static_infer.py", line 252, in __call__
    self.predictor.run()
    ~~~~~~~~~~~~~~~~~~^^
RuntimeError: Unknown exception
OCR 8/12 shot_20250730153347.png
len(new_links)=46
len(existing_urls)=314
len(updated_urls)=339
append success
OCR 9/12 shot_20250730153351.png
len(new_links)=46
len(existing_urls)=339
len(updated_urls)=364
append success
OCR 10/12 shot_20250730153354.png
[2025-07-30 16:06:28,046] [   ERROR] main.py:57 - Error
Traceback (most recent call last):
  File "C:\Users\yexia\Documents\github\pobr\src\pobr\main.py", line 55, in ocr_and_extract_links
    yield await asyncio.to_thread(ocr_scan, str(img_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\Programs\Python\Python313\Lib\asyncio\threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\Programs\Python\Python313\Lib\concurrent\futures\thread.py", line 59, in run
    result = self.fn(*self.args, **self.kwargs)
  File "C:\Users\yexia\Documents\github\pobr\src\pobr\main.py", line 41, in ocr_scan
    return list(pocr.predict(str(image_path))[0]["rec_texts"])
                ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddleocr\_pipelines\ocr.py", line 208, in predict
    return list(
        self.predict_iter(
    ...<10 lines>...
        )
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\_parallel.py", line 129, in predict
    yield from self._pipeline.predict(
    ...<3 lines>...
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\ocr\pipeline.py", line 350, in predict
    det_results = list(
        self.text_det_model(doc_preprocessor_images, **text_det_params)
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predictor\base_predictor.py", line 211, in __call__
    yield from self.apply(input, **kwargs)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predictor\base_predictor.py", line 267, in apply
    prediction = self.process(batch_data, **kwargs)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\text_detection\predictor.py", line 105, in process
    batch_preds = self.infer(x=x)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\common\static_infer.py", line 287, in __call__
    pred = self.infer(x)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\common\static_infer.py", line 252, in __call__
    self.predictor.run()
    ~~~~~~~~~~~~~~~~~~^^
RuntimeError: Unknown exception
OCR 11/12 shot_20250730153358.png
len(new_links)=42
len(existing_urls)=364
len(updated_urls)=387
append success
OCR 12/12 shot_20250730153401.png
[2025-07-30 16:06:40,444] [   ERROR] main.py:57 - Error
Traceback (most recent call last):
  File "C:\Users\yexia\Documents\github\pobr\src\pobr\main.py", line 55, in ocr_and_extract_links
    yield await asyncio.to_thread(ocr_scan, str(img_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\Programs\Python\Python313\Lib\asyncio\threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\Programs\Python\Python313\Lib\concurrent\futures\thread.py", line 59, in run
    result = self.fn(*self.args, **self.kwargs)
  File "C:\Users\yexia\Documents\github\pobr\src\pobr\main.py", line 41, in ocr_scan
    return list(pocr.predict(str(image_path))[0]["rec_texts"])
                ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddleocr\_pipelines\ocr.py", line 208, in predict
    return list(
        self.predict_iter(
    ...<10 lines>...
        )
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\_parallel.py", line 129, in predict
    yield from self._pipeline.predict(
    ...<3 lines>...
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\pipelines\ocr\pipeline.py", line 350, in predict
    det_results = list(
        self.text_det_model(doc_preprocessor_images, **text_det_params)
    )
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predictor\base_predictor.py", line 211, in __call__
    yield from self.apply(input, **kwargs)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\base\predictor\base_predictor.py", line 267, in apply
    prediction = self.process(batch_data, **kwargs)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\text_detection\predictor.py", line 105, in process
    batch_preds = self.infer(x=x)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\common\static_infer.py", line 287, in __call__
    pred = self.infer(x)
  File "C:\Users\yexia\AppData\Local\hatch\env\virtual\pobr\CDbpi3Zz\pobr\Lib\site-packages\paddlex\inference\models\common\static_infer.py", line 252, in __call__
    self.predictor.run()
    ~~~~~~~~~~~~~~~~~~^^
RuntimeError: Unknown exception
```

## Env


```
PS C:\Users\yexia> systeminfo
OS 名称:            Microsoft Windows 11 专业版
OS 版本:            10.0.26100 暂缺 Build 26100
```

```
$ hatch --version
Hatch, version 1.14.1

$ hatch run python --version
Python 3.13.2

$ hatch run pip list | grep paddle
paddleocr                3.1.0
paddlepaddle             3.1.0
paddlex                  3.1.3
```

RAM 16GB

CPU:

```
PS C:\Users\yexia> wmic cpu get name
Name
AMD Ryzen 7 5800H with Radeon Graphics
```

CUDA None

## Ubuntu (RAM 38GB)

```
> hatch --version
Hatch, version 1.14.1
> hatch run python --version
Python 3.12.3
> hatch run pip list | rg paddle
paddleocr                3.1.0
paddlepaddle             3.1.0
paddlex                  3.1.3
```


```
OS: Ubuntu 24.04.2 LTS x86_64 
Host: HP Pavilion Notebook PC 
Kernel: 6.8.0-64-generic 
Uptime: 16 days, 17 hours, 9 mins 
Packages: 2818 (dpkg), 12 (snap) 
Shell: bash 5.2.21 
Resolution: 1920x1080 
Terminal: node 
CPU: Intel i7-7700HQ (8) @ 3.800GHz 
GPU: NVIDIA GeForce GTX 1050 Mobile 
GPU: Intel HD Graphics 630 
Memory: 17170MiB / 39872MiB 
```

没有使用GPU (nvidia-smi 没有看到使用)

async 依然会报错, 同样的错误, 出错率也很高, 内存一半都没用到

sync 测了几次没有报错

```bash
for i in {1..3};do hatch run bug && hatch run bug_sync; done
```

报错例子

```
hatch run bug
/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddle/utils/cpp_extension/extension_utils.py:715: UserWarning: No ccache found. Please be aware that recompiling all source files may be required. You can download and install ccache from: https://github.com/ccache/ccache/blob/master/doc/INSTALL.md
  warnings.warn(warning_message)
Creating model: ('PP-OCRv5_server_det', None)
Using official model (PP-OCRv5_server_det), the model files will be automatically downloaded and saved in /home/esakura/.paddlex/official_models.
Creating model: ('PP-OCRv5_server_rec', None)
Using official model (PP-OCRv5_server_rec), the model files will be automatically downloaded and saved in /home/esakura/.paddlex/official_models.
len(files)=12
OCR 1/12 shot_20250730153401.png
len(new_links)=51
len(existing_urls)=479
len(updated_urls)=479
append success
OCR 2/12 shot_20250730153333.png
len(new_links)=48
len(existing_urls)=479
len(updated_urls)=479
append success
OCR 3/12 shot_20250730153340.png
[2025-08-06 16:39:15,887] [   ERROR] main.py:57 - Error
Traceback (most recent call last):
  File "/data/github/pobr/src/pobr/main.py", line 55, in ocr_and_extract_links
    yield await asyncio.to_thread(ocr_scan, str(img_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/data/github/pobr/src/pobr/main.py", line 41, in ocr_scan
    return list(pocr.predict(str(image_path))[0]["rec_texts"])
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddleocr/_pipelines/ocr.py", line 208, in predict
    return list(
           ^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/pipelines/_parallel.py", line 129, in predict
    yield from self._pipeline.predict(
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/pipelines/ocr/pipeline.py", line 350, in predict
    det_results = list(
                  ^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 211, in __call__
    yield from self.apply(input, **kwargs)
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 267, in apply
    prediction = self.process(batch_data, **kwargs)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/text_detection/predictor.py", line 105, in process
    batch_preds = self.infer(x=x)
                  ^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/common/static_infer.py", line 287, in __call__
    pred = self.infer(x)
           ^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/common/static_infer.py", line 252, in __call__
    self.predictor.run()
RuntimeError: std::exception
OCR 4/12 shot_20250730153337.png
len(new_links)=44
len(existing_urls)=479
len(updated_urls)=479
append success
OCR 5/12 shot_20250730153344.png
len(new_links)=35
len(existing_urls)=479
len(updated_urls)=479
append success
OCR 6/12 shot_20250730153326.png
len(new_links)=49
len(existing_urls)=479
len(updated_urls)=479
append success
OCR 7/12 shot_20250730153228.png
len(new_links)=196
len(existing_urls)=479
len(updated_urls)=479
append success
OCR 8/12 shot_20250730153329.png
[2025-08-06 16:41:19,681] [   ERROR] main.py:57 - Error
Traceback (most recent call last):
  File "/data/github/pobr/src/pobr/main.py", line 55, in ocr_and_extract_links
    yield await asyncio.to_thread(ocr_scan, str(img_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/data/github/pobr/src/pobr/main.py", line 41, in ocr_scan
    return list(pocr.predict(str(image_path))[0]["rec_texts"])
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddleocr/_pipelines/ocr.py", line 208, in predict
    return list(
           ^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/pipelines/_parallel.py", line 129, in predict
    yield from self._pipeline.predict(
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/pipelines/ocr/pipeline.py", line 350, in predict
    det_results = list(
                  ^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 211, in __call__
    yield from self.apply(input, **kwargs)
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 267, in apply
    prediction = self.process(batch_data, **kwargs)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/text_detection/predictor.py", line 105, in process
    batch_preds = self.infer(x=x)
                  ^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/common/static_infer.py", line 287, in __call__
    pred = self.infer(x)
           ^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/common/static_infer.py", line 252, in __call__
    self.predictor.run()
RuntimeError: std::exception
OCR 9/12 shot_20250730153354.png
len(new_links)=37
len(existing_urls)=479
len(updated_urls)=479
append success
OCR 10/12 shot_20250730153358.png
[2025-08-06 16:41:53,582] [   ERROR] main.py:57 - Error
Traceback (most recent call last):
  File "/data/github/pobr/src/pobr/main.py", line 55, in ocr_and_extract_links
    yield await asyncio.to_thread(ocr_scan, str(img_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/data/github/pobr/src/pobr/main.py", line 41, in ocr_scan
    return list(pocr.predict(str(image_path))[0]["rec_texts"])
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddleocr/_pipelines/ocr.py", line 208, in predict
    return list(
           ^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/pipelines/_parallel.py", line 129, in predict
    yield from self._pipeline.predict(
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/pipelines/ocr/pipeline.py", line 350, in predict
    det_results = list(
                  ^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 211, in __call__
    yield from self.apply(input, **kwargs)
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 267, in apply
    prediction = self.process(batch_data, **kwargs)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/text_detection/predictor.py", line 105, in process
    batch_preds = self.infer(x=x)
                  ^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/common/static_infer.py", line 287, in __call__
    pred = self.infer(x)
           ^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/common/static_infer.py", line 252, in __call__
    self.predictor.run()
RuntimeError: std::exception
OCR 11/12 shot_20250730153351.png
len(new_links)=46
len(existing_urls)=479
len(updated_urls)=479
append success
OCR 12/12 shot_20250730153347.png
[2025-08-06 16:42:30,713] [   ERROR] main.py:57 - Error
Traceback (most recent call last):
  File "/data/github/pobr/src/pobr/main.py", line 55, in ocr_and_extract_links
    yield await asyncio.to_thread(ocr_scan, str(img_path))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/data/github/pobr/src/pobr/main.py", line 41, in ocr_scan
    return list(pocr.predict(str(image_path))[0]["rec_texts"])
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddleocr/_pipelines/ocr.py", line 208, in predict
    return list(
           ^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/pipelines/_parallel.py", line 129, in predict
    yield from self._pipeline.predict(
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/pipelines/ocr/pipeline.py", line 350, in predict
    det_results = list(
                  ^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 211, in __call__
    yield from self.apply(input, **kwargs)
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 267, in apply
    prediction = self.process(batch_data, **kwargs)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/text_detection/predictor.py", line 105, in process
    batch_preds = self.infer(x=x)
                  ^^^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/common/static_infer.py", line 287, in __call__
    pred = self.infer(x)
           ^^^^^^^^^^^^^
  File "/home/esakura/.local/share/hatch/env/virtual/pobr/0wCVYwZv/pobr/lib/python3.12/site-packages/paddlex/inference/models/common/static_infer.py", line 252, in __call__
    self.predictor.run()
RuntimeError: std::exception
```

## Diff

```diff
diff -u -w main.py main_sync.py
--- main.py     2025-08-16 05:41:20.874672673 +0800
+++ main_sync.py        2025-08-06 16:30:18.724666868 +0800
@@ -1,17 +1,15 @@
-import asyncio
 import json
 import logging
 import re
 from pathlib import Path
 
-import aiofiles
 from paddleocr import PaddleOCR
 
 
-async def append_urls_to_json(urls: list[str], file_path: str) -> None:
+def append_urls_to_json(urls: list[str], file_path: str) -> None:
     try:
-        async with aiofiles.open(file_path, encoding="utf-8") as f:
-            content = await f.read()
+        with open(file_path, "r", encoding="utf-8") as f:
+            content = f.read()
             if content.strip():  # 文件不为空
                 existing_urls = json.loads(content)
                 if not isinstance(existing_urls, list):
@@ -25,11 +23,11 @@
     updated_urls = existing_urls + [url for url in urls if url not in existing_urls]
     print(f"{len(updated_urls)=}")
 
-    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
-        await f.write(json.dumps(updated_urls, ensure_ascii=False, indent=2))
+    with open(file_path, "w", encoding="utf-8") as f:
+        f.write(json.dumps(updated_urls, ensure_ascii=False, indent=2))
 
 
-async def main() -> None:
+def main() -> None:
     pocr = PaddleOCR(
         lang="ch",
         use_doc_orientation_classify=False,
@@ -40,7 +38,7 @@
     def ocr_scan(image_path: str | Path):
         return list(pocr.predict(str(image_path))[0]["rec_texts"])
 
-    async def ocr_and_extract_links():
+    def ocr_and_extract_links():
         current_dir = Path()
         files = [
             p
@@ -52,15 +50,16 @@
         for idx, img_path in enumerate(files, start=1):
             print(f"OCR {idx}/{len(files)} {img_path}")
             try:
-                yield await asyncio.to_thread(ocr_scan, str(img_path))
+                yield ocr_scan(str(img_path))  # 直接调用，无需 await
             except Exception:
                 logging.exception("Error")
 
-    async for new_links in ocr_and_extract_links():
+    # 使用普通 for 循环替代 async for
+    for new_links in ocr_and_extract_links():
         print(f"{len(new_links)=}")
-        await append_urls_to_json(new_links, "bug.json")
-        print(f"append success")
+        append_urls_to_json(new_links, "bug.json")
+        print("append success")
 
 
 if __name__ == "__main__":
-    asyncio.run(main())
+    main()  # 直接调用 main，无需 asyncio.run
```

```diff
diff -u -w main.py main_worker.py
--- main.py     2025-08-16 05:41:20.874672673 +0800
+++ main_worker.py      2025-08-16 05:44:22.541187139 +0800
@@ -2,7 +2,9 @@
 import json
 import logging
 import re
+import threading
 from pathlib import Path
+from queue import Queue, Empty
 
 import aiofiles
 from paddleocr import PaddleOCR
@@ -29,7 +31,15 @@
         await f.write(json.dumps(updated_urls, ensure_ascii=False, indent=2))
 
 
-async def main() -> None:
+class OCRWorker:
+    def __init__(self):
+        self._loop = asyncio.get_running_loop()
+        self._input_queue = Queue()
+        self.thread = threading.Thread(target=self._worker_loop, daemon=False)
+        self.thread.start()
+
+    def _worker_loop(self):
+        # ✅ 在工具线程中创建 PaddleOCR 实例
     pocr = PaddleOCR(
         lang="ch",
         use_doc_orientation_classify=False,
@@ -37,8 +47,45 @@
         use_textline_orientation=False,
     )
 
-    def ocr_scan(image_path: str | Path):
-        return list(pocr.predict(str(image_path))[0]["rec_texts"])
+        while True:
+            try:
+                # 获取任务
+                future, image_path = self._input_queue.get()
+                if future is None:  # 退出信号
+                    break
+
+                # 执行 OCR（在工具线程中）
+                try:
+                    result = list(pocr.predict(str(image_path))[0]["rec_texts"])
+                    # 使用 call_soon_threadsafe 把结果送回 asyncio 事件循环
+                    self._loop.call_soon_threadsafe(future.set_result, result)
+                except Exception as e:
+                    self._loop.call_soon_threadsafe(future.set_exception, e)
+
+                self._input_queue.task_done()
+
+            except Empty:
+                continue
+            except Exception as e:
+                logging.error(f"OCRWorker 线程异常: {e}", exc_info=True)
+
+    def ocr_scan(self, image_path: str | Path) -> asyncio.Future:
+        future = self._loop.create_future()
+        self._input_queue.put_nowait((future, image_path))
+        return future
+
+    def close(self):
+        self._input_queue.put_nowait((None, None))  # 发送退出信号
+
+
+async def main() -> None:
+    # 创建专用 OCR 工具线程
+    ocr_worker = OCRWorker()
+
+    try:
+        # 定义 ocr_scan 接口，与原来一致
+        async def ocr_scan(image_path: str | Path):
+            return await ocr_worker.ocr_scan(image_path)
 
     async def ocr_and_extract_links():
         current_dir = Path()
@@ -52,14 +99,17 @@
         for idx, img_path in enumerate(files, start=1):
             print(f"OCR {idx}/{len(files)} {img_path}")
             try:
-                yield await asyncio.to_thread(ocr_scan, str(img_path))
+                    yield await ocr_scan(img_path)  
             except Exception:
                 logging.exception("Error")
 
     async for new_links in ocr_and_extract_links():
         print(f"{len(new_links)=}")
         await append_urls_to_json(new_links, "bug.json")
-        print(f"append success")
+            print("append success")
+
+    finally:
+        ocr_worker.close()
 
 
 if __name__ == "__main__":
```
