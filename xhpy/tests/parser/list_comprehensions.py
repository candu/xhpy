[x for x in L]
[x for x in L if x]
[(x, x+1) for x in L]
[[(x, y) for x in L1] for y in L2]
[(x, y) for x in L1 for y in L2]
[(x, y) for (x, y) in zip(L1, L2)]
[x for x in L[0]]
[child for child in self._children if isinstance(child, tag_class)]
[x for x in L[0] if x]
# TODO: add support for this syntax
#[x for x in L[0] if (x if f(x) else y)]
(x for x in L)
(x for x in L if x)
((x, x+1) for x in L)
(((x, y) for x in L1) for y in L2)
((x, y) for x in L1 for y in L2)
((x, y) for (x, y) in zip(L1, L2))
(x for x in L[0])
