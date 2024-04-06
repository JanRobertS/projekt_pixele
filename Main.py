import Silnik as S

def main():
    engine = S.Engine()
    engine.create_box(150, 150)

    engine.create_pixel(1, 0, 1, 1)
    engine.create_pixel(51, 50, -1, -1)
    engine.create_pixel(51, 50, 1)
    engine.create_pixel(50, 51, 0, 1)


    engine.time(1000, False, 1, 750, 750)

if __name__ == '__main__':
    main()