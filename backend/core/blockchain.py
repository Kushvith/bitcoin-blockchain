import sys
import time
sys.path.append("/programs/python/blockchain")

from backend.core.block import Block
from backend.core.blockheader import Blockheader
from backend.util.util import hash256
from backend.core.database.database import BlockChainDb

ZERO_HASH = '0' * 64
VERSION = 1
class Blockchain:
    def __init__(self):
        self.gensisBlock()
    
    def write_on_disk(self,block):
        blockchaindb = BlockChainDb()
        blockchaindb.write(block)
    
    def fetch_last_block(self):
        blockchaindb = BlockChainDb()
        return blockchaindb.lastBlock()
    
    def gensisBlock(self):
        BlockHeight = 0
        prevBlockHash = ZERO_HASH
        self.addBlock(BlockHeight,prevBlockHash)
        
    def addBlock(self,BlockHeight,prevBlockHash):
        timestamp = int(time.time())
        transaction = f"kushvith sent {BlockHeight} bitcoins to joe"
        merkleRoot = hash256(transaction.encode()).hex()
        bits = "ffff001f"
        blockheader = Blockheader(version=VERSION,prevBlockHash=prevBlockHash,merkleRoot=merkleRoot,
                                  timestamp=timestamp,bits=bits)
        blockheader.mine()
        self.write_on_disk([Block(BlockHeight,1,blockheader.__dict__,1,transaction).__dict__] ) 
       
        
    def main(self):
        while True:
            lastBlock = self.fetch_last_block()
            print(lastBlock)
            BlockHeight = lastBlock["Height"] +1
            prevBlockHash = lastBlock["BlockHeader"]["blockHash"]
            self.addBlock(BlockHeight,prevBlockHash)
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.main()