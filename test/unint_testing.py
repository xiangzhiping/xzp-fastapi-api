import base64
import importlib
import os
import random
import string

from captcha.image import ImageCaptcha


def get_file_names(directory):
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith('.pyc'):  # 排除以 .pyc 结尾的文件
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]  # 去除文件后缀
                file_names.append("src.reqBody." + file_name)

    return file_names


directory = "../src/reqBody"  # 替换为你的目录路径
files = get_file_names(directory)

# for file in files:
module = importlib.import_module(files[2])
print(module)

# 获取模块中的类名列表
class_names = [key for key in dir(module) if not key.startswith('_') and isinstance(getattr(module, key), type)][2]
print(class_names)
class_obj = getattr(module, class_names)
print(class_obj)
print(type(dict(class_obj.__dict__)), dict(class_obj.__dict__).get("model_fields"))


x = [(b'host', b'localhost:8888'), (b'connection', b'keep-alive'), (b'content-length', b'32'), (b'sec-ch-ua', b'"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"'), (b'accept', b'application/json, text/plain, */*'), (b'content-type', b'application/json'), (b'sec-ch-ua-mobile', b'?0'), (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.36'), (b'token', b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6dGJfcHJvamVjdCIsInN1YiI6NzA5MzI0MTE2MTc3NDY2NTcyOCwiYXVkIjoiYXBpLnp0Yl9wcm9qZWN0LmNvbSIsImV4cCI6MTY5MTY3MDI2NCwibmJmIjoxNjkxNTgzODY0LCJpYXQiOjE2OTE1ODM4NjQsImp0aSI6IjcwOTUwMTgyNTI2MTg4Mjk4MjQifQ.87fLYjycTxr7Nk01piY9vPkSzi_WhibXpWAKUhMasGY'), (b'sec-ch-ua-platform', b'"Windows"'), (b'origin', b'http://localhost:5173'), (b'sec-fetch-site', b'same-site'), (b'sec-fetch-mode', b'cors'), (b'sec-fetch-dest', b'empty'), (b'referer', b'http://localhost:5173/'), (b'accept-encoding', b'gzip, deflate, br'), (b'accept-language', b'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6')]
print(dict(x).get(b'token').decode("utf-8"))

y = b'DSADAS'
if y:
    print("sdad")
else:
    print("daSD")

captcha = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
image_data = ImageCaptcha().generate(captcha).getvalue()
captchaImage = base64.b64encode(image_data).decode('utf-8')
print(captcha)

# db.createUser({
#   user: "xzp",
#   pwd: "633124",
#   roles: ["root"]
# })
