from ariadne import PathMap

m = PathMap()
m['a.b.c'] = 10
print(m.a.b.c)
print(m.a)
m.a.__delitem__('b.c')
del m.a.b.c
del m.a
print(m)

#p1 = PathMap()
#p1['a'] = 1
#p2 = PathMap()
#p2['b'] = 2



