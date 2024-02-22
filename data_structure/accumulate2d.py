class accumulate2d:
    def __build(self, v : list) -> None:
        self.n = len(v)
        self.m = len(v[0]) if self.n else 0
        self.sum = [[self.e for _ in range(self.m + 1)] for __ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                self.sum[i][j] = self.op(self.sum[i][j - 1], v[i - 1][j - 1])
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                self.sum[i][j] = self.op(self.sum[i][j], self.sum[i - 1][j])
        
    def __init__(self, commutative_group, v : list) -> None:
        self.sum = v
        self.op = commutative_group.merge
        self.e = commutative_group.id()
        self.inv = commutative_group.inv
        self.__build(v)
    
    def __init__(self, v : list) -> None:
        self.sum = v
        self.op = lambda x, y : x + y
        self.e = 0
        self.inv = lambda x : -x
        self.__build(v)
    
    # [lx, rx) × [ly, ry)の和, 範囲外は全て単位元とする
    def query(self, lx : int, rx : int, ly : int, ry : int):
        lx, rx = max(lx, 0), min(rx, self.n)
        ly, ry = max(ly, 0), min(ry, self.m)
        if lx >= rx or ly >= ry: return self.e
        upper = self.op(self.sum[lx][ly], self.inv(self.sum[lx][ry]))
        lower = self.op(self.sum[rx][ry], self.inv(self.sum[rx][ly]))
        return self.op(lower, upper)