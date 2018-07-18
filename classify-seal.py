import ahem
import numpy as np
import time

ahem.test()
port = int(input("Enter port:"))
ahem.setup_host("172.17.0.3", port)

keygen = ahem.KeyGenerator(ahem.context)


batch = np.load('save/batch.npy')
label = np.load('save/label.npy')

index = int(input("Choose Image Index: "))

x = batch[index,np.newaxis]
y = np.argmax(label[index,np.newaxis], axis=1)

img = ahem.CipherMatrix(x)
img.encrypt(keygen=keygen)

result = ahem.cloud.classify_request(img)

prob = result.decrypt(keygen=keygen)

pred = np.argmax(prob, axis=1)

print("\n\nAnd the prediction is...\n\n")
time.sleep(1.5)
print("drumroll please...\n\n")
time.sleep(1.5)
print(pred)