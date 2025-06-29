facts = [
    ("parent", "john", "doe"),
    ("parent", "doe", "jane")
]

rules = [
    ("ancestor", ["X", "Y"], [("parent", "X", "Y")]),
    ("ancestor", ["X", "Z"], [("parent", "X", "Y"), ("ancestor", "Y", "Z")])
]

def unify(a, b, env):
    if a == b: return env
    if isinstance(a, str) and a.isupper():
        env = env.copy(); env[a] = b; return env
    if isinstance(b, str) and b.isupper():
        env = env.copy(); env[b] = a; return env
    return None

def match_fact(pred, args):
    for f in facts:
        if f[0] != pred: continue
        env = {}
        for fa, pa in zip(f[1:], args):
            env = unify(pa, fa, env)
            if env is None: break
        if env is not None:
            yield env

def resolve(goal, env):
    pred, args = goal[0], [env.get(x, x) for x in goal[1:]]
    yield from match_fact(pred, args)
    for rule in rules:
        if rule[0] != pred: continue
        local_env = env.copy()
        for subenv in resolve_all(rule[2], local_env):
            yield unify(goal[1], rule[1], subenv)

def resolve_all(goals, env):
    if not goals: yield env; return
    for e1 in resolve(goals[0], env):
        yield from resolve_all(goals[1:], e1)

print("Ancestors of jane:")
for res in resolve(("ancestor", "X", "jane"), {}):
    print(res["X"])
