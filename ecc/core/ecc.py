import asn1tools
import binascii
import copy
import hashlib
import random

from ecc.utils import util

class Point:
    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y
        self.z = kwargs.get('zero', False)

    def normalize(self, mod):
        self.x = self.x % mod
        self.y = self.y % mod
        return self

    def __str__(self):
        return "({},{})".format(self.x, self.y) if not self.z else "Inf"

    def __eq__(self, t):
        if self.z & t.z: return True
        if self.z != t.z: return False
        return self.x == t.x and self.y == t.y

class Curve:
    # See FIPS 186-3, section D.2.3
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
    G = Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
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

def F(p, n = Curve.mod):
    F = sum(Curve.curve[i] * pow(x, i, n) for i in range(len(curve))) % n

def slope(p, q):
    if p.z or q.z:
        return None
    m = None
    if p == q:
        if p.y == 0:
            return None
        m = 3 * pow(p.x, 2, Curve.mod) + Curve.curve[1]
        m = (m % Curve.mod) * util.inv(2 * p.y, Curve.mod)
    else:
        if q.x == p.x:
            return None
        m = (q.y - p.y) * util.inv(q.x - p.x, Curve.mod)

    m = m % Curve.mod
    return m

def add(p, q):
    if p.z: return Point(q.x, q.y, zero=q.z).normalize(Curve.mod)
    if q.z: return Point(p.x, p.y, zero=p.z).normalize(Curve.mod)

    m = slope(p, q)
    if m is None:
        return Point(0, 0, zero=True)

    x = pow(m, 2, Curve.mod) - p.x - q.x
    y = m * (x - p.x) + p.y
    return Point(x, -y).normalize(Curve.mod)

def mul(p, v):
    res = Point(0, 0, zero=True)
    d = copy.deepcopy(p)
    while v > 0:
        if v & 1:
            res = add(res, d)
        d = add(d, d)
        v >>= 1
    return res.normalize(Curve.mod)

def sign(s, pkey):
    if type(s) != type(bytes()):
        print ("Input needs to be a bytes type object")
        return None
    z = hashlib.sha256(s).digest()[:256]
    z = int(binascii.hexlify(z), 16)
    k, cp = None, None
    while True:
        k = random.randint(1, Curve.N - 1)

        # curve point kG
        cp = mul(Curve.G, k)
        if cp.x % Curve.N != 0:
            break

    r = cp.x % Curve.N
    s = util.inv(k, Curve.N) * (z +  (r * pkey % Curve.N))
    s = s % Curve.N

    print ("({},{})".format(r, s))
    return (r, s)
