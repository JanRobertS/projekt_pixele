import Obiekty as Ob
import numpy as np
import cv2


class Engine():
    def __init__(self):
        self.box = None
    
    def run(self):
        print('Engine działa')

    def create_box(self, witdh = 100, height = 100):
        self.box = Ob.box(witdh, height)
    
    def create_pixel(self, x, y, dx = 0, dy = 0):
        return self.box.create_pixel(x, y, dx, dy)
    
    def delete_pixel(self, pixel):
        self.box.delete_pixel(pixel)
    
    def pixele_in_box(self):
        return self.box.pixele_in_box()
    
    def time(self, t, wizualizacja = True, czas = 50, wymiarx = 750, wymiary = 750):
        for __ in range(t):  
            positions, speeds = self.box.create_list_of_positions_all_pixels(), self.box.create_list_of_speeds_all_pixels()
            for pixel in self.box.pixele:
                id = pixel.id

                collision, pixel2, id2 = self.box.coliision2_pixel(pixel, positions, speeds)
                if collision:
                    pixel.speed(speeds[id2][0], speeds[id2][1])
                    #print('Kolizja z pixelem 2')
                
                
                collisionx = self.box.collisionx(pixel)
                collisiony = self.box.collisiony(pixel)
                if collisionx and collisiony:
                    pixel.speed(-speeds[id][0], -speeds[id][1])
                    #print('Kolizja x i y')
                elif collisionx:
                    pixel.speed(-speeds[id][0], speeds[id][1])
                    #print('Kolizja')

                elif collisiony:
                    pixel.speed(speeds[id][0], -speeds[id][1])
                    #print('Kolizja')
            
                pixel.move()

            if not self.__display_image(czas, wymiarx, wymiary):
                print("wyjście z programu")
                return 

    def tablica_pixelow(self):
        tablica = [[(0, 0, 0) for _ in range(self.box.witdh)] for _ in range(self.box.height)]    
        for pixel in self.box.pixele_in_box():
            tablica[pixel.y][pixel.x] = pixel.color
        return tablica
    
    
    def __dodaj_legende(self, obraz):

        font = cv2.FONT_HERSHEY_SIMPLEX 
        fontScale = 0.5
        thickness = 1

        for pixel in self.box.pixele:
            org = (425, 25 + pixel.id*20) 
            color = (int(pixel.color[0]), int(pixel.color[1]), int(pixel.color[2]))

            s = "pixel: "
            s += str(pixel.id)

            obraz = cv2.putText(obraz, s, org, font,  
                   fontScale,color , thickness, cv2.LINE_AA) 
            
        return obraz

                
        
    def __display_image(self, czas = 50, wymiarx = 750, wymiary = 750):
        if not hasattr(self, "window_created"):
            self.window_created = False

        tablica = self.tablica_pixelow()
        image = np.array(tablica, dtype=np.uint8)
        resized_image = cv2.resize(image, (wymiarx, wymiary), interpolation=cv2.INTER_NEAREST)
        
        resized_image = self.__dodaj_legende(resized_image)

        if not self.window_created:
            cv2.namedWindow("Image")
            self.window_created = True

        cv2.imshow("Image", resized_image)
        key = cv2.waitKey(czas)
        if key == ord('q'):
            cv2.destroyAllWindows()
            return False
        else:
            return True


    def __del__(self):
        print('Engine usunięty')
