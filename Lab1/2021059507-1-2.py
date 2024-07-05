/Users/naeunkim/Desktop/24-1/ComputerGraphics import numpy as np

M = np.arange(2,27)
print(M)
print("\n")

M = M.reshape(5,5)
print(M)
print("\n")

M[1:-1, 1:-1] = 0
print(M)
print("\n")

M = M@M
print(M)
print("\n")

v = M[0]
v_size = np.sqrt(np.sum(v**2))
print(v_size)
