import time
import random
import threading
import seal
import numpy as np
from seal import ChooserEvaluator,     \
                 Ciphertext,           \
                 Decryptor,            \
                 Encryptor,            \
                 EncryptionParameters, \
                 Evaluator,            \
                 IntegerEncoder,       \
                 FractionalEncoder,    \
                 KeyGenerator,         \
                 MemoryPoolHandle,     \
                 Plaintext,            \
                 SEALContext,          \
                 EvaluationKeys,       \
                 GaloisKeys,           \
                 PolyCRTBuilder,       \
                 ChooserEncoder,       \
                 ChooserEvaluator,     \
                 ChooserPoly

# import sealimports

def dot_product():
    print("Example: Weighted Average")

    # In this example we demonstrate the FractionalEncoder, and use it to compute
    # a weighted average of 10 encrypted rational numbers. In this computation we
    # perform homomorphic multiplications of ciphertexts by plaintexts, which is
    # much faster than regular multiplications of ciphertexts by ciphertexts.
    # Moreover, such `plain multiplications' never increase the ciphertext size,
    # which is why we have no need for evaluation keys in this example.

    # We start by creating encryption parameters, setting up the SEALContext, keys,
    # and other relevant objects. Since our computation has multiplicative depth of
    # only two, it suffices to use a small poly_modulus.
    parms = EncryptionParameters()
    parms.set_poly_modulus("1x^2048 + 1")
    parms.set_coeff_modulus(seal.coeff_modulus_128(2048))
    parms.set_plain_modulus(1 << 8)

    context = SEALContext(parms)
    print_parameters(context)

    keygen = KeyGenerator(context)
    keygen2 = KeyGenerator(context)
    public_key = keygen.public_key()
    secret_key = keygen.secret_key()

    secret_key2 = keygen.secret_key()

    # We also set up an Encryptor, Evaluator, and Decryptor here.
    encryptor = Encryptor(context, public_key)
    evaluator = Evaluator(context)
    decryptor = Decryptor(context, secret_key2)

    # Create a vector of 10 rational numbers (as doubles).
    # rational_numbers = [3.1, 4.159, 2.65, 3.5897, 9.3, 2.3, 8.46, 2.64, 3.383, 2.795]
    rational_numbers = np.random.rand(10)

    # Create a vector of weights.
    # coefficients = [0.1, 0.05, 0.05, 0.2, 0.05, 0.3, 0.1, 0.025, 0.075, 0.05]
    coefficients = np.random.rand(10)

    my_result = np.dot(rational_numbers, coefficients)

    # We need a FractionalEncoder to encode the rational numbers into plaintext
    # polynomials. In this case we decide to reserve 64 coefficients of the
    # polynomial for the integral part (low-degree terms) and expand the fractional
    # part to 32 digits of precision (in base 3) (high-degree terms). These numbers
    # can be changed according to the precision that is needed; note that these
    # choices leave a lot of unused space in the 2048-coefficient polynomials.
    encoder = FractionalEncoder(context.plain_modulus(), context.poly_modulus(), 64, 32, 3)

    # We create a vector of ciphertexts for encrypting the rational numbers.
    encrypted_rationals = []
    rational_numbers_string = "Encoding and encrypting: "
    for i in range(10):
        # We create our Ciphertext objects into the vector by passing the
        # encryption parameters as an argument to the constructor. This ensures
        # that enough memory is allocated for a size 2 ciphertext. In this example
        # our ciphertexts never grow in size (plain multiplication does not cause
        # ciphertext growth), so we can expect the ciphertexts to remain in the same
        # location in memory throughout the computation. In more complicated examples
        # one might want to call a constructor that reserves enough memory for the
        # ciphertext to grow to a specified size to avoid costly memory moves when
        # multiplications and relinearizations are performed.
        encrypted_rationals.append(Ciphertext(parms))
        encryptor.encrypt(encoder.encode(rational_numbers[i]), encrypted_rationals[i])
        rational_numbers_string += (str)(rational_numbers[i])[:6]
        if i < 9: rational_numbers_string += ", "
    print(rational_numbers_string)

    # Next we encode the coefficients. There is no reason to encrypt these since they
    # are not private data.
    encoded_coefficients = []
    encoded_coefficients_string = "Encoding plaintext coefficients: "


    encrypted_coefficients =[]

    for i in range(10):
        encoded_coefficients.append(encoder.encode(coefficients[i]))
        encrypted_coefficients.append(Ciphertext(parms))
        encryptor.encrypt(encoded_coefficients[i], encrypted_coefficients[i])
        encoded_coefficients_string += (str)(coefficients[i])[:6]
        if i < 9: encoded_coefficients_string += ", "
    print(encoded_coefficients_string)

    # We also need to encode 0.1. Multiplication by this plaintext will have the
    # effect of dividing by 10. Note that in SEAL it is impossible to divide
    # ciphertext by another ciphertext, but in this way division by a plaintext is
    # possible.
    div_by_ten = encoder.encode(0.1)

    # Now compute each multiplication.

    prod_result = [Ciphertext() for i in range(10)]
    prod_result2 = [Ciphertext() for i in range(10)]

    print("Computing products: ")
    for i in range(10):
        # Note how we use plain multiplication instead of usual multiplication. The
        # result overwrites the first argument in the function call.
        evaluator.multiply_plain(encrypted_rationals[i], encoded_coefficients[i], prod_result[i])
        evaluator.multiply(encrypted_rationals[i], encrypted_coefficients[i], prod_result2[i])
    print("Done")

    # To obtain the linear sum we need to still compute the sum of the ciphertexts
    # in encrypted_rationals. There is an easy way to add together a vector of
    # Ciphertexts.

    encrypted_result = Ciphertext()
    encrypted_result2 = Ciphertext()

    print("Adding up all 10 ciphertexts: ")
    evaluator.add_many(prod_result, encrypted_result)
    evaluator.add_many(prod_result2, encrypted_result2)

    print("Done")

    # Perform division by 10 by plain multiplication with div_by_ten.
    # print("Dividing by 10: ")
    # evaluator.multiply_plain(encrypted_result, div_by_ten)
    # print("Done")

    # How much noise budget do we have left?
    print("Noise budget in result: " + (str)(decryptor.invariant_noise_budget(encrypted_result)) + " bits")

    # Decrypt, decode, and print result.
    plain_result = Plaintext()
    plain_result2 = Plaintext()
    print("Decrypting result: ")
    decryptor.decrypt(encrypted_result, plain_result)
    decryptor.decrypt(encrypted_result2, plain_result2)
    print("Done")

    result = encoder.decode(plain_result)
    print("Weighted average: " + (str)(result)[:8])

    result2 = encoder.decode(plain_result2)
    print("Weighted average: " + (str)(result2)[:8])

    print('\n\n', my_result)


def print_parameters(context):
    print("/ Encryption parameters:")
    print("| poly_modulus: " + context.poly_modulus().to_string())

    # Print the size of the true (product) coefficient modulus
    print("| coeff_modulus_size: " + (str)(context.total_coeff_modulus().significant_bit_count()) + " bits")

    print("| plain_modulus: " + (str)(context.plain_modulus().value()))
    print("| noise_standard_deviation: " + (str)(context.noise_standard_deviation()))

def main():
    # a = sealimports.CipherMatrix(params = 1, matrix = 1)
    dot_product()
    # sealimports.blah()

if __name__ == '__main__':
    main()