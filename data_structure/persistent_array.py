import array
class persistent_array:
  __parray_split = 8
  __parray_mask  = 7
  __parray_shift = 3
  __parray_ch  = []
  __parray_val = []

  def __copy_node(self, v : int) -> int:
    node_id = len(self.__parray_ch)
    if v == -1:
      self.__parray_ch.append(array.array('i', [-1] * self.__parray_split))
      self.__parray_val.append(self.e)
    else:
      self.__parray_ch.append(self.__parray_ch[v][:])
      self.__parray_val.append(self.__parray_val[v])
    return node_id
  
  def __set(self, v : int, i : int, x) -> None:
    while i:
      next_node = self.__parray_ch[v][i & self.__parray_mask]
      next_node = self.__copy_node(next_node)
      self.__parray_ch[v][i & self.__parray_mask] = next_node
      v = next_node
      i >>= self.__parray_shift
    self.__parray_val[v] = x
  
  # 単位元eの配列を初期化(vは必要ない)
  def __init__(self, e, v = -1) -> None:
    if v == -1:
      self.e = e
      self.v = len(self.__parray_ch)
      self.__parray_ch.append(array.array('i', [-1] * self.__parray_split))
      self.__parray_val.append(e)
    else:
      self.e = e
      self.v = v

  # N要素の数列で構築
  def build_sequence(self, A) -> 'persistent_array':
    N = len(A)
    root = len(self.__parray_ch)
    self.__parray_ch.append(array.array('i', [-1] * self.__parray_split))
    self.__parray_val.append(A[0] if N else self.e)
    if N == 0:
      return persistent_array(self.e, root)
    
    st = [(root, 0, 0)]
    while st:
      v, k, d = st[-1]
      st.pop()
      # 0
      if k + (1 << ((d + 1) * self.__parray_shift)) < N:
        idx = len(self.__parray_ch)
        self.__parray_ch[v][0] = idx
        self.__parray_ch.append(array.array('i', [-1] * self.__parray_split))
        self.__parray_val.append(self.e)
        st.append((idx, k, d + 1))

      # [1, split_number)
      for i in range(1, self.__parray_split):
        j = k + (i << (d * self.__parray_shift))
        if j >= N:
          break
        idx = len(self.__parray_ch)
        self.__parray_ch[v][i] = idx
        self.__parray_ch.append(array.array('i', [-1] * self.__parray_split))
        self.__parray_val.append(A[j])
        st.append((idx, j, d + 1))

    return persistent_array(self.e, root)

  # N要素の数列で構築
  def build_sequence(self, A) -> 'persistent_array':
    N = len(A)
    root = len(self.__parray_ch)
    self.__parray_ch.append(array.array('i', [-1] * self.__parray_split))
    self.__parray_val.append(A[0] if N else self.e)
    if N == 0:
      return persistent_array(self.e, root)
    
    st = [(root, 0, 0)]
    while st:
      v, k, d = st[-1]
      st.pop()
      # 0
      if k + (1 << ((d + 1) * self.__parray_shift)) < N:
        idx = len(self.__parray_ch)
        self.__parray_ch[v][0] = idx
        self.__parray_ch.append(array.array('i', [-1] * self.__parray_split))
        self.__parray_val.append(self.e)
        st.append((idx, k, d + 1))

      # [1, split_number)
      for i in range(1, self.__parray_split):
        j = k + (i << (d * self.__parray_shift))
        if j >= N:
          break
        idx = len(self.__parray_ch)
        self.__parray_ch[v][i] = idx
        self.__parray_ch.append(array.array('i', [-1] * self.__parray_split))
        self.__parray_val.append(A[j])
        st.append((idx, j, d + 1))

    return persistent_array(self.e, root)

  # 元の配列に変更を加えず, ai <- xに変更した新バージョンを作る
  def set(self, i : int, x) -> 'persistent_array':
    v = self.__copy_node(self.v)
    self.__set(v, i, x)
    return persistent_array(self.e, v)

  # ai
  def get(self, i : int):
    v = self.v
    while i:
      v = self.__parray_ch[v][i & self.__parray_mask]
      if v == -1:
        return self.e
      i >>= self.__parray_shift
    return self.__parray_val[v]

class persistent_union_find:
  def __find(self, i : int) -> int:
    while True:
      x = self.pa.get(i)
      p = x & ((1 << 30) - 1)
      if p == i:
        return x
      i = p

  def __init__(self, n : int, ver = None) -> None:
    if n != -1:
      assert ver == None
      A = [(1 << 30) + i for i in range(n)]
      self.pa = persistent_array(0).build_sequence(A)
    else:
      assert ver != None
      self.pa = ver

  def find(self, i : int) -> int:
    return self.__find(i) & ((1 << 30) - 1)
  
  def size(self, i : int) -> int:
    return self.__find(i) >> 30

  def same(self, i : int, j : int) -> bool:
    return self.find(i) == self.find(j)
  
  def unite(self, i : int, j : int) -> 'persistent_union_find':
    x = self.__find(i)
    y = self.__find(j)
    i = (x & ((1 << 30) - 1))
    j = (y & ((1 << 30) - 1))
    if i == j:
      return self
    x >>= 30
    y >>= 30
    if x > y:
      x, y = y, x
      i, j = j, i
    pa = self.pa.set(i, (x << 30) + j)
    pa = pa.set(j, ((x + y) << 30) + j)
    return persistent_union_find(-1, pa)
    
    
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
