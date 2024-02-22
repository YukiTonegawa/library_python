class accumulate1d:
    def __init__(self, commutative_group, v : list) -> None:
        self.sum = v
        self.op = commutative_group.merge
        self.e = commutative_group.id()
        self.inv = commutative_group.inv
        for i in range(1, len(v)):
            self.sum[i] = self.op(self.sum[i - 1], v[i])
    
    def __init__(self, v : list) -> None:
        self.sum = v
        self.op = lambda x, y : x + y
        self.e = 0
        self.inv = lambda x : -x
        for i in range(1, len(v)):
            self.sum[i] = self.op(self.sum[i - 1], v[i])
    
    # [0, r)の和, 範囲外の部分は全て単位元
    def query(self, r : int):
        r = min(r, len(self.sum))
        if r <= 0: return self.e
        return self.sum[r - 1]
    
    # [l, r)の和, 範囲外の部分は全て単位元
    def query(self, l : int, r : int):
        l, r = max(l, 0), min(r, len(self.sum))
        if r <= l: return self.e
        if l == 0: return self.sum[r - 1]
        return self.op(self.sum[r - 1], self.inv(self.sum[l - 1]))

