import ahem
import numpy as np

ahem.test()

# mat = np.random.randint(0, 10, [3,8])
# print(mat)
# mat2 = 2*mat
# mat2 = mat2.T
# cm = ahem.CipherMatrix(mat)
# b = ahem.CipherMatrix()

# b.encrypt(mat2, cm.get_keygen())

# print(cm.decrypt())
# print(b.decrypt())
# res = b * cm
# print(res)
# res.save('/seal-project/save/')
# print(b.decrypt(keygen = cm.get_keygen()))

# print(cm.matrix)
# cm.save("/seal-project/save/")


test = ahem.CipherMatrix()
test.load("/seal-project/save/0098")

print(test)

print(test.decrypt())

#
# cm.encrypt(mat)

# print(cm)
#
# new_mat = cm.decrypt()
#
# print(new_mat)
# print(type(new_mat))