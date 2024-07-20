from random import randrange
from Point import Point


class CurveP256:    # y^2 = x^3 + ax + b (mod p)

    def __init__(self):
        self.p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        self.a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
        self.b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
        self.G = Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
        self.n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
        self.h = 0x01

    def doubling(self, P): # P + P = 2 * P
        s = (3 * pow(P.x, 2, self.p) + self.a) % self.p
        s = s * pow(2 * P.y, -1, self.p) % self.p
        x = (pow(s, 2, self.p) - 2 * P.x) % self.p
        y = -(P.y - (s * (P.x - x) % self.p)) % self.p
        return Point(x, y)

    def add(self, P1, P2): # P1 + P2
        if P1.isInfinity():
            return P2
        if P2.isInfinity():
            return P1
        if P1.equal(P2):
            return self.doubling(P1)
        if (P1.x - P2.x) % self.p == 0:
            return Point.infinity()

        s = (P2.y - P1.y % self.p) * pow(P2.x - P1.x, -1, self.p)
        s = s % self.p

        x = (pow(s, 2, self.p) - P1.x - P2.x) % self.p
        y = -(P1.y - (s * (P1.x - x) % self.p)) % self.p

        return Point(x, y)

    def mult(self, r, P): # int * Point
    
        tmp1, tmp2 = Point.infinity(), P
        while r != 0:
            if r & 0x01:
                tmp1 = self.add(tmp1, tmp2)
            tmp2 = self.doubling(tmp2)
            r = r >> 1
        return tmp1

# Test
if __name__ == '__main__':
    from  tqdm import trange
    
    def test():
        a, b = randrange(2**256), randrange(2**256)
        p256 = CurveP256()
        aG = p256.mult(a, p256.G)
        bG = p256.mult(b, p256.G)
        baG = p256.mult(b, aG)
        abG = p256.mult(a, bG)

        if abG.equal(baG):
            return True
        else:
            return False

    for i in trange(1000):
        if not test():
            print('Fail')
            break
    print('Success')