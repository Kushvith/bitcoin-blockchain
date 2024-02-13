import sys
sys.path.append('/programs/python/blockchain')
import time
from backend.core.Tx import Tx, TxIn, TxOut
from backend.core.database.database import AccountDb
from backend.util.util import decode_base64
from backend.core.Script import Script
from backend.core.EllepticCurve.EllepticCurve import PrivateKey
class SendBitcoin:
    def __init__(self,fromAccount,toAccount,Amount,UTOxS):
        self.COIN = 10
        self.FromPublicAddress = fromAccount
        self.toAccount = toAccount
        self.Amount = Amount * self.COIN
        self.UTOxs = UTOxS
    def scriptPubKey(self,publicAddress):
        h160 = decode_base64(publicAddress)
        script_publicKey = Script.p2pkh_script(h160)
        return script_publicKey
    def getPrivateKey(self):
        AllAccounts = AccountDb().read()
        for account in AllAccounts:
            if account['publicAddress'] == self.FromPublicAddress:
                return account['privateKey']
    def prepareTxIn(self):
        TxIns = []
        self.Total = 0
        """convert public addreess into public hash to find tx_outs that are locked to hasj"""
        self.From_address_script_pubkey = self.scriptPubKey(self.FromPublicAddress)
        self.fromPubKeyHash = self.From_address_script_pubkey.cmds[2]
        newUtoxs = {}
        try:
            while len(newUtoxs) < 1:
                newUtoxs = dict(self.UTOxs)
                time.sleep(2)
        except Exception as e:
            print("error in converting the managed dict to normal dict")
        
        for Txbyte in newUtoxs:
            if self.Total < self.Amount:
                TxObj = newUtoxs[Txbyte]
                for index,txout in enumerate(TxObj.tx_outs):
                    if txout.script_pubkey.cmds[2] ==self.fromPubKeyHash:
                        self.Total += txout.amount
                        print(self.Total)
                        prev_tx = bytes.fromhex(TxObj.id())
                        TxIns.append(TxIn(prev_index=index,prev_tx=prev_tx))
                else:
                    break
        self.isBalanceEnough = True
        if self.Amount < self.Total:
            self.isBalanceEnough = False
        return TxIns
                 
        
    def prepareTxOut(self):
        Txouts = []
        to_ScriptPubKey = self.scriptPubKey(self.toAccount)
        Txouts.append(TxOut(self.Amount,to_ScriptPubKey))
        """calculate fee"""
        self.fee = self.COIN
        self.changeAmount = self.Total - self.Amount - self.fee
        Txouts.append(TxOut(self.changeAmount,self.From_address_script_pubkey))
        return Txouts
    def signTx(self):
        secreat = self.getPrivateKey()
        priv = PrivateKey(secret=secreat)
        for index,input in enumerate(self.TxIns):
            self.Txobj.sign_input(index,priv,self.From_address_script_pubkey)
        return True
    def prepareTransaction(self):
        self.TxIns = self.prepareTxIn()
        print(self.isBalanceEnough)
        if self.isBalanceEnough:
            self.TxOuts = self.prepareTxOut()
            self.Txobj = Tx(1,self.TxIns,self.TxOuts,0)
            print(3)
            self.signTx()
            return True
        return False        