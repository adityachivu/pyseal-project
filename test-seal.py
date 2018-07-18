import ahem
import numpy as np

ahem.test()
port = int(input("Enter port:"))
ahem.setup_host("172.17.0.3", port)

keygen = ahem.KeyGenerator(ahem.context)

# mat = np.random.randint(0, 10, [3,8])
mat = np.random.random(size=[4,4])
mat2 = 2*mat
mat2 = mat2.T

print("\nMatrix 1:")
print(mat)
print("\nMatrix 2:")
print(mat2)

print("\nCipherMatrix A: ", end='')
A = ahem.CipherMatrix()
print("CipherMatrix B: ", end='')
B = ahem.CipherMatrix()

A.encrypt(mat, keygen)
B.encrypt(mat2, keygen)

result = ahem.cloud.add_request(A, B)
print("\nResult Loaded, Decrypted")
res_mat = result.decrypt(keygen=keygen)
print(res_mat)
print("\nExpected Result:")
print(np.matmul(mat, mat2))

result = ahem.cloud.subtract_request(A, B)
print("\nResult Loaded, Decrypted")
res_mat = result.decrypt(keygen=keygen)
print(res_mat)
print("\nExpected Result:")
print(np.matmul(mat, mat2))

result = ahem.cloud.multiply_request(A, B)
print("\nResult Loaded, Decrypted")
res_mat = result.decrypt(keygen=keygen)
print(res_mat)
print("\nExpected Result:")
print(np.matmul(mat, mat2))