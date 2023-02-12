from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import random


class Preview:
    def __init__(self, image_text: str, background: str):
        self.text = image_text
        self.image = Image.open(background)
        self.size_x, self.size_y = self.image.size
        self.font = 'fonts/CricketInlineShadow.ttf'
        self.bg_font_color = None
        self.font_color = (255, 255, 255)

    def blur_background(self, strength=100):
        self.image = self.image.filter(ImageFilter.GaussianBlur(strength))  # наложение блюра

    def rotate_image(self, rot: int):
        self.image = self.image.rotate(rot)
        x = int(self.size_x / (16 / 9 * math.sin(math.radians(rot)) + math.cos(math.radians(rot))))
        y = int(x * 9 / 16)
        self.image = self.image.crop(((self.size_x - x) // 2, (self.size_y - y) // 2, x + (self.size_x - x) // 2,
                                      (self.size_y - y) // 2 + y))
        self.size_x = x
        self.size_y = y

    def overlay_noise(self, noise_id=1):
        noise_image = Image.open(f'noises/noise{noise_id}.png')  # выбор картинки шума
        noise_image = noise_image.resize((self.size_x, self.size_y),
                                         Image.ANTIALIAS)
        # пофиксить адаптацию!!!
        self.image.paste(noise_image, (0, 0), mask=noise_image)  # вставка шума как маски

    def set_font(self, font_name: str):
        self.font = 'fonts/' + font_name

    def set_bg_font_color(self, red, green, blue):
        self.bg_font_color = (red, green, blue)

    def set_font_color(self, red, green, blue):
        self.font_color = (red, green, blue)

    def generate_text(self, text=''):
        if text:
            self.text = text
        test_font = ImageFont.truetype(self.font, 100)
        max_words = list()
        for word in self.text.split('\n'):
            max_words.append(test_font.getlength(word.strip()))
        del test_font
        max_word = self.text.split('\n')[max_words.index(max(max_words))]
        del max_words
        # определение размера шрифта
        bg_font = ImageFont.truetype(self.font, size=6)
        main_font = ImageFont.truetype(self.font, size=1)
        for font_size in range(self.size_x // 2, 0, -2):
            bg_font = ImageFont.truetype(self.font, size=font_size)
            main_font = ImageFont.truetype(self.font, size=font_size)
            if bg_font.getlength(max_word) < self.size_x * 0.9 and bg_font.getsize_multiline(self.text)[1] < self.size_y:
                break
        # добавление пробелов для центрирования текста
        max_length = main_font.getlength(max_word)
        new_text = ''
        for iter_word in self.text.split('\n'):
            while main_font.getlength(iter_word) <= max_length:
                iter_word = ' ' + iter_word + ' '
            new_text += iter_word + '\n'
        self.text = new_text[:-1]
        # определение среднего цвета
        if self.bg_font_color is None:
            red, green, blue, total = 0, 0, 0, 0
            pixels = self. image.load()
            for x_cord in range(self.size_x):
                for y_cord in range(self.size_y):
                    red += pixels[x_cord, y_cord][0]
                    green += pixels[x_cord, y_cord][1]
                    blue += pixels[x_cord, y_cord][2]
                    total += 1
            self.bg_font_color = (red // total, green // total, blue // total)
        # отрисовка текста
        text_artist = ImageDraw.Draw(self.image)
        font_x, font_y = bg_font.getsize_multiline(self.text)
        text_artist.text(((self.size_x - font_x) // 2, (self.size_y - font_y) // 2), self.text, font=bg_font,
                         fill=self.bg_font_color)
        font_x, font_y = main_font.getsize_multiline(self.text)
        text_artist.text((((self.size_x - font_x) // 2) * 0.9, (self.size_y - font_y) // 2), self.text, font=main_font,
                         fill=self.font_color)

    def set_filter(self, filter_type: str):
        pixels = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                new_pixel = [0, 0, 0]
                if filter_type == 'invert':
                    filter_type = 'invertredinvertgreeninvertblue'
                if filter_type == 'gray':
                    center = sum(pixels[x, y]) // 3
                    pixels[x, y] = (center, center, center)
                    continue
                if 'invertred' in filter_type:
                    new_pixel[0] = 255 - pixels[x, y][0]
                elif 'red' in filter_type:
                    new_pixel[0] = pixels[x, y][0]
                if 'invertgreen' in filter_type:
                    new_pixel[1] = 255 - pixels[x, y][1]
                elif 'green' in filter_type:
                    new_pixel[1] = pixels[x, y][1]
                if 'invertblue' in filter_type:
                    new_pixel[2] = 255 - pixels[x, y][2]
                elif 'blue' in filter_type:
                    new_pixel[2] = pixels[x, y][2]
                pixels[x, y] = tuple(new_pixel)

    def save_preview(self, name='result.png'):
        self.image.save(name, format='png')


def get_random_font():
    fonts = os.listdir('fonts')
    font = random.choice(fonts)
    return font


if __name__ == '__main__':
    preview = Preview('wow\nNSTEP GAY\nebaat', 'image2.jpg')
    preview.rotate_image(30)
    fonts = os.listdir('fonts')
    font = random.choice(fonts)
    preview.set_font(font)
    preview.blur_background()
    preview.generate_text()
    preview.save_preview()

# сделать строки разного размера
