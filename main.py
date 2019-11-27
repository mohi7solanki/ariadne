from ariadne import Map

m = Map()
m['a.b.c'] = 10
m.a.b.c = 20
m.a.b.d = 30
m.a.z = 15

#print(m.a.z)
#print(m['a'].b['c'])
#print(m.a['b'].c)
#print(m['a.b.c'])
#print(m['a.b/d'])
#m.a.z.d = 45