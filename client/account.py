import sys
sys.path.append('/programs/python/blockchain')
from backend.core.EllepticCurve.EllepticCurve import Sha256Point
import secrets
from backend.util.util import hash160
from backend.util.util import hash256
class Account:
    def createKeys(self):
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        G = Sha256Point(Gx,Gy)
        privateKey = secrets.randbits(256)
        unCompressedpublickey = privateKey * G
        Xpoint = unCompressedpublickey.x
        Ypoint = unCompressedpublickey.y
        if Ypoint.num % 2 !=0:
            compressedKey = b'\x02'+Xpoint.num.to_bytes(32,'big')
        else:
            compressedKey = b'\x03'+Xpoint.num.to_bytes(32,'big')
        hsh160 = hash160(compressedKey)
        """Prefix from mainnet"""
        main_prefix = b'\00'
        newaddr = main_prefix + hsh160
        """checksum"""
        checksum = hash256(newaddr)[:4]
        newaddr = newaddr +checksum
        BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        count = 0
        for c in newaddr:
            if c==0:
                count+=1
            else:
                break
     
        num = int.from_bytes(newaddr,'big')
   
        prefix = '1'*count
        result = ""
        while num>0:
            num,mod = divmod(num,58)
            
            result = BASE58_ALPHABET[mod] +result
        publicAddress = prefix+result
        print(f"public address {publicAddress}")
        
        
        
        
        
        
if __name__ == "__main__":
    acc= Account()
    acc.createKeys()