import asn1tools

def xgcd(a, b):
	"""return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
	x0, x1, y0, y1 = 0, 1, 1, 0
	while a != 0:
		q, b, a = b // a, a, b % a
		y0, y1 = y1, y0 - q * y1
		x0, x1 = x1, x0 - q * x1
	return b, x0, y0

def inv(a, m):
	a = a % m
	g, x, _ = xgcd(a, m)
	if g == 1: return x % m

def asn1_marshal(t, filename="data/x.txt"):
    """Marshal the tuple t=(r, s) to ASN1 encoding."""
    r, s = t
    d = {'r': r, 's': s}
    enc = asn1tools.compile_files('core/sg.asn')
    res = enc.encode('Point', d)
    with open(filename, 'wb') as f:
    	f.write(res)
