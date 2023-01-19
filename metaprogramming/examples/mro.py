
class Base:
    x = 1


class A(Base):
    x = 2


class B(Base):
    x = 3


class C(Base):
    x = 4


class D(A, B):
    x = 5


class E(C, D):
    x = 6



def main():
    print(E.__mro__)
    print(E.x)
    return 0


if __name__ == '__main__':
    exit(main())
