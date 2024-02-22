import math
from pylib.math.miller_rabin import *
from random import randrange

class rho_factorization:
  # nの1, n以外の約数を探す O(n^(1/4))
  # nが素数の場合はnを返す
  def find_divisor(self, n : int) -> int:
    if n == 1: return 1
    for s in (2, 3, 5): 
      if n % s == 0: return s
    if miller_rabin(n): return n

    m = int(n ** 0.125) + 1
    res = n
    def __try():
      c = randrange(1, n)
      f = lambda a : (a * a + c) % n
      y, r, q, g, x, k, ys = n, 1, 1, 1, 1, 1, 1
      while g == 1:
        x = y
        for _ in range(r): y = f(y)
        k = 0
        while k < r and g == 1:
          ys = y
          for _ in range(min(m, r - k)):
            y = f(y)
            q = q * abs(x - y) % n
          g = math.gcd(q, n)
          k += m
        r <<= 1
      if g == n:
        g = 1
        while g == 1:
          ys = f(ys)
          g = math.gcd(n, abs(x - ys))
      return g
    
    res = n
    while res == n: res = __try() 
    return res
  
  # xが素数か O(log(x))
  def is_prime(self, x : int) -> bool:
    return miller_rabin(x)
  
  # 重複なしの素因数(素因数の昇順) O(x^(1/4))
  # prime_factor(12) -> [2, 3]
  def prime_factor(self, x : int) -> list:
    P = self.factorize(x)
    res = []
    for p in P:
      if len(res) == 0 or res[-1] != p:
        res.append(p)
    return res
  
  # 素因数分解(素因数の昇順) O(x^(1/4))
  # factorize(12) -> [2, 2, 3]
  def factorize(self, x : int) -> list:
    if x == 1: return []
    res = [x]
    i = 0
    while i < len(res):
      y = self.find_divisor(res[i])
      if res[i] == y:
        i += 1
      else:
        res[i] //= y
        res.append(y)
    res.sort()
    return res

  # 素因数分解(素因数の昇順) O(x^(1/4))
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
  
  # オイラーのφ関数 O(x^(1/4))
  # https://en.wikipedia.org/wiki/Euler%27s_totient_function
  # φ(x) := 1以上x以下の数のうちxと互いに素なものの数
  def totient_function(self, x : int) -> int:
    res = x
    for p in self.prime_factor(x):
      res -= res // p
    return res
  
  # メビウス関数 O(x^(1/4))
  # https://en.wikipedia.org/wiki/M%C3%B6bius_function
  def mobius_function(self, x : int) -> int:
    P = self.factorize(x)
    m = len(P)
    for i in range(m - 1):
      if P[i] == P[i + 1]:
        return 0
    return 1 if (m % 2 == 0) else -1
  

  