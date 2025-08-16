import time

class Ledger:
    def __init__(self):
        self.chain = []

    def add_entry(self, node_id, update_hash):
        entry = {
            "node": node_id,
            "hash": update_hash,
            "timestamp": time.time()
        }
        self.chain.append(entry)

    def display(self):
        for entry in self.chain:
            print(entry)
