from CurveP256 import CurveP256
from random import randrange

class ECDSA:
    def __init__(self, curve):
        if curve == 'P256':
            self.curve = CurveP256()
        else:
            self.curve = CurveP256()
    
    def sign(self, privKey, h):
            curve = self.curve
            n = self.curve.n
            h = int(h.hex(), 16)
            k = randrange(1, n)
            tmp = curve.mult(k, curve.G)
            r = tmp.x % n
            s = (h % n + r * privKey % n) * pow(k, -1, n) 
            return (r, s)
            
    def verify(self, pubKey, h, sign):
        curve = self.curve
        n = curve.n
        h = int(h.hex(), 16)
        r, s = sign
        w = pow(s, -1, n)
        u = (w * (h % n)) % n
        v = w * r % n
        Q = curve.add(curve.mult(u, curve.G), curve.mult(v, pubKey)) # Q = kG
        if sign[0] == Q.x % n:
            return True
        
        return False

# Test ECDSA
if __name__ == '__main__':
    import os
    from Crypto.Hash import SHA256
    from tqdm import trange
    
    p256 = CurveP256()
    ecdsa = ECDSA('CurveP256')
    
    for i in trange(1000):
        m = os.urandom(randrange(100))
        h = SHA256.new(m).digest()
    
        privKey = randrange(1, p256.p)
        pubKey = p256.mult(privKey, p256.G) 
    
        sign = ecdsa.sign(privKey, h)
        if not ecdsa.verify(pubKey, h, sign):
            print('Fail')
            break
    print('Success')
    
        