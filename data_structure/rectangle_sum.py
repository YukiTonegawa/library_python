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

from bisect import bisect_left

# list(tuple)のソート
# @param keyidxの型が整数型
def tuple_sort(v : list, keyidx : int):
    N = len(v)
    tmp = [(v[i][keyidx] << 30) + i for i in range(N)]
    tmp.sort()
    __mask30 = (1 << 30) - 1
    return [v[tmp[i] & __mask30] for i in range(N)]

class offline_static_rectangle_sum:
    def __init__(self):
        self.built = False
        self.P = []
        self.Q = []
    
    # (x, y)に重みzを足す
    def update(self, x, y, z) -> None:
        assert not self.built
        self.P.append((x, y, z))
    
    # [lx, rx) × [ly, ry)の和
    def query(self, lx, rx, ly, ry) -> None:
        assert not self.built
        self.Q.append((lx, rx, ly, ry))
    
    def solve(self) -> list:
        assert not self.built
        self.built = True
        
        # compress y
        self.P = tuple_sort(self.P, 1)
        Y = []
        for i in range(len(self.P)):
            x, y, z = self.P[i]
            if len(Y) == 0 or Y[-1] != y:
                Y.append(y)
            self.P[i] = (x, len(Y) - 1, z)
        
        E = []
        N = len(self.Q)
        for i in range(N):
            lx, rx, ly, ry = self.Q[i]
            ly2 = bisect_left(Y, ly)
            ry2 = bisect_left(Y, ry)
            E.append((lx, ly2, ry2, i))
            E.append((rx, ly2, ry2, i + N))
        
        # sort by x
        self.P = tuple_sort(self.P, 0)
        E = tuple_sort(E, 0)
        
        res = [0] * N
        bit = binary_indexed_tree(len(Y))
        pidx, qidx = 0, 0
        while qidx < 2 * N:
            if pidx == len(self.P) or E[qidx][0] <= self.P[pidx][0]:
                x, ly, ry, i = E[qidx]
                S = bit.query(ly, ry)
                if i < N:
                    res[i] -= S
                else:
                    res[i - N] += S
                qidx += 1
            else:
                bit.update(self.P[pidx][1], self.P[pidx][2])
                pidx += 1
        return res

class offline_point_add_rectangle_sum:
    def __init__(self):
        self.built = False
        self.Q = []
        self.qcnt = [0]
    
    # (x, y)に重みzを足す
    def update(self, x, y, z) -> None:
        assert not self.built
        self.Q.append((-1, x, y, z))
        self.qcnt.append(self.qcnt[-1])
    
    # [lx, rx) × [ly, ry)の和
    def query(self, lx, rx, ly, ry) -> None:
        assert not self.built
        self.Q.append((self.qcnt[-1], lx, rx, ly, ry))
        self.qcnt.append(self.qcnt[-1] + 1)
    
    def solve(self) -> list:
        assert not self.built
        self.built = True
        res = [0] * self.qcnt[-1]
        st = [(0, len(self.Q))]
        while st:
            L, R = st[-1]
            st.pop()
            if R - L < 2:
                continue
            M = (L + R) // 2
            st.append((L, M))
            st.append((M, R))
            
            left_update = (M - L) - (self.qcnt[M] - self.qcnt[L])
            right_query = self.qcnt[R] - self.qcnt[M]

            if left_update * right_query < 200:
                A = []
                for i in range(L, M):
                    if self.Q[i][0] == -1:
                        A.append(self.Q[i])
                for i in range(M, R):
                    if self.Q[i][0] != -1:
                        j, lx, rx, ly, ry = self.Q[i]
                        for _, x, y, z in A:
                            if lx <= x < rx and ly <= y < ry:
                                res[j] += z
                continue

            Y = []
            A = []
            for i in range(L, M):
                if self.Q[i][0] == -1:
                    Y.append(self.Q[i][2])
                    A.append(self.Q[i])

            Y.sort()
            for i in range(left_update):
                _, x, y, z = A[i]
                A[i] = (x, bisect_left(Y, y), z)

            B = []
            for i in range(M, R):
                if self.Q[i][0] != -1:
                    j, lx, rx, ly, ry = self.Q[i]
                    ly2 = bisect_left(Y, ly)
                    ry2 = bisect_left(Y, ry)
                    B.append((j, lx, ly2, ry2))
                    B.append((j + self.qcnt[-1], rx, ly2, ry2))
            
            A = tuple_sort(A, 0)
            B = tuple_sort(B, 1)

            bit = binary_indexed_tree(len(Y))
            aidx, bidx = 0, 0
            while bidx < len(B):
                if aidx == len(A) or B[bidx][1] <= A[aidx][0]:
                    i, x, ly, ry = B[bidx]
                    S = bit.query(ly, ry)
                    if i < self.qcnt[-1]:
                        res[i] -= S
                    else:
                        res[i - self.qcnt[-1]] += S
                    bidx += 1
                else:
                    x, y, z = A[aidx]
                    bit.update(y, z)
                    aidx += 1

        return res


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

io_init()
n, q = read_line(int)

rect = offline_point_add_rectangle_sum()
for i in range(n):
    x, y, z = read_line(int)
    rect.update(x, y, z)

for i in range(q):
    t = list(map(int, input().split()))
    if t[0] == 0:
        rect.update(t[1], t[2], t[3])
    else:
        rect.query(t[1], t[3], t[2], t[4])

print(*rect.solve())
