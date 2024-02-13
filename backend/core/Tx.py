from backend.core.Script import Script
from backend.util.util import int_to_little_endian
from backend.util.util import bytes_needed,decode_base64,little_to_int,encode_varient,hash256
ZERO_HASH = b'\0'*32
REWARD = 50

PRIVATE_KEY = "78752236796040771153958786401960443589424187305886373190304611680843114035674"
MINER_ADDRESS = "1AuYyWqw2ivooAK2k5TSp8jjgfcLAgJae2"
SIGHASH = 1
class CoinbaseTx:
    def __init__(self,BlockHeight) -> None:
        self.BlockHeightInLittleEndian = int_to_little_endian(BlockHeight,bytes_needed(BlockHeight))
    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xffffffff
        tx_ins = []
        tx_ins.append(TxIn(prev_tx,prev_index))
        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleEndian)
        tx_out = []
        target_amount = REWARD * 10000
        target_h160 = decode_base64(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_h160)
        tx_out.append(TxOut(amount=target_amount,script_pubkey=target_script))
        coinbasetx = Tx(1,tx_ins=tx_ins,tx_outs=tx_out,locktime=0)
        coinbasetx.Txid = coinbasetx.id()
        return coinbasetx
        
class Tx:
    def __init__(self,version,tx_ins,tx_outs,locktime) -> None:
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
    def id(self):
        """human readable tx in hex"""
        return self.hash().hex()
    def hash(self):
        return hash256(self.serialize())[::-1]
    def serialize(self):
        result = int_to_little_endian(self.version,4)
        result += encode_varient(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varient(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime,4)
        return result
    
    def is_coinbase(self):
        """
        #check that there is exactly one input
        #grab the first input and check if the prev_tx b'\x00'*32
        #check that the first input prev_index = 0Xffffffff
        """
        if len(self.tx_ins) !=1:
            return False
        first_input  = self.tx_ins[0]
        if first_input.prev_tx != b'\x00'*32:
            return False
        if first_input.prev_index != 0xffffffff:
            return False
        return True
    def toDict(self):
        """
        convert coinbase transaction
         #convert prev_tx in hex from bytes
         #convert Blockheight in hex which is stored Script signature
        """
        if self.is_coinbase():
            self.tx_ins[0].prev_tx = self.tx_ins[0].prev_tx.hex()
            self.tx_ins[0].script_sig.cmds[0] = little_to_int(self.tx_ins[0].script_sig.cmds[0])
            self.tx_ins[0].script_sig = self.tx_ins[0].script_sig.__dict__
        self.tx_ins[0] = self.tx_ins[0].__dict__
        """
            convert the transaction output to dict
            # if there are numbers we donot need to do anything 
            # if values is in bytes convert into hex
            # loop through all the tx_outs object and convert it into the dict
        """
        self.tx_outs[0].script_pubkey.cmds[2] = self.tx_outs[0].script_pubkey.cmds[2].hex()
        self.tx_outs[0].script_pubkey = self.tx_outs[0].script_pubkey.__dict__
        self.tx_outs[0] = self.tx_outs[0].__dict__
        return self.__dict__
    
    def sign_hash(self,input_index,script_pubkey):
        s = int_to_little_endian(self.version,4)
        s+= encode_varient(len(self.tx_ins))
        for i,tx_in in enumerate(self.tx_ins):
            if i == input_index:
                s+= TxIn(tx_in.prev_tx,tx_in.prev_index,script_pubkey).serialize()
            else:
                s+= TxIn(tx_in.prev_tx,tx_in.prev_index).serialize()
        s+= encode_varient(len(self.tx_outs))
        for tx_out in self.tx_outs:
            print(tx_out.__dict__)
            s+= tx_out.serialize()
        s+=int_to_little_endian(self.locktime,4)
        s+=int_to_little_endian(SIGHASH,4)
        h256 = hash256(s)
        return int.from_bytes(h256,'big')
        
    
    def sign_input(self,input_index,private_key,script_pubkey):
        z = self.sign_hash(input_index,script_pubkey)
        der = private_key.sign(z).der()
        sig = der + SIGHASH.to_bytes(1,'big')
        # compressed public key
        sec = private_key.point.sec()
        self.tx_ins[input_index].script_sig = Script([sig,sec])
        
    
class TxIn:
    def __init__(self,prev_tx,prev_index,script_sig = None,sequence = 0xffffffff) -> None:
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence
    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index,4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence,4)
        return result

class TxOut:
    def __init__(self,amount,script_pubkey) -> None:
        self.amount = amount
        self.script_pubkey = script_pubkey
    def serialize(self):
        result = int_to_little_endian(self.amount,4)
        result += self.script_pubkey.serialize()
        return result