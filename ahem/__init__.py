from . import ciphermatrix
from .ciphermatrix import *

parms = EncryptionParameters()
parms.set_poly_modulus("1x^8192 + 1")
parms.set_coeff_modulus(seal.coeff_modulus_128(8192))
parms.set_plain_modulus(1 << 8)

context = SEALContext(self.parms)