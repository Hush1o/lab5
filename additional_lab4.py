import numpy as np

eps = 1e-6

with open("input.txt", "r") as file:
    M = np.array([list(map(float, line.split())) for line in file if line.strip()])

if M.shape[0] != M.shape[1]:
    raise ValueError("Матриця має бути квадратною!")

n = M.shape[0]
sym_tol = 1e-12

for r in range(n):
    for c in range(n):
        if abs(M[r][c] - M[c][r]) > sym_tol:
            raise ValueError("Матриця не симетрична!")

A = M.copy()
E = np.eye(n)

while True:
    off_diag = [[0]*n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if r != c:
                off_diag[r][c] = abs(A[r][c])

    max_val = -float("inf")
    p = q = -1
    for r in range(n):
        for c in range(n):
            if r != c and off_diag[r][c] > max_val:
                max_val = off_diag[r][c]
                p, q = r, c

    if off_diag[p][q] < eps:
        break

    app = A[p, p]
    aqq = A[q, q]
    apq = A[p, q]

    P = 2 * apq
    Q = app - aqq
    delta = np.hypot(P, Q)

    if Q == 0:
        cos_t = sin_t = np.sqrt(2) / 2
    else:
        ratio = abs(Q) / (2 * delta)
        cos_t = np.sqrt(0.5 + ratio)
        sin_t = np.sqrt(0.5 - ratio) * np.sign(P * Q)

    A_new = A.copy()

    A_new[p, p] = cos_t**2 * app + sin_t**2 * aqq + 2*cos_t*sin_t*apq
    A_new[q, q] = sin_t**2 * app + cos_t**2 * aqq - 2*cos_t*sin_t*apq
    A_new[p, q] = A_new[q, p] = (cos_t**2 - sin_t**2)*apq + cos_t*sin_t*(aqq - app)

    for k in range(n):
        if k != p and k != q:
            akp = A[k, p]
            akq = A[k, q]
            A_new[k, p] = A_new[p, k] = cos_t * akp + sin_t * akq
            A_new[k, q] = A_new[q, k] = -sin_t * akp + cos_t * akq

    A = A_new

    T = np.eye(n)
    T[p, p] = cos_t
    T[q, q] = cos_t
    T[p, q] = -sin_t
    T[q, p] = sin_t

    E = E @ T

eig_vals = np.diag(A)

print("\nВласні числа:")
print(eig_vals)

print("\nВласні вектори:")
print(E)

res = M @ E - E @ A
res_norm = np.linalg.norm(res)
print(f"\nНев'язка: {res_norm}")
