import hashlib
from typing import List

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def double_sha256(data: bytes) -> bytes:
    return sha256(sha256(data))

def merkle_tree(txid_list: List[bytes]) -> List[List[bytes]]:
    if not txid_list:
        return []

    tree = [txid_list]

    while len(tree[-1]) > 1:
        layer = []
        for i in range(0, len(tree[-1]), 2):
            left = tree[-1][i]
            right = tree[-1][i + 1] if i + 1 < len(tree[-1]) else left
            layer.append(double_sha256(left + right))
        tree.append(layer)

    return tree

def merkle_root(txid_list: List[bytes]) -> bytes:
    tree = merkle_tree(txid_list)
    return tree[-1][0] if tree else b''

# Example usage
txids = [
    "8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87",
    "fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4",
    "6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4",
    "e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d"
]
txid_bytes = [bytes.fromhex(txid) for txid in txids]
root = merkle_root(txid_bytes)
print(f"Merkle root: {root.hex()}")
