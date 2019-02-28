import random

from ecc.core import ecc

def quadratic_residue(n, p):
    """Solve Quadratic Residue for n and prime p.

    Solve for the equation x^2 = n mod p.

    Arguments:
        n (int): quadratic residue.
        p (int): prime.
    """
    if pow(n, (p-1)//2, p) == p - 1:
        return 0

    s, Q = 0, p - 1
    while Q % 2 == 0:
        s += 1
        Q = Q // 2

    z = find_non_residue(p)

    t = pow(n, Q, p)
    c = pow(z, Q, p)
    R = pow(n, (Q + 1) // 2, p)
    M = s
    while True:
        if t == 0: return 0
        if t == 1: return R

        ts = t
        mo = M
        for i in range(1, M):
            ts = pow(ts, 2, p)
            if ts == 1:
                mo = i
                break

        b = pow(c, pow(2, M - mo - 1, p), p)
        M = mo
        c = pow(b, 2, p)
        t = (t * c) % p
        R = (R * b) % p

def find_non_residue(p):
    q = (p - 1) // 2
    while True:
        n = random.randint(2, p)
        if pow(n, q, p) == p - 1:
            return n
    return 0

if __name__ == '__main__':
    print ("Testing using P-256 Generator point")
    x = ecc.Curve.G.x
    y = ecc.Curve.G.y

    y_square = ecc.F(x)

    y_sol = quadratic_residue(y_square, ecc.Curve.mod)

    print ("Verified" if y == y_sol else "Solutions don't match !!")
    print ("Curve.G.y : {}".format(y))
    print ("Caluclated: {}".format(y_sol))
