import sys

def io_init() -> None:
    global input
    input = sys.stdin.readline

# make_list(2, 3, 4) -> [[4, 4, 4], [4, 4, 4]]
def make_list(arg1 : int, arg2, *arg3) -> list:
    if len(arg3) == 0:
        return [arg2] * arg1
    else:
        return [make_list(arg2, arg3[0], *(arg3[1 :])) for _ in range(arg1)]

# read_list(2, 3, int) -> 2 × 3のintのリストを入力
def read_list(arg1 : int, arg2, *arg3) -> list:
    if len(arg3) == 0:
        return list(map(arg2, input().split()))
    else:
        return [read_list(arg2, arg3[0], *(arg3[1 :])) for _ in range(arg1)]

# 1行入力, 空白で分割してarg1をmap
def read_line(arg1) -> list:
    return map(arg1, input().split())

# 文字列を入力して文字ごとに分割
def read_str() -> list:
    return list(map(chr, list(input())[: -1]))



__MOD = 998244353
__I = []
__F = []
__FI = []
def make_table1(n : int) -> None:
    # 0 ≡ (p // i) * i + (p % i) (mod p)
    # ->
    # inv[i] ≡ -inv[p % i] * (p // i) (mod p)
    global __I, __F, __FI
    n = min(n + 1, __MOD)
    I, F, FI = [0] * n, [0] * n, [0] * n
    I[0], I[1] = 0, 1
    F[0], F[1] = 1, 1
    FI[0], FI[1] = 1, 1
    for i in range(2, n):
        I[i] = (__MOD - I[__MOD % i]) * (__MOD // i) % __MOD
        F[i] = F[i - 1] * i % __MOD
        FI[i] = FI[i - 1] * I[i] % __MOD
    __I, __F, __FI = I, F, FI
    

def make_table2(n : int) -> None:
    # inv[i] = finv[i] * fac[i - 1]
    global __I, __F, __FI
    n = min(n + 1, __MOD)
    I, F, FI = [0] * n, [0] * n, [0] * n
    I[0], I[1] = 0, 1
    F[0], F[1] = 1, 1
    FI[0], FI[1] = 1, 1
    for i in range(2, n):
        F[i] = F[i - 1] * i % __MOD
    FI[n - 1] = pow(F[n - 1], __MOD - 2, __MOD)
    for i in reversed(range(2, n)):
        I[i] = F[i - 1] * FI[i] % __MOD
        FI[i - 1] = FI[i] * i % __MOD
    __I, __F, __FI = I, F, FI
    
# nCk mod
def comb(n : int, k : int) -> int:
    if n < 0 or k < 0 or n < k:
        return 0
    return __F[n] * __FI[n - k] % __MOD * __FI[k] % __MOD

# inv(nCk) mod
def combinv(n : int, k : int) -> int:
    return __FI[n] * __F[n - k] % __MOD * __F[k] % __MOD

# nPk mod
def perm(n : int, k : int) -> int:
    if n < 0 or k < 0 or n < k:
        return 0
    return __F[n] * __FI[n - k] % __MOD

# inv(nPk) mod
def perminv(n : int, k : int) -> int:
    return __FI[n] * __F[n - k] % __MOD

# inv(x)
def inv(x : int) -> int:
    return __I[x]

# x! mod
def fac(x : int) -> int:
    return __F[x]

# inv(x!) mod
def finv(x : int) -> int:
    return __FI[x]


io_init()

t, m = read_line(int)
__MOD = m
#make_table1(10000000)

for _ in range(t):
    n, k = read_line(int)
    #print(comb(n, k))
