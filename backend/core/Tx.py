from backend.core.Script import Script
from backend.util.util import int_to_little_endian
from backend.util.util import bytes_needed
ZERO_HASH = b'\0'*32
REWARD = 50
class CoinbaseTx:
    def __init__(self,BlockHeight) -> None:
        self.BlockHeightInLittleEndian = int_to_little_endian(BlockHeight,bytes_needed(BlockHeight))
    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xffffffff
        tx_ins = []
        tx_ins.append(TxIn(prev_tx,prev_index))
        tx_out = []
        target_amount = REWARD * 100000000000
        target_
        
        
class Tx:
    def __init__(self,version,tx_ins,tx_outs,locktime) -> None:
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
    
class TxIn:
    def __init__(self,prev_tx,prev_index,script_sig = None,sequence = 0xffffffff) -> None:
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

class TxOut:
    def __init__(self,amount,script_pubkey) -> None:
        self.amount = amount
        self.script_pubkey = script_pubkey