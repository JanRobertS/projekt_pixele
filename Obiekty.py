#pixel

from time import sleep as wait
import cv2
import numpy as np
import copy


class Pixel():
    next_id = 0
    colors = []

    def __init__(self, x, y, speedx = 0, speedy = 0, color = None):
        self.x = x
        self.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.id = Pixel.next_id

        if color is None:
            self.color = self.check_color(self.random_color())
        else:
            self.color = color

        if not color in Pixel.colors:
            Pixel.colors.append(self.color)


        Pixel.next_id += 1
    
    def random_color(self):
        return list(np.random.choice(range(256), size=3))
    
    def check_color(self, color):
        while color == (0,0,0) or color in Pixel.colors:
            color = self.random_color()
        return color
    
    def __str__(self):
        return f'Pixel na pozycji ({self.x}, {self.y})'
    
    def move(self):
        self.x += self.speedx
        self.y += self.speedy
    
    def speed(self, dsx, dsy):
        self.speedx = dsx
        self.speedy = dsy

    def nowa_pozycja(self, x = None, y = None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y


class Obiekt(Pixel):
    def __init__(self, x: int, y: int, ksztalt: str, witdh: int, height: int, speedx: int = 0, speedy: int = 0, color = None):
        super().__init__(x, y)
        self.witdh = witdh
        self.height = height
        self.ksztalt = ksztalt

        self.tab_pixele = []

        if color is None:
            color = self.random_color()

        self.color = self.check_color(color)

        self.build_obiekt

    def build_obiekt(self):
        if self.ksztalt == "kwadrat":
            obiekt = [[None for _ in range(self.witdh)] for __ in range(self.height)]
            for x in range(self.witdh):
                for y in range(self.height):
                    obiekt[x][y] = Pixel(self.x + x, self.y + y, self.speedx, self.speedy, self.color)

        self.tab_pixele = obiekt

    def speed(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy

    def move(self):
        self.x += self.speedx
        self.y += self.speedy

        for pixel in self.tab_pixele:
            pixel.x += self.speedx
            pixel.y += self.speedy








class box():
    def __init__(self, witdh = 100, height = 100):
        self.witdh = witdh
        self.height = height
        self.pixele = []
        self.obiekty = []

    def create_pixel(self, x, y, dx = 0, dy = 0):
        pixel = Pixel(x, y, dx, dy)
        self.add_pixel(pixel)
        return pixel
    
    def create_list_of_positions_all_pixels(self):
        return [[pixel.x, pixel.y] for pixel in self.pixele]
    
    def create_list_of_speeds_all_pixels(self):
        return [[pixel.speedx, pixel.speedy] for pixel in self.pixele]
    
    def add_pixel(self, pixel):
        self.pixele.append(pixel)
    
    def delete_pixel(self, pixel):
        self.pixele.remove(pixel)
        del pixel

    def pixele_in_box(self):
        return self.pixele
    
    def collisionx(self, pixel):
        if pixel.x + pixel.speedx < 0 or pixel.x + pixel.speedx > self.witdh - 1:
            return True
        return False
    
    def collisionx2(self, pixel):
        warunek1 = pixel.x + pixel.speedx - self.witdh + 1
        warunek2 = pixel.x + pixel.speedx
        if warunek1 > 0:
            new_x = self.witdh - warunek1
            return True, new_x
        if warunek2 < 0:
            new_x = -warunek2
            return True, new_x
        return False, None

    def collisiony(self, pixel):
        if pixel.y + pixel.speedy < 0 or pixel.y + pixel.speedy > self.height - 1:
            return True
        return False
    
    def collisiony2(self, pixel):
        warunek1 = pixel.y + pixel.speedy - self.height + 1
        warunek2 = pixel.y + pixel.speedy
        if warunek1 > 0:
            new_y = self.height - warunek1
            return True, new_y
        if warunek2 < 0:
            new_y = -warunek2
            return True, new_y
        return False, None

    
    def coliision_pixel(self, pixel):
        for pixel2 in self.pixele:
            if pixel != pixel2 and pixel.x + pixel.speedx == pixel2.x + pixel2.speedx and pixel.y + pixel.speedy == pixel2.y + pixel2.speedy :
                return True, pixel2
        return False, None
    
    def coliision2_pixel(self, pixel, position, speeds):
        id = pixel.id
        for pixel2 in self.pixele:
            id2 = pixel2.id
            if pixel != pixel2:
                if (position[id][0] + speeds[id][0] == position[id2][0] + speeds[id2][0] and position[id][1] + speeds[id][1] == position[id2][1] + speeds[id2][1] \
                or position[id][0] == position[id2][0] + speeds[id2][0] and position[id][1] == position[id2][1] + speeds[id2][1]): 
                #sprawdzanie czy pixele nie będą koło siebie lub na tym samym miejcu, w najstępnym kroku
                    return True, pixel2, id2
        return False, None, None
    
    def create_obiekt(self, x, y, ksztalt, witdh, height, speedx = 0, speedy = 0, color = None):
        obiekt = Obiekt(x, y, ksztalt, witdh, height, speedx, speedy, color)
        self.__add_obiekt(obiekt)
        return obiekt

    def __add_obiekt(self, obiekt):
        self.obiekty.append(obiekt)
    
    def delete_obiekt(self, obiekt):
        self.obiekty.remove(obiekt)
        del obiekt

    def colisionx_obiekt(self, obiekt):
        tab_pixele = obiekt.tab_pixele
        x, y = np.shape(tab_pixele)

    def __str__(self):
        return f'Box o wymiarach {self.witdh}x{self.height}'
    
    def __del__(self):
        print('Box usunięty')
