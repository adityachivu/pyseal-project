import ahem
import numpy as np

ahem.test()
port = int(input("Enter port:"))
ahem.setup_host("172.17.0.3", port)

ahem.close_server()