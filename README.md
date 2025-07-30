# paddle ocr bug reproduce

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
```

add `shot_.*\.png`

```bash
hatch run bug
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

