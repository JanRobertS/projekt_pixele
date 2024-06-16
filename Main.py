import Silnik as S

def main():
    engine = S.Engine()
    engine.create_box(100, 100)

    engine.create_random_pixel(100)


    engine.time(200, False, 10, 750, 750)

if __name__ == '__main__':
    main()