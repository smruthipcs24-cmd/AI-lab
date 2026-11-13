def is_variable(x):
    return isinstance(x, str) and x.islower()


def substitute(x, subst):
    if is_variable(x) and x in subst:
        return substitute(subst[x], subst)

    if isinstance(x, tuple):
        return tuple([x[0]] + [substitute(a, subst) for a in x[1:]])

    return x


def occurs(var, x, subst):
    x = substitute(x, subst)

    if var == x:
        return True

    if isinstance(x, tuple):
        return any(occurs(var, a, subst) for a in x[1:])

    return False


def unify(x, y, subst=None):
    if subst is None:
        subst = {}

    x = substitute(x, subst)
    y = substitute(y, subst)

    if x == y:
        return subst

    if is_variable(x):
        if occurs(x, y, subst):
            return None
        subst[x] = y
        return subst

    if is_variable(y):
        if occurs(y, x, subst):
            return None
        subst[y] = x
        return subst

    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x) != len(y):
            return None

        for a, b in zip(x[1:], y[1:]):
            subst = unify(a, b, subst)

            if subst is None:
                return None

        return subst

    return None


def display(expr):
    if isinstance(expr, tuple):
        return expr[0] + "(" + ", ".join(display(a) for a in expr[1:]) + ")"
    return str(expr)


test_cases = [
    (("Eats", "x", "Apple"), ("Eats", "Riya", "y")),
    (("Knows", "John", "x"), ("Knows", "x", "Elisabeth")),
    (("Likes", "x", "Mango"), ("Likes", "Ravi", "Mango")),
    (("P", "x", "y"), ("Q", "a", "b")),
    (("P", "x", "y"), ("P", "a"))
]


for i, (expr1, expr2) in enumerate(test_cases, 1):
    print(f"\n========== TEST CASE {i} ==========")
    print("Expression 1 :", display(expr1))
    print("Expression 2 :", display(expr2))

    result = unify(expr1, expr2)

    if result is None:
        print("Status       : Unification Failed")
    else:
        print("Status       : Unification Successful")
        print("Substitutions:")

        if result:
            for var, value in result.items():
                print(f"  {var} -> {display(substitute(value, result))}")
        else:
            print("  No substitutions required")

        print("Unified Form :", display(substitute(expr1, result)))

    print("=================================")
