import std_heap
import interval_heap

class erasable_min_heap:
  def __init__(self):
    self.h = std_heap.min_heap()
    self.d = {}
    self.sz = 0
  
  # サイズ
  def size(self):
    return self.sz

  # 空か
  def empty(self):
    return self.sz == 0

  # 配列から構築
  def make_heap(self, v):
    for x in v:
      if x in self.d:
        self.d[x] += 1
      else:
        self.d[x] = 1
    self.h.make_heap(v)
    self.sz = self.h.size()

  # xを追加
  def push(self, x):
    if x in self.d:
      self.d[x] += 1
    else:
      self.d[x] = 1
    self.h.push(x)
    self.sz += 1

  # xの数
  def count(self, x):
    return self.d[x] if x in self.d else 0
  
  # xを1個消す(すでにない場合は何もしない)
  def erase(self, x):
    if x in self.d and self.d[x] > 0:
      self.d[x] -= 1
      self.sz -= 1

  # 最小値, ない場合はNone
  def min(self):
    ans = self.h.min()
    while ans and self.d[ans] == 0:
      self.h.pop_min()
      ans = self.min()
    return ans

  # 最小値をpopして返す, ない場合はNone
  def pop_min(self):
    ans = self.h.pop_min()
    while ans and self.d[ans] == 0:
      ans = self.h.pop_min()
    if ans:
       self.sz -= 1
    return ans

class erasable_max_heap:
  def __init__(self):
    self.h = std_heap.max_heap()
    self.d = {}
    self.sz = 0
  
  # サイズ
  def size(self):
    return self.sz

  # 空か
  def empty(self):
    return self.sz == 0

  # 配列から構築
  def make_heap(self, v):
    for x in v:
      if x in self.d:
        self.d[x] += 1
      else:
        self.d[x] = 1
    self.h.make_heap(v)
    self.sz = self.h.size()

  # xを追加
  def push(self, x):
    if x in self.d:
      self.d[x] += 1
    else:
      self.d[x] = 1
    self.h.push(x)
    self.sz += 1

  # xの数
  def count(self, x):
    return self.d[x] if x in self.d else 0
  
  # xを1個消す(すでにない場合は何もしない)
  def erase(self, x):
    if x in self.d and self.d[x] > 0:
      self.d[x] -= 1
      self.sz -= 1

  # 最大値, ない場合はNone
  def max(self):
    ans = self.h.min()
    while ans and self.d[ans] == 0:
      self.h.pop_min()
      ans = self.min()
    return ans

  # 最大値をpopして返す, ない場合はNone
  def pop_max(self):
    ans = self.h.pop_min()
    while ans and self.d[ans] == 0:
      ans = self.h.pop_min()
    if ans:
       self.sz -= 1
    return ans

class erasable_interval_heap:
  def __init__(self):
    self.h = interval_heap.interval_heap()
    self.d = {}
    self.sz = 0
  
  # サイズ
  def size(self):
    return self.sz

  # 空か
  def empty(self):
    return self.sz == 0

  # 配列から構築
  def make_heap(self, v):
    for x in v:
      if x in self.d:
        self.d[x] += 1
      else:
        self.d[x] = 1
    self.h.make_heap(v)
    self.sz = self.h.size()

  # xを追加
  def push(self, x):
    if x in self.d:
      self.d[x] += 1
    else:
      self.d[x] = 1
    self.h.push(x)
    self.sz += 1

  # xの数
  def count(self, x):
    return self.d[x] if x in self.d else 0
  
  # xを1個消す(すでにない場合は何もしない)
  def erase(self, x):
    if x in self.d and self.d[x] > 0:
      self.d[x] -= 1
      self.sz -= 1

  # 最小値, ない場合はNone
  def min(self):
    ans = self.h.min()
    while ans and self.d[ans] == 0:
      self.h.pop_min()
      ans = self.min()
    return ans

  # 最大値
  def max(self):
    ans = self.h.max()
    while ans and self.d[ans] == 0:
      self.h.pop_max()
      ans = self.max()
    return ans

  # 最小値をpopして返す, ない場合はNone
  def pop_min(self):
    ans = self.h.pop_min()
    while ans and self.d[ans] == 0:
      ans = self.h.pop_min()
    if ans:
       self.sz -= 1
    return ans

  # 最大値をpopして返す, ない場合はNone
  def pop_max(self):
    ans = self.h.pop_max()
    while ans and self.d[ans] == 0:
      ans = self.h.pop_max()
    if ans:
       self.sz -= 1
    return ans