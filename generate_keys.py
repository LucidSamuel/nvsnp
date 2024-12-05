from ecdsa import SigningKey, SECP256k1
import hashlib

private_key = SigningKey.generate(curve=SECP256k1)
print(f"Private Key: {private_key.to_string().hex()}")

public_key = private_key.get_verifying_key()
print(f"Public Key (x, y): ({public_key.pubkey.point.x()}, {public_key.pubkey.point.y()})")

message = "Hello, Noir!"
hashed_message = int(hashlib.sha256(message.encode()).hexdigest(), 16)
print(f"Hashed Message: {hashed_message}")

signature = private_key.sign_deterministic(message.encode(), hashfunc=hashlib.sha256)
r = int(signature[:32].hex(), 16)
s = int(signature[32:].hex(), 16)
print(f"Signature (r, s): ({r}, {s})")

n = SECP256k1.order  # Curve order
generator = SECP256k1.generator
print(f"Curve Order (n): {n}")
print(f"Generator (x, y): ({generator.x()}, {generator.y()})")
