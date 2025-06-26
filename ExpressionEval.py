def precedence(op):
    return {'+':1, '-':1, '*':2, '/':2}.get(op, 0)

def apply_op(a, b, op):
    return {'+': a+b, '-': a-b, '*': a*b, '/': a//b}[op]

def evaluate(expr):
    values, ops = [], []
    i = 0
    while i < len(expr):
        if expr[i] == ' ':
            i += 1
            continue
        if expr[i].isdigit():
            val = 0
            while i < len(expr) and expr[i].isdigit():
                val = val * 10 + int(expr[i])
                i += 1
            values.append(val)
            continue
        elif expr[i] == '(':
            ops.append(expr[i])
        elif expr[i] == ')':
            while ops[-1] != '(':
                b, a = values.pop(), values.pop()
                values.append(apply_op(a, b, ops.pop()))
            ops.pop()
        else:
            while ops and precedence(ops[-1]) >= precedence(expr[i]):
                b, a = values.pop(), values.pop()
                values.append(apply_op(a, b, ops.pop()))
            ops.append(expr[i])
        i += 1
    while ops:
        b, a = values.pop(), values.pop()
        values.append(apply_op(a, b, ops.pop()))
    return values[0]
