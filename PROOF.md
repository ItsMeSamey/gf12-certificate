# Identity and failure witnesses

Let V be the 12-dimensional vector space over GF(2), represented by integers 0..4095. Integer bit i is the coefficient of X^i. The fixed polynomial is

`p(X) = X^12 + X^6 + X^4 + X + 1`, encoded by `0x1053`.

A triple `(a,b,c)` denotes the vector-valued map `parity(a & x) * parity(b & y) * c`, where multiplication of the two parity bits is multiplication in GF(2), and scalar multiplication of c selects either zero or c. The certificate denotes the XOR sum of its 42 terms.

Each parity is a linear functional. Each product of one left and one right functional is bilinear, and XOR preserves bilinearity. Ordinary carryless polynomial multiplication is also bilinear. Reduction modulo a fixed monic polynomial is linear, so the reference multiplication M is bilinear as well.

Write x as the sum of x_i e_i and y as the sum of y_j e_j, with e_i = X^i. For the difference D between the certificate map and M,

`D(x,y) = XOR over i,j of x_i * y_j * D(e_i,e_j)`.

Therefore D is identically zero if and only if all 144 basis coefficients are zero. This proves equality for every pair of 12-bit operands. It immediately gives the classical identity `z XOR certificate(x,y) = z XOR M(x,y)` for every classical output word z.

The new reference implementation forms all carryless product coefficients with nested bit loops, then performs descending polynomial long division. Acceptance depends on these independently computed products and the certificate's coefficients. Hashes identify the checked data.

## Fixed-field terminology

The identity proof above works in the quotient ring even before irreducibility is established. To independently establish the field label for this fixed polynomial, it suffices to test every monic binary divisor of degrees 1 through 6: 126 polynomials. Any reducible degree-12 polynomial has a nonconstant factor of degree at most 6. A zero remainder for any candidate would disprove the field claim; absence of such a factor establishes irreducibility. The independent review records this tiny check separately from the certificate tests.

## Frozen semantic corruptions

The retained first two triples are `(321,321,1958)` and `(272,272,2420)`. The first input mask has bits 0, 6 and 8 set. The second has bits 4 and 8 set. These facts establish nonzero tensor differences without running the implementation being tested.

1. Toggle output bit 0 of term 0. At x=1,y=1 both input parities are one, so the map changes by 1. The correct product is 1; the corrupted map must return 0.
2. Toggle left-mask bit 1 of term 0. At x=2,y=1 the new left coefficient changes by one and the right coefficient is one, so the map changes by 1958. The correct product is 2; the corrupted map must return `2 XOR 1958 = 1956`.
3. Replace term 0 with a copy of term 1. At x=1,y=1 the removed term contributes 1958 and the replacement contributes zero. The correct product is 1; the corrupted map must return `1 XOR 1958 = 1959`.

These witness locations are also the first mismatches in the checker's lexicographic left-bit/right-bit order. They are semantic failures of well-formed 42-term inputs. Reversing all 42 terms is an equivalent certificate because XOR is associative and commutative, and must remain accepted. The frozen tests distinguish these behaviors from unsupported metadata or malformed JSON, which are rejected before algebraic checking.

## Boundaries

The proof certifies the classical tensor identity. A circuit can have the correct classical basis output and still introduce unwanted relative phases, retain scratch state, mishandle a measurement branch or have different resource costs. These properties require a separately identified emitter and separate verification. The historical finite-shot receipts establish their recorded cases.

The supported certificate has exactly 42 terms over the specified field. Input bytes are bounded by the fixed schema. Correctness of Python's integer and JSON behavior remains part of the software trusted base, as does the independently inspected checker implementation.
