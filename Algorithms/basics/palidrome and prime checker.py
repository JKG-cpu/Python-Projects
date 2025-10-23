# Paledromes
def check_paledromes(word: str) -> bool:
    reversed_word = ""
    word = word.lower()

    n = len(word)
    for i in range(0, n):
        reversed_word += word[n - i - 1]

    if word == reversed_word:
        return True
    
    return False

word1 = "Racecar"
value1 = check_paledromes(word1)
msg = f"{word1} is a palendrome." if value1 else f"{word1} is not a palendrome." 
print(msg)

# Prime Checker
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors from 3 up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2

    return True

print(is_prime(2))
print(is_prime(10))