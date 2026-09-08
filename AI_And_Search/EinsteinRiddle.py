from itertools import permutations

def einstein_solver():
    colors = ['red', 'green', 'white', 'yellow', 'blue']
    nations = ['brit', 'swede', 'dane', 'norwegian', 'german']
    drinks = ['tea', 'coffee', 'milk', 'beer', 'water']
    pets = ['dog', 'bird', 'cat', 'horse', 'fish']
    smokes = ['pallmall', 'dunhill', 'blend', 'blueMaster', 'prince']

    for c in permutations(colors):
        if c.index('green') != c.index('white') - 1: continue
        for n in permutations(nations):
            if n[c.index('red')] != 'brit': continue
            if n[0] != 'norwegian': continue
            for d in permutations(drinks):
                if d[n.index('dane')] != 'tea': continue
                if d[c.index('green')] != 'coffee': continue
                if d[2] != 'milk': continue
                for p in permutations(pets):
                    if p[n.index('swede')] != 'dog': continue
                    for s in permutations(smokes):
                        if s[p.index('bird')] != 'pallmall': continue
                        if c[s.index('dunhill')] != 'yellow': continue
                        if abs(s.index('blend') - p.index('cat')) != 1: continue
                        if abs(s.index('dunhill') - p.index('horse')) != 1: continue
                        if abs(s.index('blend') - d.index('water')) != 1: continue
                        if s[d.index('beer')] != 'blueMaster': continue
                        if s[n.index('german')] != 'prince': continue
                        return nations[p.index('fish')]

print("The person who owns the fish is:", einstein_solver())
