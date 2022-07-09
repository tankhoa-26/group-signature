from cryptomath import EllipticCurve

# NOTE: this file has to be placed one directory above 'cryptomath' in order to run correctly

A = Point(1, 1)
B = Point(2, 5)
C = A + B

print("A: (", A.x, ", ", A.y, ")")
print("B: (", B.x, ", ", B.y, ")")
print("C: (", C.x, ", ", C.y, ")")

