from array import array
import typing
class unweighted_tree:
    def __init__(self, n : int) -> None:
        # 基本情報
        self.n = n
        self.g = [array('i') for _ in range(n)]

        # dfsの情報
        self.root = None
        self.sz   = None
        self.par  = None
        self.dep  = None
        self.tour = None

        # hldの情報
        self.head  = None
        self.heavy = None

        # euler_tourの情報
        self.tour_in  = None
        self.tour_out = None
    
    # 無向辺u-vを追加
    # O(1)
    def add_edge(self, u : int, v : int) -> None:
        self.g[u].append(v)
        self.g[v].append(u)
    
    # rootを根としてdfs
    # O(N)
    def build_dfs(self, root : int) -> None:
        self.root = root
        st = array('i', [root])
        self.sz   = array('i', [1] * self.n)
        self.par  = array('i', [-1] * self.n)
        self.dep  = array('i', [0] * self.n)
        self.tour = array('i')

        # tourテーブル
        while st:
            v = st.pop()
            self.tour.append(v)
            for u in self.g[v]:
                if u == self.par[v]:
                    continue
                self.par[u] = v
                self.dep[u] = self.dep[v] + 1
                st.append(u)
        
        # 部分木サイズ
        for v in reversed(self.tour[1:]):
            p = self.par[v]
            self.sz[p] += self.sz[v]
    
    # rootを根としてhld
    # O(N)
    def build_hld(self, root : int) -> None:
        # 根が異なる or build_dfsしていない
        if self.root != root:
            self.build_dfs(root)
        self.head  = array('i', [root] * self.n)
        self.heavy = [array('i') for _ in range(self.n)]
        self.sz.append(-1) # 常に部分木サイズ-1を返すダミー
        heavy_c = array('i', [-1] * n) # 部分木サイズ最大の子
        for v in reversed(self.tour[1:]):
            p = self.par[v]
            phc = heavy_c[p]
            if self.sz[phc] < self.sz[v]:
                heavy_c[p] = v 
        self.sz.pop()

        for v in self.tour:
            p = self.par[v]
            self.head[v] = v if (p == -1 or heavy_c[p] != v) else self.head[p]
            self.heavy[self.head[v]].append(v)

    # rootを根としてeuler_tour
    # O(N)
    def build_euler_tour(self, root : int) -> None:
        # 根が異なる or build_dfsしていない
        if self.root != root:
            self.build_dfs(root)
        self.tour_in  = array('i', [0] * n)
        self.tour_out = array('i', [0] * n)
        for i, v in enumerate(self.tour):
            self.tour_in[v]  = i
            self.tour_out[v] = i + 1   
        for v in reversed(self.tour[1:]):
            p = self.par[v]
            if self.tour_out[p] < self.tour_out[v]:
                self.tour_out[p] = self.tour_out[v]

    # k個上の祖先, k = 0なら自身, k > depth[u]なら-1
    # O(logN)
    def la(self, u : int, k : int) -> int:
        assert self.heavy, 'do build_hld'
        if self.dep[u] < k:
            return -1
        while True:
            p = self.head[u]
            depth_diff = self.dep[u] - self.dep[p]
            if depth_diff >= k:
                return self.heavy[p][depth_diff - k]
            k -= depth_diff + 1
            u = self.par[p]

    # O(logN)
    def lca(self, u : int, v : int) -> int:
        assert self.heavy, 'do build_hld'
        while True:
            if self.head[u] == self.head[v]:
                return u if self.dep[u] < self.dep[v] else v
            if self.dep[self.head[u]] > self.dep[self.head[v]]:
                u, v = v, u
            v = self.par[self.head[v]]
    
    # u->vパスのk番目, k=0ならu, k>パス長なら-1
    # O(logN)
    def jump_on_tree(self, u : int, v : int, k : int) -> int:
        l = self.lca(u, v)
        diff_l_u = self.dep[u] - self.dep[l]
        if diff_l_u >= k:
            return self.la(u, k)
        k = (self.dep[v] - self.dep[l]) - k + diff_l_u
        if k < 0:
            return -1
        return self.la(v, k)

    # 重みなしの　u-vの距離
    # O(logN)
    def dist(self, u : int, v : int) -> int:
        l = self.lca(u, v)
        return self.dep[u] + self.dep[v] - 2 * self.dep[l]

    # uの部分木がvを含むか(端点含む)
    # build_euler_tourをしているなら O(1)
    # build_hldをしているなら O(logN)
    def contain_subtree(self, u : int, v : int) -> bool:
        # euler_tour済
        if self.tour_in:
            return bool(self.tour_in[u] <= self.tour_in[v] and self.tour_in[v] < self.tour_out[u])
        assert self.heavy, 'do build_hld'
        if self.dep[u] > self.dep[v]:
            return False
        return u == self.la(v, self.dep[v] - self.dep[u])
    
    # u-vパスがwを含むか(端点含む)
    # O(logN)
    def contain_path(self, u : int, v : int, w : int) -> bool:
        if self.lca(u, v) == w:
            return True
        return bool(self.contain_subtree(w, u) ^ self.contain_subtree(u, v))
    
    
    # 頂点番号 -> euler_tour上のインデックス
    def et_v2idx(self, v : int) -> int:
        assert self.tour_in, 'do build_euler_tour'
        return self.tour_in[v]

    # 頂点番号 -> euler_tour上のvの　部分木の区間[l, r)
    def et_v2range(self, v : int) -> tuple:
        assert self.tour_in, 'do build_hld'
        return (self.tour_in[v], self.tour_out[v])