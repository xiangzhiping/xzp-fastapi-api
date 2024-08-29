from random import randint, choices
from PIL import Image, ImageDraw, ImageFont
from string import ascii_letters, digits


async def ImageCaptchaGenerator(width: int = 160, height: int = 60, fn: int = 4) -> (str, Image.Image):
    """图像验证码生成器
        :param width: int - 验证码图片的宽度，默认为 160 像素；
        :param height: int - 验证码图片的高度，默认为 60 像素；
        :param fn: int - 验证码字符的数量，默认为 4 个字符；
    返回:
        Tuple[str, Image.Image]: 一个元组，包含生成的验证码文本和对应的 PIL.Image 对象。
    """
    bc = (randint(200, 255), randint(200, 255), randint(200, 255))
    image = Image.new('RGB', (width, height), color=bc)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('ariali.ttf', int(height * 0.8))
    text = ''.join(choices(ascii_letters + digits, k=fn))
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (width - bbox[2] - bbox[0]) / 2
    y = (height - bbox[3] - bbox[1]) / 2
    for i, char in enumerate(text):
        sc = (randint(0, 255), randint(0, 255), randint(0, 255))
        for _ in range(3):
            gc = tuple(int(c * 1.7) for c in sc)
            for dx, dy in [(1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)]:
                draw.text((x + i * bbox[2] / len(text) + dx * 1, y + dy * 1), char, font=font, fill=gc)
        draw.text((x + i * bbox[2] / len(text), y), char, font=font, fill=sc)

    return text.lower(), image

# async def main():
#     text, image = await ImageCaptchaGenerator()
#     image.show()
#     print(text)
#
#
# if __name__ == '__main__':
#     from asyncio import run
#
#     run(main())
