import bisect

class prime_sieve:
  # 1以上N以下の数を扱えるように初期化 O(NloglogN)
  def __init__(self, N : int):
    self.N = N
    self.primes = []
    self.min_factor = [-1] * (N + 1)
    pr = self.primes
    mf = self.min_factor
    for i in range(2, N + 1):
      if mf[i] == -1:
        pr.append(i)
        mf[i] = i
      for p in pr:
        if p * i > N or p > mf[i]:
          break
        mf[p * i] = p
  
  # xが素数か O(1)
  def is_prime(self, x : int) -> bool:
    assert 1 <= x and x <= self.N
    return self.min_factor[x] == x
  
  # k番目(0-indexed)の素数を返す. Nを超える場合は-1を返す O(1)
  def kth_prime(self, k : int) -> int:
    assert 0 <= k
    return self.primes[k] if k < len(self.primes) else -1
  
  # x以下の素数がいくつあるか O(log(x))
  def count_prime(self, x : int) -> int:
    return bisect.bisect_right(self.primes, x)
  
  # 重複なしの素因数(素因数の昇順) O(log(x))
  # prime_factor(12) -> [2, 3]
  def prime_factor(self, x : int) -> list:
    assert 1 <= x and x <= self.N
    res = []
    while x > 1:
      p = self.min_factor[x]
      res.append(p)
      while self.min_factor[x] == p:
        x //= p
    return res
  
  # 素因数分解(素因数の昇順) O(log(x))
  # factorize(12) -> [2, 2, 3]
  def factorize(self, x : int) -> list:
    assert 1 <= x and x <= self.N
    res = []
    while x > 1:
      res.append(self.min_factor[x])
      x //= self.min_factor[x]
    return res
  
  # 素因数分解(素因数の昇順) O(log(x))
  # (素因数, 個数)のリストで返す
  # factorize_compress(12) -> [(2, 2), (3, 1)]
  def factorize_compress(self, x : int) -> list:
    assert 1 <= x and x <= self.N
    res = []
    while x > 1:
      cnt = 0
      p = self.min_factor[x]
      while self.min_factor[x] == p:
        x //= p
        cnt += 1
      res.append((p, cnt))
    return res
  
  # xの約数(昇順に並んでいるとは限らない) O(xの約数の個数)
  # 約数の個数の最大値 : https://algo-method.com/descriptions/92
  def divisors(self, x : int) -> list:
    assert 1 <= x and x <= self.N
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
  
  # オイラーのφ関数 O(log(x))
  # https://en.wikipedia.org/wiki/Euler%27s_totient_function
  # φ(x) := 1以上x以下の数のうちxと互いに素なものの数
  def totient_function(self, x : int) -> int:
    assert 1 <= x and x <= self.N
    res = x
    prev = -1
    while x > 1:
      p = self.min_factor[x]
      if p > prev:
        res -= res // p
        prev = p
      x //= p
    return res
  
  # メビウス関数 O(log(x))
  # https://en.wikipedia.org/wiki/M%C3%B6bius_function
  def mobius_function(self, x : int) -> int:
    assert 1 <= x and x <= self.N
    pcnt = 0
    while x > 1:
      p = self.min_factor[x]
      y = x // p
      if p == self.min_factor[y]:
        return 0
      x = y
      pcnt += 1
    return 1 if (pcnt % 2 == 0) else -1