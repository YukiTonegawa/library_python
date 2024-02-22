
from array import array
class bitvector:
    __block_len = 16
    __block_len_shift = 4
    __block_len_mod = 15
    
    def __init__(self, v : list):
        init_popcount_table()
        self.n = len(v)
        self.B = array('I', [0])
        self.S = array('I')
        pop, s, t = 0, 0, 0
        for i in range(self.n):
            if v[i]:
                pop += 1
                s += 1 << t
            if t == self.__block_len - 1 or i == self.n - 1:
                self.B.append(pop)
                self.S.append(s)
                t, s = 0, 0
            else:
                t += 1
        self.S.append(0)
    
    def rank1(self, r : int) -> int:
        a, b = r >> self.__block_len_shift, r & self.__block_len_mod
        return self.B[a] + popcount_table[self.S[a] & ((1 << b) - 1)]

    def rank0(self, r : int) -> int:
        a, b = r >> self.__block_len_shift, r & self.__block_len_mod
        return r - (self.B[a] + popcount_table[self.S[a] & ((1 << b) - 1)])
    
from collections import deque
class wavelet_matrix:
    def __build(self, v : list):
        n, h = self.n, self.h
        self.bv = [0] * self.h
        self.bottom_idx = array('I', [i for i in range(n)])
        tmp_idx = array('I', [0] * n)
        tmp = array('I', [0] * n)
        bits = array('I', [0] * n)
        q = deque()
        if h: q.append((h - 1, 0, n))

        
        while q:
            d, l, r = q.popleft()
            lcnt, rcnt = 0, 0
            for i in range(l, r):
                bits[i] = (v[i] >> d) & 1
                if bits[i]:
                    tmp[rcnt] = v[i]
                    tmp_idx[rcnt] = self.bottom_idx[i]
                    rcnt += 1
                else:
                    v[l + lcnt] = v[i]
                    self.bottom_idx[l + lcnt] = self.bottom_idx[i]
                    lcnt += 1
            for i in range(rcnt):
                v[l + lcnt + i] = tmp[i]
                self.bottom_idx[l + lcnt + i] = tmp_idx[i]
            if d:
                mid = l + lcnt
                if l < mid: q.append((d - 1, l, mid))
                if mid < r: q.append((d - 1, mid, r))
            if r == n: self.bv[d] = bitvector(bits)
    
    def __init__(self, v : list):
        self.n = len(v)
        self.inf = max(v) + 1 if v else 0
        min_elem = min(v) if v else 0
        assert min_elem >= 0, "負の値, 大きい値を扱う場合は座圧バージョンを使う"
        self.h = 0
        while (1 << self.h) < self.inf: self.h += 1
        self.__build(v)
    
    # r未満のcの数
    def rank(self, r : int, c : int) -> int:
        L, R = 0, self.n
        for d in reversed(range(self.h)):
            L0 = self.bv[d].rank0(L)
            R0 = self.bv[d].rank0(R) - L0
            r0 = self.bv[d].rank0(r) - L0
            if (c >> d) & 1:
                r += R0 - r0
                L += R0
            else:
                r -= (r - L) - r0
                R = L + R0
            if r == L: return 0
        return r - L
    
    # [l, r)のcの数
    def rank(self, l : int, r : int, c : int) -> int:
        L, R = 0, self.n
        for d in reversed(range(self.h)):
            continue
            #L0 = self.bv[d].rank0(L)
            #R0 = self.bv[d].rank0(R) - L0
            #l0 = self.bv[d].rank0(l) - L0
            #r0 = self.bv[d].rank0(r) - L0
            #if (c >> d) & 1:
                #l += R0 - l0
                #r += R0 - r0
                #L += R0
            #else:
                #l -= (l - L) - l0
                #r -= (r - L) - r0
                #R = L + R0
            #if r == l: return 0
        return r - l
