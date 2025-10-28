import hashlib
import time
from typing import List, Dict

class SimplePQSignature:
    """Simplified Dilithium-like PQ Signature (multi-SHA3 layers for quantum resistance)."""
    def __init__(self):
        self.private_key = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()

    def sign(self, message: str) -> str:
        msg_hash = message.encode()
        for _ in range(10):  # Simulate lattice-based multi-hash for PQ security
            msg_hash = hashlib.sha3_256(msg_hash).digest()
        return self.public_key + ':' + msg_hash.hex()

    def verify(self, message: str, signature: str) -> bool:
        expected_sig = self.sign(message)
        return signature == expected_sig

class AetherBlock:
    def __init__(self, index: int, transactions: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.ai_threat_score = 0.05  # Simulated AI prediction (0-1 risk)
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.signature = None

    def calculate_hash(self) -> str:
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}{self.ai_threat_score}"
        return hashlib.sha3_256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int, pq_signer: SimplePQSignature):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        block_msg = f"{self.index}:{self.hash}:{self.ai_threat_score}"
        self.signature = pq_signer.sign(block_msg)
        print(f"Block mined: {self.hash} with nonce {self.nonce}, AI score {self.ai_threat_score}")

class AetherChain:
    def __init__(self):
        self.chain: List[AetherBlock] = []
        self.difficulty = 4
        self.pq_signer = SimplePQSignature()
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_transactions = [{"from": "genesis", "to": "creator", "amount": 100}]
        genesis_block = AetherBlock(0, genesis_transactions, "0")
        genesis_block.mine_block(self.difficulty, self.pq_signer)
        self.chain.append(genesis_block)

    def add_transaction(self, transaction: Dict):
        if len(self.chain) > 0:
            new_block = AetherBlock(len(self.chain), [transaction], self.chain[-1].hash)
            new_block.mine_block(self.difficulty, self.pq_signer)
            self.chain.append(new_block)
            print(f"Transaction added: {transaction}")
        else:
            print("Chain not started!")

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash() or current.previous_hash != previous.hash:
                return False
            if not self.pq_signer.verify(f"{current.index}:{current.hash}:{current.ai_threat_score}", current.signature):
                return False
        return True

# Demo: Run the chain
aether = AetherChain()
aether.add_transaction({"from": "alice", "to": "bob", "amount": 10})
print(f"Chain valid: {aether.is_chain_valid()}")
print(f"Total blocks: {len(aether.chain)}")
print("Genesis Hash:", aether.chain[0].hash)
print("Block 1 Hash:", aether.chain[1].hash if len(aether.chain) > 1 else "N/A")