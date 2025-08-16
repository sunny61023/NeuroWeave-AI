import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def verify_update(update, signature, public_key_bytes):
    """Verify signed updates from other nodes"""
    public_key = load_pem_public_key(public_key_bytes)
    message = json.dumps(update).encode()
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False

def merge_knowledge(node, incoming_update):
    """
    Naive knowledge merging:
    Append new vocabulary and re-train local model (toy example).
    """
    vocab = set(node.vectorizer.get_feature_names_out())
    new_vocab = set(incoming_update["vocab"])
    combined_vocab = vocab.union(new_vocab)
    print(f"[{node.name}] Merged vocab size: {len(combined_vocab)}")
