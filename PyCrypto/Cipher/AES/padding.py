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