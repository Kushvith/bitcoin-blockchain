import json
import os


class BaseDb:
    def __init__(self) -> None:
        self.basePath = "data"
        self.filePath = "/".join((self.basePath,self.filename))
    def read(self):
        if not os.path.exists(self.filePath):
            print(f"file {self.filePath} not available")
            return False
        with open(self.filePath,'r') as file:
            raw = file.readline()
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []
        return data
            
    def write(self,item):
        data = self.read()
        if data:
            data = data + item
        else:
            data = item
        with open(self.filePath,"w+") as file:
            file.write(json.dumps(data)) 
class BlockChainDb(BaseDb):
    def __init__(self):
        self.filename = "blockchain"
        super().__init__()
    
    def lastBlock(self):
        data = self.read()
        if data:
            return data[-1]
        
class AccountDb(BaseDb):
    def __init__(self):
        self.filename = "account"
        super().__init__()