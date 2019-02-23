"""
-----BEGIN EC PARAMETERS-----
BggqhkjOPQMBBw==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIMP3w5qb4kGM2JpzLkDWSLCfoK+ekJpPtoZJEBRLXLzfoAoGCCqGSM49
AwEHoUQDQgAEPHX7+SKmDCQvxiIqimYVTfhk+toXxomN8HuFu6LnAdNYzOdi3mHz
99Fy9n7yR6QDzorLOcngyzmfEwcZAtG9Iw==
-----END EC PRIVATE KEY-----

$ openssl ec -in ec.pem -noout -text
read EC key
Private-Key: (256 bit)
priv:
    00:c3:f7:c3:9a:9b:e2:41:8c:d8:9a:73:2e:40:d6:
    48:b0:9f:a0:af:9e:90:9a:4f:b6:86:49:10:14:4b:
    5c:bc:df
pub:
    04:3c:75:fb:f9:22:a6:0c:24:2f:c6:22:2a:8a:66:
    15:4d:f8:64:fa:da:17:c6:89:8d:f0:7b:85:bb:a2:
    e7:01:d3:58:cc:e7:62:de:61:f3:f7:d1:72:f6:7e:
    f2:47:a4:03:ce:8a:cb:39:c9:e0:cb:39:9f:13:07:
    19:02:d1:bd:23
ASN1 OID: prime256v1
NIST CURVE: P-256


$ openssl ec -in curve.pem -pubout -out pub.pem
$ openssl dgst -sha256 -sign curve.pem -out sign.txt.sha256 a.txt
$ openssl dgst -sha256 -verify pub.pem -signature sign.txt.sha256 a.txt
$ openssl dgst -sha256 -verify pub.pem -signature x.txt a.txt
$ openssl asn1parse -in sign.txt.sha256 -inform DER
"""

from core import ecc, util
import subprocess
import base64

if __name__ == '__main__':
    pkey = 0x00c3f7c39a9be2418cd89a732e40d648b09fa0af9e909a4fb6864910144b5cbcdf
    print ('Elliptic Curve P-256')
    print ()

    print ('Sign EC-SHA256: "{}"'.format('This is a sample message'))
    (r, s) = ecc.sign(b'This is a sample message', pkey)
    util.asn1_marshal((r, s))
    print ()

    print ('base64 DER signature calculated:')
    with open('data/x.txt', 'rb') as f:
        print (base64.standard_b64encode(f.read()))
    print ()

    cmd = ['openssl', 'dgst', '-sha256', '-verify', 'data/pub.pem', '-signature', 'data/x.txt', 'data/a.txt']
    print ('Verify using openssl')
    print (' '.join(cmd))
    subprocess.run(['openssl', 'dgst', '-sha256', '-verify', 'data/pub.pem', '-signature', 'data/x.txt', 'data/a.txt'])
