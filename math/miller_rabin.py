__small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
__small_test_numbers = [2, 7, 61]
__large_test_numbers = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]

# 素数判定 O(log(x))
def miller_rabin(x : int) -> bool:
    if x <= 50: return x in __small_primes
    if not x & 1: return False
    test_numbers = __small_test_numbers if x < (1 << 30) else __large_test_numbers
    d = x - 1
    while ~d & 1: d >>= 1
    for a in test_numbers:
        if x <= a: break
        t = d
        y = pow(a, t, x)
        while t != x - 1 and y != 1 and y != x - 1:
            y = y * y % x
            t <<= 1
        if y != x - 1 and not t & 1: return False
    return True