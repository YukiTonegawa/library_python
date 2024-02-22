class interval_heap:
    # サイズnのリストをサイズkに拡張
    def __extend(self, k):
        assert self.n < k
        self.v.extend([0] * (k - self.n))

    def __parent(self, k):
        return ((k >> 1) - 1) & ~1

    def __down(self, k):
        if k & 1:
            while 2 * k + 1 < self.n:
                c = 2 * k + 3
                if self.n <= c or self.v[c - 2] < self.v[c]:
                    c -= 2
                if c < self.n and self.v[c] < self.v[k]:
                    self.v[k], self.v[c] = self.v[c], self.v[k]
                    k = c
                else:
                    break
        else:
            while 2 * k + 2 < self.n:
                c = 2 * k + 4
                if self.n <= c or self.v[c] < self.v[c - 2]:
                    c -= 2
                if c < self.n and self.v[k] < self.v[c]:
                    self.v[k], self.v[c] = self.v[c], self.v[k]
                    k = c
                else:
                    break
        return k

    def __up(self, k, root = 1):
        if ((k | 1) < self.n) and (self.v[k & ~1] < self.v[k | 1]):
            self.v[k & ~1], self.v[k | 1] = self.v[k | 1], self.v[k & ~1]
            k ^= 1
        while root < k and self.v[p := self.__parent(k)] < self.v[k]:
            self.v[p], self.v[k] = self.v[k], self.v[p]
            k = p
        while root < k and self.v[k] < self.v[p := self.__parent(k) | 1]:
            self.v[p], self.v[k] = self.v[k], self.v[p]
            k = p
        return k

    def __init__(self):
        self.n = 0
        self.v = []

    # サイズ
    def size(self):
        return self.n

    # 空か
    def empty(self):
        return self.n == 0

    # 配列から構築
    def make_heap(self, v):
        self.n = len(v)
        self.v = v
        for i in reversed(range(self.n)):
            if (i & 1) and self.v[i - 1] < self.v[i]:
                self.v[i - 1], self.v[i] = self.v[i], self.v[i - 1]
            k = self.__down(i)
            self.__up(k, i)

    # xを追加
    def push(self, x):
        if self.n == len(self.v):
            self.__extend(max(4, self.n << 1))
        self.v[self.n] = x
        self.n += 1
        self.__up(self.n - 1)

    # 最小値, ない場合はNone
    def min(self):
        if self.n == 0:
            return None
        return self.v[0] if self.n < 2 else self.v[1];

    # 最大値, ない場合はNone
    def max(self):
        if self.n == 0:
            return None
        return self.v[0]

    # 最小値をpopして返す, ない場合はNone
    def pop_min(self):
        if self.n == 0:
            return None
        min_val = self.min()
        self.n -= 1
        if self.n > 1:
            self.v[1], self.v[self.n] = self.v[self.n], self.v[1]
            k = self.__down(1)
            self.__up(k)
        return min_val

    # 最大値をpopして返す, ない場合はNone
    def pop_max(self):
        if self.n == 0:
            return None
        max_val = self.max()
        self.n -= 1
        if self.n > 0:
            self.v[0], self.v[self.n] = self.v[self.n], self.v[0]
            k = self.__down(0)
            self.__up(k)
        return max_val