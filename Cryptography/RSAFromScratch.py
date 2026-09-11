import random

def is_probable_prime(n, rounds=40):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(rounds):  # Miller-Rabin
        x = pow(random.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def random_prime(bits):
    while True:
        candidate = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_probable_prime(candidate):
            return candidate

def generate_keys(bits=512, e=65537):
    p = random_prime(bits)
    q = random_prime(bits)
    while q == p:
        q = random_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return (e, n), (d, n), (p, q)

def encrypt(message, public):
    e, n = public
    m = int.from_bytes(message.encode(), 'big')
    if m >= n:
        raise ValueError("message longer than the modulus")
    return pow(m, e, n)

def decrypt(cipher, private):
    d, n = private
    m = pow(cipher, d, n)
    return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()

def sign(message, private):
    d, n = private
    return pow(int.from_bytes(message.encode(), 'big'), d, n)

def verify(message, signature, public):
    e, n = public
    return pow(signature, e, n) == int.from_bytes(message.encode(), 'big')

# Textbook RSA -- no padding, so this is for learning, not for real traffic.
public, private, (p, q) = generate_keys()
print(f"p = {p}\nq = {q}\nn = {public[1]}\n")

message = "attack at dawn"
cipher = encrypt(message, public)
print("Message  :", message)
print("Ciphertext:", cipher)
print("Decrypted:", decrypt(cipher, private))

signature = sign(message, private)
print("\nSignature verifies    :", verify(message, signature, public))
print("Tampered text verifies:", verify("retreat at dawn", signature, public))
