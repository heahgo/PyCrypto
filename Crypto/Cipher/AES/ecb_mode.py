
from AES_util import *
class AES_ECB(AES):
    
    def encrypt(self, state):
        try:
            unpad(state, self.block_size)
        except ValueError as e:
            print(e)
            exit()

        blocks = [state[i:i+16] for i in range(0, len(state), self.block_size)]
        result = b''
        for block in blocks:
            state = byte2state(block)

            state = self.addRoundKey(state, self.ex_key[0:16])
            for i in range(16, (self.r)*16, 16):
                state = self.round(state, self.ex_key[i:i+16])
            state = self.addRoundKey(self.shiftRows(self.subBytes(state)), self.ex_key[-16:])
            result += state2byte(state)

        return result
            
    def decrypt(self, state):
        if len(state) % self.block_size != 0:
            return 0
        
        blocks = [state[i:i+16] for i in range(0, len(state), self.block_size)]
        result = b''
        for block in blocks:
            state = byte2state(block)

            state = self.addRoundKey(state, self.ex_key[-16:])
            for i in reversed(range(16, (self.r)*16, 16)):
                state = self.inv_round(state, self.ex_key[i:i+16])
            state = self.addRoundKey(self.inv_subBytes(self.inv_shiftRows(state)), self.ex_key[0:16])
            result += state2byte(state)

        return result
    
if __name__ ==  '__main__':
    from Crypto.Random import get_random_bytes
    from random import randint
    from Crypto.Cipher import AES 
    from Crypto.Util.Padding import pad, unpad
    def test(key_len):
        if key_len != 16 and key_len != 24 and key_len != 32:
            print('Key length only 128, 192, 256')
            return
        for i in range(100):
            key = get_random_bytes(key_len)
            crypto1 = AES_ECB(key)
            crypto2 = AES.new(key, AES.MODE_ECB)
            p = get_random_bytes(randint(1, 196))
            c1 = crypto1.encrypt(pad(p, 16))
            c2 = crypto2.encrypt(pad(p, 16))
            try:
                p1 = unpad(crypto1.decrypt(c1), 16)
                p2 = unpad(crypto2.decrypt(c2), 16)
            except ValueError:
                print(f'AES-{key_len*8} ECB mode Test Falied')
                return        
            if  c1  != c2 or p1 != p2:
                print(f'AES-{key_len*8} ECB mode Test Falied')
                return
        print(f'AES-{key_len*8} ECB mode Test Sucsessed')
    
    test(16)
    test(24)
    test(32)