import ahem
import numpy as np

ahem.test()

mat = np.ones([2, 2], dtype=np.int32)
mat2 = 2*mat
cm = ahem.CipherMatrix(mat)
b = ahem.CipherMatrix()

b.encrypt(mat2, cm.get_keygen())

print(cm.decrypt())
print(b.decrypt())
# res = b * cm
# print(res)
# print(res.decrypt())
#
# cm.encrypt(mat)

# print(cm)
#
# new_mat = cm.decrypt()
#
# print(new_mat)
# print(type(new_mat))