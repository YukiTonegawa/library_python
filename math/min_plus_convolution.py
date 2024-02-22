from collections import deque

# aが凸
def min_plus_convolution(a, b) -> list:
    n, m = len(a), len(b)
    c = [0] * (n + m - 1)
    q = deque()
    q.append((0, n + m - 1, 0, max(n, m)))
    while q:
        lk, rk, li, ri = q.popleft()
        midk = (lk + rk) // 2
        mn, amn = inf, li
        for i in range(li, ri):
            if midk >= i and midk - i < n and i < m and a[midk - i] + b[i] < mn:
                mn, amn = a[midk - i] + b[i], i
        c[midk] = mn
        if rk > midk + 1:
            q.append((midk + 1, rk, amn, ri))
        if midk > lk:
            q.append((lk, midk, li, amn + 1))
    return c;