print("Please write in this format: '{number}' '{operator}' '{number}'")
 
while True:
    try:
        a = input("➤ ")
        one, two, three = a.split()

        n1 = int(one)
        op = two
        n2 = int(three)

        if op == "+":
            res = n1 + n2
        elif op == "-":
            res = n1 - n2
        elif op == "*":
            res = n1 * n2
        elif op == "/":
            res = n1 / n2
        elif op == "%":
            res = n1 % n2
        else:
            print("❌ Invalid operator! Use +, -, *, /, or %.")
            continue

        print("✅ Result:", res)
        break

    except ValueError:
        print("❌ Please enter valid numbers!")
    except ZeroDivisionError:
        print("❌ Cannot divide by zero!")
