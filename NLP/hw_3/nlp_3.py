import random


def main():
    test_x = open('test_x.txt', 'r')
    lines = test_x.readlines()
    print len(lines)
    test_y = open('random.txt', 'w')
    for i in range(len(lines)):
        tmp = random.randint(1, 5)
        print >> test_y, tmp
    test_y.close()


if __name__ == '__main__':
    main()
