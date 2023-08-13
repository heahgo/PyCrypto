def mult(x : int, y : int) -> int: # Multiplication GF(2^128)
    z = 0
    r = 0b11100001 << 120 # 1 + x + x^2 + x^7
    for i in range(128): 
        if x & (1<<127):
            z ^= y
        x <<= 1
        if y & 1:
            y = (y>>1)^r
        else:
            y >>= 1
    return z

def GHASH(x : bytes, H : bytes) -> int:
    y = 0
    H = int.from_bytes(H, 'big')
    for i in range(0, len(x), 16):
        y = mult(y ^ int.from_bytes(x[i:i+16], 'big'), H)
    return y

def gen_tag(x : bytes, H : bytes, ej : bytes, ad=b'') -> int:
    length = (len(ad)*8).to_bytes(8, byteorder='big') + (len(x)*8).to_bytes(8, byteorder='big')
    x = ad + bytes((16-len(ad)%16)%16) + x + bytes((16-len(x)%16)%16) + length
    result = GHASH(x, H)
    ej = int.from_bytes(ej, 'big')
    return (result^ej).to_bytes(16, byteorder='big')

if __name__ == '__main__':
    def test(repeat : int) -> None: 
        from Crypto.Cipher import AES
        from random import randbytes
        for i in range(repeat):
            key = randbytes(16)
            nonce = randbytes(11)
            counter = b'\x00'*3 + b'\x01'
            p1 = randbytes(123)
            ad = randbytes(8)

            crypto = AES.new(key, AES.MODE_GCM, nonce=nonce)
            crypto.update(ad)
            c1, tag1 = crypto.encrypt_and_digest(p1)

            crypto = AES.new(key, AES.MODE_ECB)
            H = crypto.encrypt(bytes(16))
            
            if len(nonce) == 12:
                j = nonce + counter
            else:
                s = bytes((16-len(nonce)%16)%16)
                j = nonce + s + bytes(8) + (len(nonce)*8).to_bytes(8, byteorder='big')
                j = GHASH(j, H).to_bytes(16, byteorder='big')
                
            ej = crypto.encrypt(j)
            tag2 = gen_tag(c1, H, ej, ad)    

            if tag1 != tag2:
                print('Test Failed')
                return
        print('Test Sucsessed')

    test(1000)
    

  