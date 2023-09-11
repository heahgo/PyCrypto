def pad(byte, block_size):
    pad_byte =  bytes({block_size - (len(byte) % block_size)})
    return byte + pad_byte[0] * pad_byte

def unpad(byte, block_size):
    pad_bytes = byte[-1]
    if pad_bytes > block_size or pad_bytes == 0:
        raise ValueError
    for i in range(pad_bytes):
        if byte[-1] != pad_bytes:
            raise ValueError
    return byte[:-(pad_bytes)]

def byte2list(byte):
        return [byte[4*i + j] for i in range(4) for j in range(4)]

def list2byte(arr):
    result = b''
    for i in range(len(arr)):
        result += bytes({arr[i]})
    return result

def list2state(arr):
    return [arr[i+j] for i in range(4) for j in range(0, 16, 4)]
    
def state2list(state):
    return [state[i+j] for i in range(4) for j in range(0, 16, 4)]

def byte2state(byte):
    return list2state(byte2list(byte))

def state2byte(state):
    return list2byte(state2list(state))

def mult_8(x, y): # mult_8 mutiplication GF(2^8)
    result = 0
    while y:
        if y & 0x01:
            result ^= x
        y >>= 1
        x <<= 1
        if x & 0x100:
            x ^= 0x1b
    return result & 0xff

def mult_128(x : int, y : int) -> int: # mult_128 multiplication GF(2^128)
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