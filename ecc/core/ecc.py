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
    def __init__(self, name, curve, mod, N, G, Ln):
        self.name = name
        self.curve = curve
        self.mod = mod
        self.N = N
        self.G = G
        self.Ln = Ln

    def F(self, x):
        return sum(
            self.curve[i] * pow(x, i, self.mod) for i in range(len(self.curve))
        ) % self.mod

    def slope(self, p, q):
        if p.z or q.z:
            return None
        m = None
        if p == q:
            if p.y == 0:
                return None
            m = 3 * pow(p.x, 2, self.mod) + self.curve[1]
            m = (m % self.mod) * util.inv(2 * p.y, self.mod)
        else:
            if q.x == p.x:
                return None
            m = (q.y - p.y) * util.inv(q.x - p.x, self.mod)

        m = m % self.mod
        return m

    def add(self, p, q):
        if p.z: return Point(q.x, q.y, zero=q.z).normalize(self.mod)
        if q.z: return Point(p.x, p.y, zero=p.z).normalize(self.mod)

        m = self.slope(p, q)
        if m is None:
            return Point(0, 0, zero=True)

        x = pow(m, 2, self.mod) - p.x - q.x
        y = m * (x - p.x) + p.y
        return Point(x, -y).normalize(self.mod)

    def mul(self, p, v):
        res = Point(0, 0, zero=True)
        d = copy.deepcopy(p)
        while v > 0:
            if v & 1:
                res = self.add(res, d)
            d = self.add(d, d)
            v >>= 1
        return res.normalize(self.mod)

    def sign(self, s, pkey):
        if type(s) != type(bytes()):
            print ("Input needs to be a bytes type object")
            return None
        z = hashlib.sha256(s).digest()[:self.Ln]
        z = int(binascii.hexlify(z), 16)
        k, cp = None, None
        while True:
            k = random.randint(1, self.N - 1)

            # curve point kG
            cp = self.mul(self.G, k)
            if cp.x % self.N != 0:
                break

        r = cp.x % self.N
        s = util.inv(k, self.N) * (z +  (r * pkey % self.N))
        s = s % self.N

        print ("({},{})".format(r, s))
        return (r, s)

    def verify(self, m, rs, pubkey):
        if type(m) != type(bytes()):
            print ("Input needs to be a bytes type object")
            return False

        if self.mul(pubkey, self.N).z == False:
            return False

        r, s = rs
        if not (1 < r < self.N) or not (1 < s < self.N):
            return False

        z = hashlib.sha256(m).digest()[:self.Ln]
        z = int(binascii.hexlify(z), 16)

        w = util.inv(s, self.N)
        u1 = (z * w) % self.N
        u2 = (r * w) % self.N

        C = self.add(self.mul(self.G, u1), self.mul(pubkey, u2))
        if C.z == True: return False

        return r == C.x
