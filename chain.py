import hashlib, ecdsa, datetime, json

def SHA256(message):
    return hashlib.sha256(message).hexdigest()

MINT_PRIVATE_ADDRESS = "0700a1ad28a20e5b2a517c00242d3e25a88d84bf54dce9e1733e6096e6d6495e"
ec = ecdsa.EllipticCurve("secp256k1")
MINT_KEY_PAIR = ec.keyFromPrivate(MINT_PRIVATE_ADDRESS, "hex")
MINT_PUBLIC_ADDRESS = MINT_KEY_PAIR.getPublic("hex")

class Block:
    def init(self, timestamp = str(datetime.datetime.now().timestamp()), data = []):
        self.timestamp = timestamp
        self.data = data
        self.prevHash = ""
        self.nonce = 0
        self.hash = Block.getHash(self)

    @staticmethod
    def getHash(block):
        return SHA256(block.prevHash + block.timestamp + json.dumps(block.data) + block.nonce)

    def mine(self, difficulty):
        while not self.hash.startswith(("0" * difficulty)):
            self.nonce += 1
            self.hash = Block.getHash(self)

    @staticmethod
    def hasValidUserData(block, chain):
        return all(UserData.isValid(user_data, chain) for user_data in block.data)



class Blockchain:
    def init(self):
        initalCoinRelease = UserData(MINT_PUBLIC_ADDRESS, 1668413948380, {})
        self.array_user_data = []
        self.chain = [Block("", [initalCoinRelease])]
        self.difficulty = 3
        self.chain[0].mine(self.difficulty)
        self.blockTime = 30000
    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        block.prevHash = self.getLastBlock().hash
        block.hash = Block.getHash(block)
        block.mine(self.difficulty)
        self.chain.append(block)

        if int(self.getLastBlock().timestamp) - int(block.timestamp) < self.blockTime:
            self.difficulty += 1
        else:
            self.difficulty -= 1

    def addUserData(self, user_data):
        if UserData.isValid(user_data, self):
            self.array_user_data.append(user_data)

    def mineUserData(self, rewardAddress):
        blockUserData = list(self.array_user_data)
        if self.array_user_data:
            self.addBlock(Block(str(datetime.datetime.now().timestamp()), blockUserData))
        self.array_user_data = self.array_user_data[len(blockUserData):]

    def getLatestInfo(self, address):
        latestInfo = None
        for block in self.chain:
            for user_data in block.data:
                if user_data.uid == address:
                    latestInfo = user_data
        return latestInfo

    def getBalance(self, address):
        balance = 0
        return balance

    @staticmethod
    def isValid(blockchain):
        for i in range(1, len(blockchain.chain)):
            currentBlock = blockchain.chain[i]
            prevBlock = blockchain.chain[i-1]

            if (
                currentBlock.hash != Block.getHash(currentBlock) or 
                prevBlock.hash != currentBlock.prevHash or 
                not Block.hasValidUserData(currentBlock, blockchain)
            ):
                return False

        return True

class UserData:
    def init(self, uid, timestamp, data):
        self.uid = uid
        self.timestamp = timestamp
        self.data = data

    def sign(self, keyPair):
        if keyPair.getPublic("hex") == self.uid:
            self.signature = keyPair.sign(SHA256(self.uid + str(self.timestamp) + json.dumps(self.data)), "base64").toDER("hex")

    @staticmethod
    def isValid(tx, chain):
        return (
            tx.uid and
            tx.timestamp and
            tx.data and
            ec.keyFromPublic(tx.uid, "hex").verify(SHA256(tx.uid + str(tx.timestamp) + json.dumps(tx.data)), tx.signature)
        )


JeChain = Blockchain()

module = {'Block': Block, 'UserData': UserData, 'Blockchain': Blockchain, 'JeChain': JeChain}