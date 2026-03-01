

class Test:
    def __init__(self, name):
        self.name = name

    def tt(self):
        print("self.name")


class Inst(Test):
    def __init__(self, name):
        self.name = name


def main():
    # obj2 = Test("22")
    obj = Inst("teddst")
    obj.tt()


main()
