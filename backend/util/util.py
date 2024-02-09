import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from math import log

from backend.core.EllepticCurve.EllepticCurve import BASE58_ALPHABET
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

def decode_base64(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25,'big')
    checksum = combined[-4:]
        