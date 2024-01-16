import hashlib
import json
from datetime import datetime, timedelta    

class Block:
    def __init__(self, prevHash, data):
        #Define block information
        self.prevHash = prevHash
        self.data = data
        self.timeStamp = datetime.now()
        self.nonce = 0
        self.totalTime = ""
        self.hash = self.calculateHash()
        
    def calculateHash(self):
        #Define mining function
        startTime = datetime.now()
        st = (self.prevHash + json.dumps(self.data) + str(self.timeStamp) + str(self.nonce)).encode('utf-8')
        st = hashlib.sha256(st).hexdigest()
        while (not st.startswith("00000")):
            self.nonce += 1
            st = (self.prevHash + json.dumps(self.data) + str(self.timeStamp) + str(self.nonce)).encode('utf-8')
            st = hashlib.sha256(st).hexdigest()
        endTime = datetime.now()
        self.totalTime = endTime-startTime
        return st
    
class BlockChain:
    def __init__(self):
        self.blocks = []
        genesisBlock = Block("",[{"isGenesis":True}])
        self.blocks.append(genesisBlock)
    
    def getLastBlock(self):
        return self.blocks[-1]
    
    def addBlock(self, data):
        prevBlock = self.getLastBlock()
        currBlock = Block(prevBlock.hash,data)
        self.blocks.append(currBlock)
        
    def isValid(self):
        for i in range(1,len(self.blocks)):
            prevBlock = self.blocks[i-1]
            currBlock = self.blocks[i]
            if (currBlock.calculateHash() != currBlock.hash):
                return False
            if (prevBlock.hash != currBlock.prevHash):
                return False
        return True

#Testing
bongoChain = BlockChain()
bongoChain.addBlock([
    {"from":"Bongo", "to":"Dat", "amount":1000},
    {"from":"Bongo", "to":"Cuong", "amount":640},
    {"from":"Bongo", "to":"Hoai", "amount":230}
])
bongoChain.addBlock([
    {"from":"Dat", "to":"Cuong", "amount":500},
    {"from":"Dat", "to":"Hoai", "amount":200}
])
bongoChain.addBlock([
    {"from":"Hoai", "to":"Cuong", "amount":400}
])

print("isValid? ",bongoChain.isValid())
print()

for block in bongoChain.blocks:
    print("prevHash: ",block.prevHash)
    print("hash: ",block.hash)
    print("data: ",block.data)
    print("totalTime: ",block.totalTime)
    print("Tries: ",block.nonce)
    print()