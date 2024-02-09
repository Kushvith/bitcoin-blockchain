from backend.util.util import hash256
class Blockheader:
    def __init__(self,version,prevBlockHash,merkleRoot,timestamp,bits):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp =timestamp
        self.bits = bits
        self.nounce = 0
        self.blockHash = ""
        
    def mine(self):
        while (self.blockHash[0:4]) != '0000':
            self.blockHash = hash256((str(self.version)+self.prevBlockHash+self.merkleRoot+str(self.timestamp)
                                     +self.bits+str(self.nounce)).encode()).hex()
            self.nounce +=1
            print(f"started {self.nounce}",end="\r")