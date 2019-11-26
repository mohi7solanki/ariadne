from ariadne import Map

x = Map()
y = Map({'a':{'b':1}})

x.b.c = 10
print(y.a)

#p1 = PathMap()
#p1['a'] = 1
#p2 = PathMap()
#p2['b'] = 2



