def word_break(s, word_dict):
    memo = {}

    def dfs(start):
        if start == len(s): return True
        if start in memo: return memo[start]
        for end in range(start+1, len(s)+1):
            if s[start:end] in word_dict and dfs(end):
                memo[start] = True
                return True
        memo[start] = False
        return False

    return dfs(0)

dictionary = {"leet", "code", "python", "rocks"}
print(word_break("leetcode", dictionary))  # True
print(word_break("pythonrocks", dictionary))  # True
print(word_break("pythonsucks", dictionary))  # False
