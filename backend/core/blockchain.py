import sys
import time
sys.path.append("/programs/python/blockchain")

from backend.core.block import Block
from backend.core.blockheader import Blockheader
from backend.util.util import hash256
from backend.core.database.database import BlockChainDb
from backend.core.Tx import CoinbaseTx
from multiprocessing import Process,Manager
from frontend.run import main
ZERO_HASH = '0' * 64
VERSION = 1
class Blockchain:
    def __init__(self,utoxs):
        self.utoxs = utoxs
    
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
    def store_utoxs(self,transaction):
        """keep the track of unspent transaction for faster retreval"""
        self.utoxs[transaction.Txid] = transaction
        
    def addBlock(self,BlockHeight,prevBlockHash):
        timestamp = int(time.time())
        coinbaseInstance = CoinbaseTx(BlockHeight=BlockHeight)
        coinbaseTx = coinbaseInstance.CoinbaseTransaction()
        merkleRoot = coinbaseTx.Txid
        bits = "ffff001f"
        blockheader = Blockheader(version=VERSION,prevBlockHash=prevBlockHash,merkleRoot=merkleRoot,
                                  timestamp=timestamp,bits=bits)
        blockheader.mine()
        self.store_utoxs(coinbaseTx)
        self.write_on_disk([Block(BlockHeight,1,blockheader.__dict__,1,coinbaseTx.toDict()).__dict__] ) 
       
        
    def main(self):
        lastBlock = self.fetch_last_block()
        if lastBlock is None:
            self.gensisBlock()
        while True:
            lastBlock = self.fetch_last_block()
            print(lastBlock)
            BlockHeight = lastBlock["Height"] +1
            prevBlockHash = lastBlock["BlockHeader"]["blockHash"]
            self.addBlock(BlockHeight,prevBlockHash)
if __name__ == "__main__":
    with Manager() as manager:
        utoxs = manager.dict()
        webapp = Process(target= main,args= (utoxs,))
        webapp.start()
        blockchain = Blockchain(utoxs)
        blockchain.main()