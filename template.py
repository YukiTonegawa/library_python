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

