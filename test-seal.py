import ahem
import numpy as np

ahem.test()
port = int(input("Enter host:"))
ahem.setup_host("172.17.0.2", port)

keygen = ahem.KeyGenerator(ahem.context)

mat = np.random.randint(0, 10, [3,8])
print(mat)
mat2 = 2*mat
mat2 = mat2.T
print(mat2)
print("cm:")
cm = ahem.CipherMatrix()
print("b:")
b = ahem.CipherMatrix()


cm.encrypt(mat, keygen)
b.encrypt(mat2, keygen)
#
# print("result")
print(np.matmul(mat2, mat))
print(np.matmul(mat, mat2))
# # print(cm.decrypt())
# # print(b.decrypt())
# print('computing')
# res = b * cm
# print('computed')
# # print(res)
# res.save('/seal-project/save/')
# print("saved\nresult:")
# print(res.decrypt(keygen = keygen))
# print(cm.decrypt(keygen = keygen))
# print(b.decrypt(keygen = keygen))

# print(cm.matrix)
# cm.save("/seal-project/save/")

test = ahem.cloud.multiply_request(b, cm)


# test = ahem.CipherMatrix()
# test =
# cpmt_num = input("Enter matrix number: ")
# test.load("/seal-project/save/" + cpmt_num)

print(test)
print("loaded, decrypted result")
res_mat = test.decrypt(keygen=keygen)
print(res_mat)

#
# cm.encrypt(mat)

# print(cm)
#
# new_mat = cm.decrypt()
#
# print(new_mat)
# print(type(new_mat))