"""This script encrypts or decrypts file with RSA-encrypted-key-AES."""
import base64
import json
import random
import sys

from Crypto.Cipher import AES
from Crypto.Util import Counter


AES_KEY_SIZE = 128


def encrypt(key_file: str, in_file: str, out_file: str):
    """Encrypts in_file using AES with randomly generated key, then encrypt the
    key with RSA and pack them into out_file.

    File formats are described in docs.

    Args:
        key_file: Path of the file storing the RSA public key.
        in_file: Path of the file to encrypt.
        out_file: Path of the output encrypted file.
    """
    # Generate random key and create AES cipher
    key = random.SystemRandom().getrandbits(AES_KEY_SIZE)
    counter = Counter.new(AES_KEY_SIZE)
    cipher = AES.new(key.to_bytes(AES_KEY_SIZE // 8, "little"),
                     AES.MODE_CTR,
                     counter=counter)

    # Encrypt the plaintext with the cipher
    with open(in_file, "rb") as in_fp:
        plaintext = in_fp.read()
        ciphertext = cipher.encrypt(plaintext)

    # Encrypt the AES key with RSA
    with open(key_file) as public_key_fp:
        public_key = json.load(public_key_fp)
        encrypted_key = pow(key, public_key["e"], public_key["n"])

    # Save the encrypted AES key and ciphertext
    with open(out_file, "w") as out_fp:
        # Use Base64 to encode the ciphertext so we can simply store it in json
        encoded_ciphertext = base64.encodebytes(ciphertext).decode()
        secret = {"key": encrypted_key, "ciphertext": encoded_ciphertext}
        json.dump(secret, out_fp)


def decrypt(key_file: str, in_file: str, out_file: str):
    """Decrypts in_file using AES with randomly generated key, then encrypt the
    key with RSA and pack them into out_file.

    File formats are described in docs.

    Args:
        key_file: Path of the file storing the RSA public key.
        in_file: Path of the file to encrypt.
        out_file: Path of the output encrypted file.
    """
    with open(in_file) as in_fp:
        secret = json.load(in_fp)
        encrypted_key = secret["key"]
        encoded_ciphertext = secret["ciphertext"]
        ciphertext = base64.decodebytes(encoded_ciphertext.encode())

    with open(key_file) as private_key_fp:
        private_key = json.load(private_key_fp)
        n = private_key["n"]
        d = private_key["d"]

    key = pow(encrypted_key, d, n)
    counter = Counter.new(AES_KEY_SIZE)
    cipher = AES.new(key.to_bytes(AES_KEY_SIZE // 8, "little"),
                     AES.MODE_CTR,
                     counter=counter)

    with open(out_file, "wb") as out_fp:
        out_fp.write(cipher.decrypt(ciphertext))


def main(argv):
    """Run encryption or decryption based on the first command line argument."""
    if argv[1] == "-e":
        encrypt(argv[2], argv[3], argv[4])
    if argv[1] == "-d":
        decrypt(argv[2], argv[3], argv[4])


if __name__ == '__main__':
    main(sys.argv)
