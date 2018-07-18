from . import ciphermatrix
from .ciphermatrix import *
from .ciphermatrix import EncryptionParameters, SEALContext

from . import cloud
from .cloud import *
from .cloud.evaluate import *

parms = EncryptionParameters()
parms.set_poly_modulus("1x^2048 + 1")
parms.set_coeff_modulus(seal.coeff_modulus_128(2048))
parms.set_plain_modulus(1 << 8)

context = SEALContext(parms)