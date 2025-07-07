def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1

def modular_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    return x % m

def generate_inverse_table(mod):
    print(f"Modular Inverse Table mod {mod}")
    for a in range(1, mod):
        inv = modular_inverse(a, mod)
        if inv:
            print(f"{a:2} × {inv:2} ≡ 1 mod {mod}")
        else:
            print(f"{a:2} has no inverse mod {mod} (not coprime)")

generate_inverse_table(17)
