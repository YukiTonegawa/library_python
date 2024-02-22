class add_sum:
    def id():
        return 0
    def id_lazy():
        return 0    
    def inv(a):
        return -a        
    def reverse(a):
        return a    
    def merge(a, b):
        return a + b    
    def apply_lazy(a, lz):
        return a + lz * sz
    def propagate_lazy(lza, lzb):
        return lza + lzb

class add_sum_mod:
    def __init__(self, mod : int):
        self.mod = mod
    def id(self):
        return 0
    def id_lazy(self):
        return 0    
    def inv(self, a):
        return self.mod - a if a else 0
    def reverse(self, a):
        return a
    def merge(self, a, b):
        return (a + b) % self.mod
    def apply_lazy(self, a, lz, sz):
        return (a + lz * sz) % self.mod
    def propagate_lazy(self, lza, lzb):
        return (lza + lzb) % self.mod


class add_max:
    def id():
        return -(1 << 62)
    def id_lazy():
        return 0
    def reverse(a):
        return a
    def merge(a, b):
        return max(a, b)
    def apply_lazy(a, lz, sz):
        return a + lz if a != -(1 << 62) else lz
    def propagate_lazy(lza, lzb):
        return lza + lzb

  