import time
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306

class OLED:
    def __init__(self, fontSize):
        disp = Adafruit_SSD1306.SSD1306_128_32(rst = 0)
        disp.begin()
        disp.clear()
        disp.display()
        self.disp = disp
        self.width = disp.width
        self.height = disp.height
        self.fontSize = fontSize
        # 1 bit pixel
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def display_text(self, text, duration=None):
        font = ImageFont.truetype("./function/ARIALUNI.TTF", self.fontSize)
        if duration is not None:
            startTime = int(time.time())
            while (True):
                if (int(time.time()) - startTime > duration):
                    break
                self.draw.rectangle((0, 0, self.width, self.height), outline = 0, fill = 255)
                self.draw.text((0, 0), text, font = font, fill = 0)
                self.disp.image(self.image)
                self.disp.display()
                time.sleep(0.2)
        else:
            self.draw.rectangle((0, 0, self.width, self.height), outline = 0, fill = 255)
            for i, line in enumerate(text):
                self.draw.text((0, i*self.fontSize), line, font = font, fill = 0)

            self.disp.image(self.image)
            self.disp.display()
            time.sleep(0.2)

    def setFontSize(self, fontSize):
        self.fontSize = fontSize

    def clear(self):
        self.disp.clear()
        self.disp.display()
