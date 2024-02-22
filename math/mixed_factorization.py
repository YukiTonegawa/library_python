import prime_sieve
import miller_rabin
import rho_factorization

# 閾値N以下なら篩, それより大きいならrho法で素因数分解
class mixed_factorization:
  def __init__(self, N):
    self.N = N
    self.low = prime_sieve(N)
    self.high = rho_factorization()
  
  # xが素数か O(1) ~ O(log(x))
  def is_prime(self, x : int) -> bool:
    if x <= self.N:
      return self.low.is_prime(x)
    return miller_rabin(x)
  
  # 重複なしの素因数(素因数の昇順) O(log(x)) ~ O(x^(1/4)log(x))
  # prime_factor(12) -> [2, 3]
  def prime_factor(self, x : int) -> list:
    P = self.factorize(x)
    res = []
    for p in P:
      if len(res) == 0 or res[-1] != p:
        res.append(p)
    return res
  
  # 素因数分解(素因数の昇順) O(log(x)) ~ O(x^(1/4)log(x))
  # factorize(12) -> [2, 2, 3]
  def factorize(self, x : int) -> list:
    if x == 1: return []
    res = [x]
    i = 0
    while i < len(res):
      y = self.high.find_divisor(res[i]) if res[i] > self.N else self.low.min_factor[res[i]]
      if res[i] == y:
        i += 1
      else:
        res[i] //= y
        res.append(y)
    res.sort()
    return res
  
  # 素因数分解(素因数の昇順) O(log(x)) ~ O(x^(1/4)log(x))
  # (素因数, 個数)のリストで返す
  # factorize_compress(12) -> [(2, 2), (3, 1)]
  def factorize_compress(self, x : int) -> list:
    P = self.factorize(x)
    res = []
    tmp_p, cnt = -1, 0
    for p in P:
      if p == tmp_p:
        cnt += 1
      else:
        if tmp_p != -1:
          res.append((tmp_p, cnt))
        tmp_p, cnt = p, 1
    if tmp_p != -1:
      res.append((tmp_p, cnt))
    return res
  
  # xの約数(昇順に並んでいるとは限らない) O(xの約数の個数)
  # 約数の個数の最大値 : https://algo-method.com/descriptions/92
  def divisors(self, x : int) -> list:
    P = self.factorize_compress(x)
    m = len(p)
    l, r = 0, 1
    res = [1]
    for i in range(m):
      p, cnt = P[i]
      ppow = 1
      for _ in cnt + 1:
        for j in range(l, r):
          res.append(res[j] * ppow)
        ppow *= p
      l, r = r, len(res)
    return res[l :]
  
 # オイラーのφ関数 O(log(x)) ~ O(x^(1/4)log(x))
  # https://en.wikipedia.org/wiki/Euler%27s_totient_function
  # φ(x) := 1以上x以下の数のうちxと互いに素なものの数
  def totient_function(self, x : int) -> int:
    res = x
    for p in self.prime_factor(x):
      res -= res // p
    return res
  
  # メビウス関数 O(log(x)) ~ O(x^(1/4)log(x))
  # https://en.wikipedia.org/wiki/M%C3%B6bius_function
  def mobius_function(self, x : int) -> int:
    P = self.factorize(x)
    m = len(P)
    for i in range(m - 1):
      if P[i] == P[i + 1]:
        return 0
    return 1 if (m % 2 == 0) else -1
