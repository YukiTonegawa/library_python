from array import array
mask00_16 = 0x0000ffff
mask16_32 = 0xffff0000
mask00_32 = 0xffffffff

popcount_table = []
select_table = []
def init_popcount_table() -> None:
    global popcount_table
    if popcount_table: return
    popcount_table = array('I', [0] * (1 << 16))
    for i in range(1 << 16): popcount_table[i] = (i & 1) + popcount_table[i >> 1]

# popcount (2^16以上だと壊れる)
def popcount16(x : int) -> int:
    return popcount_table[x]

# popcount
def popcount32(x : int) -> int:
    return popcount_table[(x >> 16) & mask00_16] + popcount_table[x & mask00_16]

# popcount
def popcount64(x : int) -> int:
    return popcount_table[(x >> 48) & mask00_16] + popcount_table[(x >> 32) & mask00_16] + popcount_table[(x >> 16) & mask00_16] + popcount_table[x & mask00_16]

# popcount(任意長)
def popcount_any(x : int) -> int:
    return bin(x).count('1')

def init_select_table() -> None:
    init_popcount_table()
    global select_table
    if select_table: return
    select_table = array('i', [-1] * (1 << 20))
    for i in range(1 << 16):
        pcnt = 0
        for j in range(1 << 4):
            if (i >> j) & 1:
                select_table[(i << 4) + pcnt] = j
                pcnt += 1

# xのk個目の1 ない場合は-1
def select16(x : int, k : int) -> int:
    return select_table[((x & mask00_16) << 4) + k]

# xのk個目の1 ない場合は-1
def select32(x : int, k : int) -> int:
    plow = popcount_table[x & mask00_16]
    if plow >= k:
        return select_table[((x & mask00_16) << 4) + k]
    return select_table[(((x >> 16) & mask00_16) << 4) + k - plow] + 16

# xのk個目の1 ない場合は-1
def select64(x : int, k : int) -> int:
    for i in range(4):
        plow = popcount_table[x & mask00_16]
        if plow > k:
            return select_table[((x & mask00_16) << 4) + k] + (i << 4)
        k -= plow
        x >>= 16
    return -1

""""
# xのk-bit以降(k含む)に初めて現れる1の場所 ない場合は-1
def next64(x : int, k : int) -> int:
"""

