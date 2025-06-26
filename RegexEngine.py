def match(text, pattern):
    if not pattern:
        return not text
    first_match = bool(text) and (pattern[0] == text[0] or pattern[0] == '.')
    if len(pattern) >= 2 and pattern[1] == '*':
        return (match(text, pattern[2:]) or
                (first_match and match(text[1:], pattern)))
    else:
        return first_match and match(text[1:], pattern[1:])

# Examples
print(match("aab", "c*a*b"))  # True
print(match("miss", "mis*"))  # True
print(match("miss", "mis"))   # False
