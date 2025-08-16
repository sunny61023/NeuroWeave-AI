import json
import sqlite3
import uuid
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class AINode:
    def __init__(self, name="Node"):
        self.id = str(uuid.uuid4())[:8]
        self.name = name

        # Cryptographic keys for signing updates
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

        # Simple ML pipeline (text classification demo)
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()

        # Local SQLite storage
        self.conn = sqlite3.connect(f"{self.id}_node.db")
        self.create_storage()

    def create_storage(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS knowledge (data TEXT)")
        self.conn.commit()

    def learn(self, texts, labels):
        """Train a simple ML model on user data"""
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

        # Save knowledge locally
        self.conn.execute("INSERT INTO knowledge VALUES (?)", (json.dumps(texts),))
        self.conn.commit()

    def compress_knowledge(self):
        """Extract compressed model coefficients (not raw data)"""
        return {
            "id": self.id,
            "vocab": self.vectorizer.get_feature_names_out().tolist(),
            "coef": self.model.coef_.tolist(),
            "classes": self.model.classes_.tolist()
        }

    def sign_update(self, update):
        """Sign the update with private key"""
        message = json.dumps(update).encode()
        signature = self.private_key.sign(
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return signature

    def get_public_key_bytes(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
