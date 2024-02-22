from bisect import bisect_left, bisect_right, insort

class multiset_avl:
    LIMIT_SIZE_PER_NODE = 1000

    class node:
        def __init__(self, v = []):
            self.h = 0
            self.nums = v
            self.size = len(v)
            self.l = None
            self.r = None

        def balanace_factor(self):
            lh = self.l.h if self.l else 0
            rh = self.r.h if self.r else 0
            return lh - rh

        def update(self):
            self.h = max(self.l.h if self.l else 0, self.r.h if self.r else 0) + 1
            self.size = len(self.nums) + (self.l.size if self.l else 0) + (self.r.size if self.r else 0)

        def rotate_right(self):
            l = self.l
            self.l = l.r
            l.r = self
            self.update()
            l.update()
            return l

        def rotate_left(self):
            r = self.r
            self.r = r.l
            r.l = self
            self.update()
            r.update()
            return r

        def balance(self):
            bf = self.balanace_factor()
            assert -2 <= bf and bf <= 2
            if bf == 2:
                if self.l.balanace_factor() == -1:
                    self.l = self.l.rotate_left()
                    self.update()
                return self.rotate_right()
            elif bf == -2:
                if self.r.balanace_factor() == 1:
                    self.r = self.r.rotate_right()
                    self.update()
                return self.rotate_left()
            return self

        def split_half(self, LIMIT_SIZE_PER_NODE):
            assert len(self.nums) == LIMIT_SIZE_PER_NODE
            r_elem = self.nums[LIMIT_SIZE_PER_NODE // 2 : LIMIT_SIZE_PER_NODE]
            self.nums = self.nums[0 : LIMIT_SIZE_PER_NODE // 2]
            self.size = len(self.nums)
            return r_elem

    def __calc_height(self, x, INIT_SIZE):
        y = 1
        res = 0
        while True:
            if (y - 1) * INIT_SIZE >= x:
                return res
            y <<= 1
            res += 1

    def __build(self, n, v, INIT_SIZE):
        st = [(0, n, None, 0)]
        while len(st):
            l, r, p, dir = st.pop()
            d = (r - l + INIT_SIZE - 1) // INIT_SIZE
            l2 = l + INIT_SIZE * (d // 2)
            r2 = min(l2 + INIT_SIZE, r)
            u = self.node(v[l2 : r2])
            u.size = r - l
            u.h = self.__calc_height(r - l, INIT_SIZE)
            if p and dir == 0:
                p.l = u
            elif p and dir == 1:
                p.r = u
            else:
                self.root = u

            if l < l2:
                st.append((l, l2, u, 0))
            if r2 < r:
                st.append((r2, r, u, 1))
    
     # ノードvの最も左の位置にノードuを追加
    def __insert_leftmost(self, v, u):
        if v == None:
            return u
        st = []
        while True:
            st.append(v)
            if v.l:
                v = v.l
            else:
                v.l = u
                break
        while len(st):
            v = st.pop()
            v.update()
            v = v.balance()
            if len(st):
                st[-1].l = v
        return v

    TEMPORARY_NODE = None
    # vの最も左のノードを切り取ってTEMPORARY_NODEに代入する
    def __cut_leftmost(self, v):
        st = []
        while True:
            if v.l:
                st.append(v)
                v = v.l
            else:
                self.TEMPORARY_NODE = v
                st.append(v.r)
                break
        while len(st):
            v = st.pop()
            if v:
                v.update()
                v = v.balance()
            if len(st):
                st[-1].l = v
        return v
    
    def __debug(self, v):
        if v.l:
            self.__debug(v.l)
        print(v.nums)
        if v.r:
            self.__debug(v.r)

    def __init__(self, v = []):
        assert self.LIMIT_SIZE_PER_NODE >= 2
        self.root = self.node([])
    
    # ソート済かつユニークな配列で初期化
    def build(self, V):
        if len(V):
            self.__build(len(V), V, self.LIMIT_SIZE_PER_NODE // 2)
        else:
            self.root = self.node([])

    # 要素数　
    def size(self):
        return self.root.size
    
    # xがあるか(bool)
    def find(self, x):
        v = self.root
        if v.size == 0:
            return False
        while v:
            if x < v.nums[0]:
                v = v.l
            elif x > v.nums[-1]:
                v = v.r
            else:
                # set
                idx = bisect_left(v.nums, x)
                return v.nums[idx] == x
        return False
    
    # xの数
    def count(self, x):
        return self.le_count(x) - self.l_count(x)

    # xを追加
    def insert(self, x):
        v = self.root
        # 空の場合
        if v.size == 0:
            v.nums.append(x)
            v.size = 1
            return
        st = []
        while v:
            if v.l and x < v.nums[0]:
                st.append((v, 0))
                v = v.l
            elif v.r and x > v.nums[-1]:
                st.append((v, 1))
                v = v.r
            else:
                insort(v.nums, x)
                v.size += 1
                if len(v.nums) == self.LIMIT_SIZE_PER_NODE:
                    u = self.node(v.split_half(self.LIMIT_SIZE_PER_NODE))
                    v.r = self.__insert_leftmost(v.r, u)
                    st.append((v, -1))
                    while len(st):
                        v, d = st.pop()
                        v.update()
                        v = v.balance()
                        if len(st):
                            if st[-1][1] == 0:
                                st[-1][0].l = v
                            else:
                                st[-1][0].r = v
                        else:
                            self.root = v
                else:
                    while len(st):
                        v, d = st.pop()
                        v.update()

                return

    # xを1個削除してTrueを返す(ない場合は何もせずFalseを返す)
    def erase(self, x):
        size_after = self.root.size - 1
        v = self.root
        if v.size == 0:
            return False
        st = []
        while v:
            if x < v.nums[0]:
                st.append((v, 0))
                v = v.l
            elif x > v.nums[-1]:
                st.append((v, 1))
                v = v.r
            else:
                idx = bisect_left(v.nums, x)
                if v.nums[idx] != x:
                    return False

                del v.nums[idx]
                v.size -= 1
                if len(v.nums) == 0 and size_after > 0: # 根だけの場合はノードを消さない
                    if v.r:
                        v.r = self.__cut_leftmost(v.r)
                        self.TEMPORARY_NODE.l = v.l
                        self.TEMPORARY_NODE.r = v.r
                        st.append((self.TEMPORARY_NODE, -1))
                    else:
                        st.append((v.l, -1))

                    while len(st):
                        v, d = st.pop()
                        if v:
                            v.update()
                            v = v.balance()
                        if len(st):
                            if st[-1][1] == 0:
                                st[-1][0].l = v
                            else:
                                st[-1][0].r = v
                        else:
                            self.root = v
                else:
                    while len(st):
                        v, d = st.pop()
                        v.update()
                return True

    # 全要素出力
    def debug(self):
        self.__debug(self.root)

    # 最小要素, ない場合はNone
    def min(self):
        v = self.root
        if v.size == 0:
            return None
        while v.l:
            v = v.l
        return v.nums[0]
    
    # 最大要素, ない場合はNone
    def max(self):
        v = self.root
        if v.size == 0:
            return None
        ans = -1
        while v.r:
            v = v.r
        return v.nums[-1]
    
    # k番目に小さい要素(minは0), ない場合はNone
    def kth_smallest(self, k):
        v = self.root
        if v.size <= k:
            return None  
        while v:
            lsz = v.l.size if v.l else 0
            if k < lsz:
                v = v.l
            elif lsz + v.size <= k:
                k -= lsz + v.size
                v = v.r
            else:
                return v.nums[k - lsz]
    
    # k番目に大きい要素(maxは0), ない場合はNone
    def kth_largest(self, k):
        v = self.root
        if v.size <= k:
            return None  
        while v:
            rsz = v.r.size if v.r else 0
            if k < rsz:
                v = v.r
            elif rsz + v.size <= k:
                k -= rsz + v.size
                v = v.l
            else:
                return v.nums[v.size - 1 - (k - rsz)]
    
    # x以下の最大要素, 無い場合はNone
    def le(self, x):
        v = self.root
        if v.size == 0:
            return None
        ans = x
        while v:
            if x < v.nums[0]:
                v = v.l
            elif x > v.nums[-1]:
                if ans == x:
                    ans = v.nums[-1]
                else:
                    ans = max(ans, v.nums[-1])
                v = v.r
            else:
                idx = bisect_left(v.nums, x)
                if v.nums[idx] == x:
                    return x
                return v.nums[idx - 1]
        return None if ans == x else ans
    
    # x未満の最大要素, 無い場合はNone
    def l(self, x):
        v = self.root
        if v.size == 0:
            return None
        ans = x
        while v:
            if x <= v.nums[0]:
                v = v.l
            elif x > v.nums[-1]:
                if ans == x:
                    ans = v.nums[-1]
                else:
                    ans = max(ans, v.nums[-1])
                v = v.r
            else:
                idx = bisect_left(v.nums, x)
                return v.nums[idx - 1]
        return None if ans == x else ans
    
    # x以上の最小要素, 無い場合はNone
    def ge(self, x):
        v = self.root
        if v.size == 0:
            return None
        ans = x
        while v:
            if x < v.nums[0]:
                if ans == x:
                    ans = v.nums[0]
                else:
                    ans = min(ans, v.nums[0])
                v = v.l
            elif x > v.nums[-1]:
                v = v.r
            else:
                idx = bisect_left(v.nums, x)
                return v.nums[idx]
        return None if ans == x else ans
    
    # xより大きい最小要素, 無い場合はNone
    def g(self, x):
        v = self.root
        if v.size == 0:
            return None
        ans = x
        while v:
            if x < v.nums[0]:
                if ans == x:
                    ans = v.nums[0]
                else:
                    ans = min(ans, v.nums[0])
                v = v.l
            elif x >= v.nums[-1]:
                v = v.r
            else:
                idx = bisect_right(v.nums, x)
                return v.nums[idx]
        return None if ans == x else ans
    
    # x以下の要素数
    def le_count(self, x):
        v = self.root
        if v.size == 0:
            return 0
        ans = 0
        while v:
            if x < v.nums[0]:
                v = v.l
            elif x >= v.nums[-1]:
                if v.l:
                    ans += v.l.size
                ans += len(v.nums)
                v = v.r
            else:
                if v.l:
                    ans += v.l.size
                ans += bisect_right(v.nums, x)
                return ans
        return ans
    
    # x未満の要素数
    def l_count(self, x):
        v = self.root
        if v.size == 0:
            return 0
        ans = 0
        while v:
            if x <= v.nums[0]:
                v = v.l
            elif x > v.nums[-1]:
                if v.l:
                    ans += v.l.size
                ans += len(v.nums)
                v = v.r
            else:
                if v.l:
                    ans += v.l.size
                ans += bisect_left(v.nums, x)
                return ans
        return ans
    
    # x以上の要素数
    def ge_count(self, x):
        v = self.root
        if v.size == 0:
            return 0
        ans = 0
        while v:
            if x > v.nums[-1]:
                v = v.r
            elif x <= v.nums[0]:
                if v.r:
                    ans += v.r.size
                ans += len(v.nums)
                v = v.l
            else:
                if v.r:
                    ans += v.r.size
                ans += len(v.nums) - bisect_left(v.nums, x)
                return ans
        return ans
    
    # xより大きい要素数
    def g_count(self, x):
        v = self.root
        if v.size == 0:
            return 0
        ans = 0
        while v:
            if x >= v.nums[-1]:
                v = v.r
            elif x < v.nums[0]:
                if v.r:
                    ans += v.r.size
                ans += len(v.nums)
                v = v.l
            else:
                if v.r:
                    ans += v.r.size
                ans += len(v.nums) - bisect_right(v.nums, x)
                return ans
        return ans