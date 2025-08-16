from src.node import AINode
from src.weave import verify_update, merge_knowledge
from src.ledger import Ledger
from src.visualize import visualize_mesh
import hashlib

# Create two nodes
node1 = AINode("Node-Alpha")
node2 = AINode("Node-Beta")
ledger = Ledger()

# Node 1 learns from local data
texts = ["AI is amazing", "Decentralized systems are powerful", "I love machine learning"]
labels = ["positive", "positive", "positive"]
node1.learn(texts, labels)

# Node 1 prepares update
update = node1.compress_knowledge()
signature = node1.sign_update(update)
public_key_bytes = node1.get_public_key_bytes()

# Node 2 verifies update
if verify_update(update, signature, public_key_bytes):
    print("[Node2] Update verified ✅")
    merge_knowledge(node2, update)

    # Record in ledger
    update_hash = hashlib.sha256(str(update).encode()).hexdigest()
    ledger.add_entry(node1.id, update_hash)

# Show trust ledger
print("\n📜 Ledger State:")
ledger.display()

# Visualize
visualize_mesh([(node1.name, node2.name)])
