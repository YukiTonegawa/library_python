import heapq

class min_heap:
    def __init__(self):
      self.v = []

    # サイズ
    def size(self):
        return len(self.v)

    # 空か
    def empty(self):
        return len(self.v) == 0

    # 配列から構築
    def make_heap(self, v):
        self.v = v
        heapq.heapify(self.v)

    # xを追加
    def push(self, x):
        heapq.heappush(self.v, x)

    # 最小値, ない場合はNone
    def min(self):
        if self.empty():
            return None
        return self.v[0]

    # 最小値をpopして返す, ない場合はNone
    def pop_min(self):
        if self.empty():
            return None
        return heapq.heappop(self.v)

class max_heap:
    def __rotate_down(self, k):
        v = self.v
        while True:
            l = k * 2 + 1
            r = l + 1
            if l >= len(v):
                break
            if r >= len(v):
                if v[k] < v[l]:
                    v[k], v[l] = v[l], v[k]
                    k = l
                else:
                    break
            elif v[k] < max(v[l], v[r]):
                if v[l] > v[r]:
                    v[k], v[l] = v[l], v[k]
                    k = l
                else:
                    v[k], v[r] = v[r], v[k]
                    k = r
            else:
                break
    
    def __rotate_up(self, k):
        v = self.v
        while k:
            k = (k - 1) // 2
            l = k * 2 + 1
            r = l + 1
            if r >= len(v):
                if v[k] < v[l]:
                    v[k], v[l] = v[l], v[k]
                else:
                    break
            else:
                if v[k] < max(v[l], v[r]):
                  if v[l] > v[r]:
                      v[k], v[l] = v[l], v[k]
                  else:
                      v[k], v[r] = v[r], v[k]
                else:
                    break
    
    def __init__(self):
      self.v = []

    # サイズ
    def size(self):
        return len(self.v)

    # 空か
    def empty(self):
        return len(self.v) == 0

    # 配列から構築
    def make_heap(self, v):
        self.v = v
        for i in reversed(range(0, (len(v) - 1) // 2 + 1)):
            self.__rotate_down(i)

    # xを追加
    def push(self, x):
        self.v.append(x)
        self.__rotate_up(len(self.v) - 1)

    # 最大値, ない場合はNone
    def max(self):
        if self.empty():
            return None
        return self.v[0]

    # 最大値をpopして返す, ない場合はNone
    def pop_max(self):
        if self.empty():
            return None
        v = self.v
        ans = v[0]
        if len(v) == 1:
            v.pop()
        else:
          v[0] = v[len(v) - 1]
          v.pop()
          self.__rotate_down(0)
        return ans
