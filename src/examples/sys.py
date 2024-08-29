from src.examples.user import *

ImageCaptchaIdGetExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "图像验证码id获取成功", '图像验证码id'),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "图像验证码id获取失败")
}
ImageCaptchaImageGetExample = {
    HTTP_200_OK: Http200PngExample(),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "图形验证码获取失败")
}

IdentityCaptchaSendExample = {
    HTTP_200_OK: Http200JsonExample(HTTP_200_OK, "xxx验证码发送成功", 'null'),
    HTTP_500_INTERNAL_SERVER_ERROR: Http500ServerErrorExample(HTTP_500_INTERNAL_SERVER_ERROR, "xxx验证码发送失败")
}
