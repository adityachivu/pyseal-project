import ahem
import numpy as np
import time

ahem.test()
port = int(input("Enter port:"))
ahem.setup_host("172.17.0.3", port)

keygen = ahem.KeyGenerator(ahem.context)

length = int(input("Enter matrix side length: "))
mat = np.random.random(size=[length,length])
mat2 = 2*mat
mat2 = mat2.T

print("\nMatrix 1:")
print(mat)
print("\nMatrix 2:")
print(mat2)
time.sleep(5)

print("\nCipherMatrix A: ", end='')
A = ahem.CipherMatrix()
print("CipherMatrix B: ", end='')
B = ahem.CipherMatrix()

A.encrypt(mat, keygen)
B.encrypt(mat2, keygen)

print("\n\n\n--------------------ADDITION---------------------")
result = ahem.cloud.add_request(A, B)
print("\nResult Loaded, Decrypted")
res_mat = result.decrypt(keygen=keygen)
print(res_mat)
print("\nExpected Result:")
print(mat + mat2)
time.sleep(5)
print("\n\n\n-------------------SUBTRACTION-------------------")
result = ahem.cloud.sub_request(A, B)
print("\nResult Loaded, Decrypted")
res_mat = result.decrypt(keygen=keygen)
print(res_mat)
print("\nExpected Result:")
print(mat-mat2)
time.sleep(5)
print("\n\n\n------------------MULTIPLICATION-----------------")
result = ahem.cloud.multiply_request(A, B)
print("\nResult Loaded, Decrypted")
res_mat = result.decrypt(keygen=keygen)
print(res_mat)
print("\nExpected Result:")
print(np.matmul(mat, mat2))

