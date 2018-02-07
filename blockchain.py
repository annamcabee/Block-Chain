import collections
import datetime
import hashlib
import json


class InvalidBlockChain(BaseException):
    pass


class Block(object):
    def __init__(self, data):
        self.timestamp = str(datetime.datetime.utcnow().date)
        self.index = None
        self.previous_hash = None
        self.data = data

    @property
    def hash(self):
        return hashlib.sha256(
            json.dumps(dict(
                index=self.index,
                timestamp=self.timestamp,
                data=str(self.data),
                previous_hash=self.previous_hash
            )).encode('utf-8')).hexdigest()

    def __repr__(self):
        return """
         Block #{index}
         Data:{data}
         Block Hash:{hash}
         Block Previous Hash: {previous_hash}
        """.format(index=self.index, data=self.data, hash=self.hash, previous_hash=self.previous_hash)


class BlockChain(object):
    def __init__(self, *blocks):
        self.chain = []
        self.append(Block("Genesis Block"))

        for block in blocks:
            self.append(block)

    def __len__(self):
        return len(self.chain)

    def __getitem__(self, index):
        return self.chain.__getitem__(index)

    def append(self, block):
        block.previous_hash = self.chain[-1].hash if self else ""
        block.index = self.__len__()
        self.chain.append(block)

    def validate(self):
        for previous_block, current_block in zip(self, self[1:]):
            if not current_block.previous_hash == previous_block.hash:
                raise InvalidBlockChain()

    def __repr__(self):
        return "------------".join([str(block) for block in self.chain])


def main():
    coin = BlockChain(
        Block({"account": "Anna", "amount": 25, "action": "buy"}),
        Block({"account": "Joe", "amount": 10, "action": "buy"}),
        Block({"account": "Ethan", "amount": 4, "action": "buy"})
    )
    block = Block({"account": "Katie", "amount": 20, "action": "buy"})
    coin.append(block)
    try:
        coin.validate()
        print("Block chain is valid")
    except InvalidBlockChain:
        print("Block chain is invalid")

    coin[1].data = {"account": "Anna", "amount": 100, "action": "buy"}

    try:
        coin.validate()
        print("Block chain is valid")
    except InvalidBlockChain:
        print("Block chain is invalid")


if __name__ == '__main__':
    main()
