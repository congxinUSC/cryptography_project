# Cryptography Project

## Background
This is just a programming assignment project of a cryptography course.
The assignment requires implementing a RSA-encrypted-key crypto system.
I'm creating this repository solely for practicing purposes.
There is **no security guarantee** in the project.
If you happen to be my classmate and wanted to take this as a reference for 
your own assignment you're more than welcome. **JUST DON'T COPY.**

## System Design
Mostly not my design, the assignment's requirements already specifies a lot.
#### Encryption
This is not a standard RSA encryption system. It actually encrypts the plaintext
with AES-128 (CTR mode) and then encrypts the AES key with RSA (2048 bit by 
default). The assignment only requires implementing the RSA part so I used 3rd 
party library for AES. The output file contains the ciphertext and encrypted AES
key.
#### Decryption
First decrypt the AES key with RSA then decrypt the ciphertext with it.
#### File formats
Again this project is not for security purposes so I simply used json-like 
format for convenience.
##### RSA public key file (*.pub)
```json
{
  "n": <RSA modula (Number)>,
  "e": <RSA public exponent (Number)>
}
```
##### RSA private key file (*.prv)
```json
{
  "n": <RSA modula (Number)>,
  "d": <RSA private exponent (Number)>
}
```
##### Ciphertext file
```json
{
  "key": <AES key ecrypted by RSA (Number)>,
  "ciphertext": <Base64 encoded ciphertext (String)>
}
```

## Development Settings
#### Programming language
This project is developed in [Python 3](https://docs.python.org/3/) 
Despite Python 2.7 will reach the end of its life on January 1st, 2020, if 
you're only comfortable with [Python 2](https://docs.python.org/2/), there is
 a tool [3to2](https://pypi.org/project/3to2/) that might be helpful for you.
#### Coding style
_Mainly_ (:smirk:) follows
[Google Python Style Guild](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).
#### Dependencies
We use [pycrypto](https://pypi.org/project/pycrypto/) for it's AES cipher.

## How to run
**Make sue you are running the right version of python (3), install dependencies
and assigned the scripts execution permission first.**

Say our old friend Alice wants Bob to send her some file `message.msg` secretly.
The first thing to do for her is to generate her RSA key pair:
```sh
./genkey.py alice
```
You'll get the public and private key stored in file `alice.pub` and `alice.prv`
respectively. Now Alice sends `alice.pub` to Bob and Bob should encrypt the file
`message.msg`:
```sh
./crypt.py -e alice.pub message.msg ciphertext.cip
```
Now Bob obtained the ciphertext file `ciphertext.cip` and send it back to Alice.
Then Alice could recover the message by decrypting it:
```sh
./crypt.py -d alice.prv ciphertext.cip message_from_bob.msg
```

## References
In addition to our wonderful course materials, this project's implementation 
details also refer to the following links:
- [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [Primality test](https://en.wikipedia.org/wiki/Primality_test)
- [Miller-Rabin primality test](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)
- [Size range for p and q in RSA](https://crypto.stackexchange.com/questions/48292/for-rsa-is-there-a-specified-size-range-for-p-and-q-when-calculating-n)
- [Carmichael totient funcition](https://en.wikipedia.org/wiki/Carmichael_function#%CE%BB(n)_divides_%CF%86(n))
- [Euler's totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function)
- [Public key selection](https://www.reddit.com/r/crypto/comments/6363di/how_do_computers_choose_the_rsa_value_for_e/)
- [Modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse)
- [Extended Euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)
- [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [CTR Mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR))