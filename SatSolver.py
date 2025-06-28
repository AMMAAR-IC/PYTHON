from itertools import product

def sat_solver(clauses, variables):
    for vals in product([False, True], repeat=len(variables)):
        env = dict(zip(variables, vals))
        if all(any((lit if isinstance(lit, bool) else env.get(lit[1:], not env[lit])) 
                   if isinstance(lit, str) and lit.startswith('~') 
                   else env[lit] for lit in clause) for clause in clauses):
            return env
    return None

vars = ['A', 'B', 'C']
clauses = [['A', '~B'], ['B', 'C'], ['~A', '~C']]
solution = sat_solver(clauses, vars)
print("✅ Satisfiable:", solution if solution else "❌ Unsatisfiable")
