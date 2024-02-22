class binary_indexed_tree:
    def __init__(self)->None:
        self.n = 0
        self.h = 0
    
    # n要素の0
    def __init__(self, n : int) -> None:
        self.n = n
        self.h = 0
        while (1 << self.h) < self.n: self.h += 1
        self.sum = [0] * (self.n + 1)
    """"
    # リストから構築
    def __init__(self, v : list) -> None:
        self.n = len(v)
        self.h = 0
        while (1 << self.h) < self.n: self.h += 1
        self.sum = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.sum[i] += v[i - 1]
            nxt = i + (i & (-i))
            if nxt <= self.n:
                self.sum[nxt] += self.sum[i]
    """

    # sum[k] += x
    def update(self, k : int, x : int) -> None:
        k += 1
        while k <= self.n:
            self.sum[k] += x
            k += (k & (-k))
    
    # sum[0, r)
    def query_r(self, r : int) -> int:
        res = 0
        while r > 0:
            res += self.sum[r]
            r -= (r & (-r))
        return res
    
    # sum[l, r)
    def query(self, l : int, r : int) -> int:
        return self.query_r(r) - self.query_r(l)
    
    # sum[0, k]がx以上になる最小のkとsum[0, k]
    # ない場合は(self.n, 全体の総和)
    # 全要素非負でなければならない
    def lower_bound(self, x : int) -> tuple:
        v, h = (1 << self.h), self.h
        s, t = 0, 0
        while h:
            h -= 1
            if self.n < v:
                v -= 1 << h
            elif x <= s + self.sum[v]:
                t = s + self.sum[v]
                v -= 1 << h
            else:
                s += self.sum[v]
                v += 1 << h
        
        if v == self.n + 1:
            return (self.n, s)
        s += self.sum[v]
        return (v - 1, s) if x <= s else (v, t)
    
    # fは(k, sum[0, k])に対してbool値を返す関数
    # kに対してfが単調(False -> True)のとき, 初めてTrueとなる(k, sum[0, k])を返す
    # ない場合は(self.n, 全体の総和)
    def lower_bound_abst(self, x : int, f : callable) -> tuple:
        v, h = (1 << self.h), self.h
        s, t = 0, 0
        while h:
            h -= 1
            if self.n < v:
                v -= 1 << h
            elif f(v - 1, s + self.sum[v]):
                t = s + self.sum[v]
                v -= 1 << h
            else:
                s += self.sum[v]
                v += 1 << h
        
        if v == self.n + 1:
            return (self.n, s)
        s += self.sum[v]
        return (v - 1, s) if f(v - 1, s) else (v, t)