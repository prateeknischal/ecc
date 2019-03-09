from ecc.core import ecc

class P256(ecc.Curve):
    # See FIPS 186-3, section D.2.3
    # https://csrc.nist.gov/csrc/media/publications/fips/186/3/archive/2009-06-25/documents/fips_186-3.pdf
    # y^2 = x^3-3x+41058363725152142129326129780047268409114441015993725554835256314039467401291
    name = "P-256"
    curve = [
        41058363725152142129326129780047268409114441015993725554835256314039467401291, #constant
        -3, # coeff of x
        0,  # coeff of x^2
        1   # coeff of x^3
    ]
    mod = pow(2, 256) - pow(2, 224) + pow(2, 192) + pow(2, 96) - 1
    N = 115792089210356248762697446949407573529996955224135760342422259061068512044369
    G = ecc.Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
        0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

    Ln = 256

    # D.1.2.3 Curve P-256
    # p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
    # n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
    # SEED = c49d3608 86e70493 6a6678e1 139d26b7 819f7e90
    # c = 7efba166 2985be94 03cb055c 75d4f7e0 ce8d84a9 c5114abc af317768 0104fa0d
    # b = 5ac635d8 aa3a93e7 b3ebbd55 769886bc 651d06b0 cc53b0f6 3bce3c3e 27d2604b
    # G x = 6b17d1f2 e12c4247 f8bce6e5 63a440f2 77037d81 2deb33a0 f4a13945 d898c296
    # G y = 4fe342e2 fe1a7f9b 8ee7eb4a 7c0f9e16 2bce3357 6b315ece cbb64068 37bf51f5

    def __init__(self):
        pass

class secp256k1(ecc.Curve):
    # See https://en.bitcoin.it/wiki/Secp256k1
    name = 'secp256k1'
    curve = [7, 0, 0, 1]

    mod = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - 1
    N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
    G = ecc.Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
        0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)

    Ln = 256

    def __init__(self):
        pass