def hide_message(msg):
    result = ''
    for char in msg:
        binary = format(ord(char), '08b')
        for bit in binary:
            result += '█' if bit == '1' else ' '
        result += '\n'
    return result

def reveal_message(hidden_art):
    lines = hidden_art.strip().split('\n')
    message = ''
    for line in lines:
        bits = ''.join(['1' if ch == '█' else '0' for ch in line])
        message += chr(int(bits, 2))
    return message

# Example
hidden = hide_message("Hi")
print("🔐 Hidden message:")
print(hidden)
print("🕵️ Revealed message:", reveal_message(hidden))
