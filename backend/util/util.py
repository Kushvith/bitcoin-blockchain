import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from math import log 

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def hash256(s):
    """two rounds of hashing"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()
def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()

def bytes_needed(n):
    if n ==0:
        return 1
    return int(log(n,256)) + 1 
        
    
def int_to_little_endian(n,length):
    """int to little endian takes the integer and returns the little endian byte sequence"""
    return n.to_bytes(length,'little')
def little_to_int(b):
    """takes a byte sequence and returns the integer"""
    return int.from_bytes(b,'little')
def decode_base64(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25,'big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f"Bad address {checksum} {hash256(combined[:-4])[:4]}")
    return combined[1:-4]

def encode_varient(i):
    """encode integer as a varient"""
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xff' + int_to_little_endian(i,2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i,4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i,8)
    else:
        raise ValueError('integer is too long {}'.format(i))         