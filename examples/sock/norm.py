from numpy import linalg as LA
import numpy as np

a=np.arange(8) - 4
b = a.reshape((4, 2))

print(b)
print(LA.norm(b,axis=1))