# part_c_answers.py
# Part C - Conceptual answers + memoize + bugfix

# ==============================================================
# Q1 - LEGB Rule (conceptual, explained in comments here)
# ==============================================================
# LEGB stands for:
#   L - Local     : Variables inside the current function
#   E - Enclosing : Variables in any enclosing (outer) function (for closures)
#   G - Global    : Variables at the top level of the module
#   B - Built-in  : Python's own built-in names (len, print, etc.)
#
# Python looks up a name in this order: L -> E -> G -> B
#
# Example:
x = "global x"          # G - Global scope

def outer():
    x = "enclosing x"   # E - Enclosing scope

    def inner():
        x = "local x"   # L - Local scope
        print(x)        # Prints "local x" (finds it in L first)

    inner()

outer()   # Output: local x

# What happens if local and global share the same name?
# Python will use the local one and never touch the global one.

# The 'global' keyword forces Python to use the module-level variable.
# Example:
counter = 0

def increment():
    global counter      # Without this, assigning counter = ... would create a local variable
    counter += 1

increment()
print(counter)          # Prints 1

# Why is 'global' a code smell?
# It makes functions depend on external state, making code harder to test,
# debug, and reason about. Functions should ideally be pure and self-contained.
#
# Better alternative: pass the value as a parameter and return the new value.
def increment_clean(counter: int) -> int:
    return counter + 1

counter = 0
counter = increment_clean(counter)
print(counter)          # Prints 1 — no global needed



# ==============================================================
# Q2 - memoize decorator
# ==============================================================

def memoize(func):
    """Cache results of a function so repeated calls with same args are fast.

    Args:
        func: The function to memoize.

    Returns:
        Wrapped function that uses a cache dict to skip recomputation.

    Example:
        @memoize
        def fibonacci(n):
            ...
    """
    cache = {}      # key: args tuple, value: result

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memoize
def fibonacci(n):
    """Fibonacci using recursion — fast because of memoize cache."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Demo
import time

start = time.time()
print(f"fibonacci(50) = {fibonacci(50)}")
end = time.time()
print(f"Time taken: {end - start:.6f} seconds")



# ==============================================================
# Q3 - Bug fix
# ==============================================================

# ---- ORIGINAL BUGGY CODE ----
# total = 0
#
# def add_to_cart(item, cart=[]):         # Bug 1: mutable default argument
#     cart.append(item)
#     total = total + len(cart)            # Bug 2: UnboundLocalError (scope bug)
#     return cart
#
# print(add_to_cart('apple'))
# print(add_to_cart('banana'))   # Prints ['apple', 'banana'] because cart is shared!

# ---- BUG EXPLANATIONS ----
# Bug 1: cart=[] is evaluated ONCE when Python loads the function definition.
#        So every call that doesn't pass a cart uses the SAME list object.
#        After add_to_cart('apple'), that default list is ['apple'].
#        Then add_to_cart('banana') appends to the same list => ['apple', 'banana'].
#        Fix: use None as default, then create a new list inside the function.
#
# Bug 2: Inside the function, Python sees 'total = ...' and treats 'total' as
#        a local variable. But on the right-hand side, 'total' hasn't been
#        assigned yet locally, so Python raises UnboundLocalError.
#        Fix: pass total as a parameter and return the updated value.

# ---- FIXED VERSION ----
def add_to_cart_fixed(item: str, cart: list = None, total: int = 0):
    """Add item to cart and update total.

    Args:
        item: Item name to add.
        cart: Current cart list. Defaults to a new empty list each call.
        total: Running total count. Defaults to 0.

    Returns:
        Tuple of (updated_cart, updated_total).
    """
    if cart is None:        # Bug 1 fixed: new list created each time
        cart = []
    cart.append(item)
    total = total + len(cart)   # Bug 2 fixed: total is a local param now
    return cart, total


# Demo of fixed code
cart1, total1 = add_to_cart_fixed('apple')
print(f"After apple: cart={cart1}, total={total1}")   # ['apple'], 1

cart2, total2 = add_to_cart_fixed('banana')
print(f"After banana: cart={cart2}, total={total2}")  # ['banana'], 1  (fresh cart)

# If you want to keep adding to the same cart, pass it explicitly:
cart, total = [], 0
cart, total = add_to_cart_fixed('apple', cart, total)
cart, total = add_to_cart_fixed('banana', cart, total)
print(f"Persistent cart: {cart}, total={total}")      # ['apple', 'banana'], 3
