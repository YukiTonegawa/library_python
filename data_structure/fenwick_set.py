from ...bitoperation import *
from ..range_query.binary_indexed_tree import *

class fenwick_set:
    BITLEN = 64
    BITLEN_MOD = 63
    BITLEN_DIV = 6
    
    def __init__(self, n : int) -> None:
        init_popcount_table()
        init_select_table()
        self.m = max(1, (n + self.BITLEN_MOD) >> self.BITLEN_DIV)
        self.v = [0] * m
        self.bit = binary_indexed_tree(m)
    
    # 01列から構築
    def __init__(self, s : str) -> None:
        init_popcount_table()
        init_select_table()
        self.m = max(1, (len(s) + self.BITLEN_MOD) >> self.BITLEN_DIV)
        self.v = [0] * self.m
        b, j = 0, 0
        for i in range(len(s)):
            if s[i] == '1':
                self.v[b] += 1 << j
            if j == self.BITLEN_MOD:
                b += 1
                j = 0
            else:
                j += 1
        pop = [0] * self.m
        for i in range(self.m):
            pop[i] = popcount64(self.v[i])
        self.bit = binary_indexed_tree(pop)

    # k番目の要素をf(0/1)にする
    def set(self, k : int, f : bool) -> None:
        b, j = (k >> self.BITLEN_DIV), k & self.BITLEN_MOD
        g = (self.v[b] >> j) & 1
        if f == g:
            return
        self.v[b] ^= 1 << j
        if f:
            self.bit.update(b, 1)
        else:
            self.bit.update(b, -1)
    
    def get(self, k : int) -> bool:
        b, j = (k >> self.BITLEN_DIV), k & self.BITLEN_MOD
        return (self.v[b] >> j) & 1
    
    # [0, r)の1の数
    def rank1(self, r : int) -> int:
        b, j = (r >> self.BITLEN_DIV), r & self.BITLEN_MOD
        popsmall = popcount64(self.v[b] & ((1 << j) - 1)) if j else 0
        return self.bit.query_r(b) + popsmall

    # [0, r)の0の数
    def rank0(self, r : int) -> int:
        return r - self.rank1(r)
    
    # k番目の1 ない場合は-1
    def select1(self, k : int) -> int:
        b, s = self.bit.lower_bound(k + 1)
        if b == self.m:
            return -1
        rem = k - s + popcount64(self.v[b])
        return (b << self.BITLEN_DIV) + select64(self.v[b], rem)

    #def select0(self, k : int) -> int:


    """
    # k以降で初めて現れる要素(kも含む) ない場合は-1
    def next1(self, k : int) -> int:
        i = k & BITLEN_MOD
        j = next64(self.v[k >> self.BITLEN_DIV], i)
        if j != -1:
            return k - i + j
        return self.select1(self.rank1(k))
    """
        