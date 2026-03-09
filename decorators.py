# decorators.py
# Part B - Custom Python Decorators

import time
import functools


def timer(func):
    """Decorator that measures and prints how long a function takes to run.

    Args:
        func: The function to wrap.

    Returns:
        Wrapper function with timing added.

    Example:
        @timer
        def slow_function():
            time.sleep(1)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        print(f"[timer] '{func.__name__}' took {elapsed:.4f} seconds")
        return result
    return wrapper


def logger(func):
    """Decorator that logs function name, arguments, and return value.

    Args:
        func: The function to wrap.

    Returns:
        Wrapper function with logging added.

    Example:
        @logger
        def add(a, b):
            return a + b
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[logger] Calling '{func.__name__}' with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[logger] '{func.__name__}' returned: {result}")
        return result
    return wrapper


def retry(max_attempts: int = 3):
    """Decorator factory that retries a function on exception.

    Args:
        max_attempts: Maximum number of times to try the function. Default is 3.

    Returns:
        A decorator that wraps the function with retry logic.

    Raises:
        Exception: Re-raises the last exception if all attempts fail.

    Example:
        @retry(max_attempts=3)
        def unstable_call():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"[retry] Attempt {attempt}/{max_attempts} failed: {e}")
            print(f"[retry] All {max_attempts} attempts failed.")
            raise last_exception
        return wrapper
    return decorator


# --- Demo when run directly ---
if __name__ == "__main__":

    # Test @timer
    print("=== @timer Demo ===")
    @timer
    def compute_sum(n):
        return sum(range(n))

    result = compute_sum(1_000_000)
    print(f"Result: {result}\n")


    # Test @logger
    print("=== @logger Demo ===")
    @logger
    def add(a, b):
        return a + b

    add(10, 20)
    print()


    # Test @retry — succeeds on 3rd attempt
    print("=== @retry Demo ===")
    attempt_count = 0

    @retry(max_attempts=3)
    def flaky_function():
        global attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ValueError("Not ready yet")
        return "Success!"

    output = flaky_function()
    print(f"Final output: {output}\n")


    # Test @retry — all attempts fail
    print("=== @retry (all fail) Demo ===")
    @retry(max_attempts=2)
    def always_fails():
        raise RuntimeError("This always fails")

    try:
        always_fails()
    except RuntimeError as e:
        print(f"Caught expected exception: {e}")


    # Test stacking decorators
    print("\n=== Stacked @timer + @logger Demo ===")
    @timer
    @logger
    def multiply(x, y):
        return x * y

    multiply(7, 6)
