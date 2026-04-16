from functools import wraps


def ff():
    print("hh")


def outer(func):
    @wraps(func)
    def inner():
        print("start")
        func()
        print("end")
    return inner


@outer
def test():
    print("hi")


print(test.__doc__)
