import base64
import subprocess
import unittest

from ecc.core import ecc, shanks
from ecc import curves
from ecc.utils import util

class TestECC(unittest.TestCase):
    def test_shanks(self):
        print ("Testing using P-256 Generator point")
        curve = curves.P256()
        x = curve.G.x
        y = curve.G.y

        y_square = curve.F(x)

        y_sol = shanks.quadratic_residue(y_square, curve.mod)

        print ("Curve.G.y : {}".format(y))
        print ("Caluclated: {}".format(y_sol))

        self.assertEqual(y, y_sol)

    def test_generator(self):
        print ("Testing Generator point for P-256")
        curve = curves.P256()
        inf = ecc.Point(0, 0, zero=True)
        self.assertEqual(inf, curve.mul(curve.G, curve.N))

    def test_signature(self):
        pkey = 0x00c3f7c39a9be2418cd89a732e40d648b09fa0af9e909a4fb6864910144b5cbcdf
        print ('Elliptic Curve P-256')
        print ()

        curve = curves.P256()
        print ('Sign EC-SHA256: "{}"'.format('This is a sample message'))
        (r, s) = curve.sign(b'This is a sample message', pkey)
        util.asn1_marshal((r, s))
        print ()

        print ('base64 DER signature calculated:')
        with open('data/x.txt', 'rb') as f:
            print (base64.standard_b64encode(f.read()))
        print ()

        cmd = ['openssl', 'dgst', '-sha256', '-verify', 'data/pub.pem',
            '-signature', 'data/x.txt', 'data/a.txt']
        print ('Verify using openssl')
        print (' '.join(cmd))
        r = subprocess.run(['openssl', 'dgst', '-sha256', '-verify',
            'data/pub.pem', '-signature', 'data/x.txt', 'data/a.txt'])

        self.assertEqual(r.returncode, 0)
