# Recursive Factorial
def factorial(n) -> int:
    if n < 0:
        raise ValueError(f"Factorial is not defined for negative numbers.")

    elif n == 0 or n == 1:
        return 1

    else:
        return n * factorial(n - 1)

print(f"Factorial of 5: {factorial(5)}")
print(f"Factorial of 6: {factorial(6)}")
print(f"Factorial of 50: {factorial(50)}")
print(f"Factorial of 100: {factorial(100)}")

# Fibonacci calculator
def fiboniaci_iterator(n) -> list:
    if n <= 0:
        return []

    elif n == 1:
        return [0]

    else:
        sequence = [0, 1]
        while len(sequence) < n:
            next_fib = sequence[-1] + sequence[-2]
            sequence.append(next_fib)
        return sequence

amount = 10
hundred_sequence = fiboniaci_iterator(amount)
print(f"Fibonacci sequence to {amount}: {hundred_sequence}")