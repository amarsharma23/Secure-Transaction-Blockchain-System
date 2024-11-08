import hashlib
import json
from time import time


class Block:
    def __init__(self, index, timestamp, transactions, prev_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = self.hash_block()
        print("Block has been created...")

    def hash_block(self):
        block_str = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.members = ['Account_A', 'Account_B', 'Account_C']
        self.create_block(prev_hash='1', proof=100)

    def create_block(self, proof, prev_hash=None):
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            prev_hash=prev_hash or self.chain[-1].hash
        )
        self.current_transactions = []
        self.chain.append(block)
        print("Approved by all members...")
        return block

    def add_transaction(self, sender, recipient, amount):
        if sender not in self.members:
            print(f"Transaction failed: Sender '{sender}' is not a member.")
            if self.prompt_add_member(sender):
                self.members.append(sender)
                print(f"{sender} has been added as a member.")
            else:
                return None

        if recipient not in self.members:
            print(f"Transaction failed: Recipient '{recipient}' is not a member.")
            if self.prompt_add_member(recipient):
                self.members.append(recipient)
                print(f"{recipient} has been added as a member.")
            else:
                return None

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        print("Conducting transactions..")
        return self.last_block.index + 1

    def prompt_add_member(self, name):
        response = input(f"Would you like to add '{name}' as a member? (Y/N): ").strip().upper()
        return response == 'Y'

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            block = self.chain[i]
            if block.prev_hash != prev_block.hash:
                return False
            if not self.valid_proof(prev_block.hash, block.proof):
                return False
        return True

    def validate_transaction(self):
        print("Validating transaction by members...")
        for member in self.members:
            print(f"{member} is validating the transaction.")
        return True


def main():
    blockchain = Blockchain()

    while True:
        print("\n1. Add Transaction")
        print("2. Mine Block")
        print("3. Display Blockchain")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            sender = input("Enter sender: ")
            recipient = input("Enter recipient: ")
            amount = float(input("Enter amount: "))
            if blockchain.validate_transaction():
                blockchain.add_transaction(sender, recipient, amount)
                print("Transaction added.")

        elif choice == '2':
            last_proof = blockchain.last_block.hash
            proof = blockchain.proof_of_work(last_proof)
            prev_hash = blockchain.last_block.hash
            blockchain.create_block(proof, prev_hash)
            print("Block mined and added to blockchain.")

        elif choice == '3':
            for block in blockchain.chain:
                print(f'\nIndex: {block.index}')
                print(f'Timestamp: {block.timestamp}')
                print(f'Transactions: {block.transactions}')
                print(f'Hash: {block.hash}')
                print('---')

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
