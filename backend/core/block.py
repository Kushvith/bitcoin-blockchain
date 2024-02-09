class Block:
    """
    block is the storage container to store transactions
    """
    def __init__(self,Height,Blocksize,BlockHeader,TxCount,Txs):
        self.Height = Height
        self.Blocksize = Blocksize
        self.BlockHeader = BlockHeader
        self.TxCount = TxCount
        self.Txs = Txs
        
    