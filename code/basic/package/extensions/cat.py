age = 6


def eat():
    print("吃鱼骨头！")


def run():
    c = Cat()
    c.eat()


class Cat:

    @staticmethod
    def play():
        print("作迷藏")

    @staticmethod
    def eat():
        print('吃猫粮')
