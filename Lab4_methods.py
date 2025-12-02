import numpy as np

with open("input.txt", "r") as f:
    A = [list(map(float, line.split())) for line in f if line.strip()]
    if len(A) != len(A[0]):
        raise ValueError("Матриця повинна бути квадратною!")


def is_symmetric(A, tol=1e-12):
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[i][j] - A[j][i]) > tol:
                return False
    return True


if not is_symmetric(A):
    raise ValueError("Матриця не симетрична")

A = np.array(A)
n = len(A)
y = [1, 1, 1, 1]
eps = 1e-6

s = np.dot(y, y)
norm = np.sqrt(s)
x = y / norm
lambda_old = 0
k = 0

while True:
    k += 1
    y_new = np.linalg.solve(A, x)

    max_idx = np.argmax(np.abs(y_new))

    if abs(x[max_idx]) < 1e-12:
        print("Попередження: ділення на мале число при оцінці lambda.")
        s_norm = np.dot(y_new, y_new)
        lambda_inv = np.sqrt(s_norm)
        if abs(lambda_inv) < 1e-12:
            raise ValueError("Вектор став нульовим.")
    else:
        lambda_inv = y_new[max_idx] / x[max_idx]

    s = np.dot(y_new, y_new)
    norm = np.sqrt(s)
    if norm < 1e-12:
        raise ValueError("Норма вектора стала нульовою.")
    x = y_new / norm

    if abs(lambda_inv - lambda_old) < eps:
        print(f"Збіжність досягнута на ітерації {k}")
        break

    lambda_old = lambda_inv

lambda_min = 1 / lambda_inv
residual = np.linalg.norm(A @ x - lambda_min * x)

print("Найменше за модулем власне число:", lambda_min)
print("Відповідний власний вектор:")
print(x)
print(f"Нев’язка: {residual:.6e}")

with open("output.txt", "w") as f:
    f.write(f"{lambda_min}\n")
    for val in x:
        f.write(f"{val:.10f}\n")