import localization as lx

P=lx.Project(mode='2D',solver='LSE')


P.add_anchor('anchore_A',(0,100))
P.add_anchor('anchore_B',(100,100))
P.add_anchor('anchore_C',(100,0))

t,label=P.add_target()

# t.add_measure('anchore_A',50)
# t.add_measure('anchore_B',50)
# t.add_measure('anchore_C',50)

# P.solve()

# Then the target location is:

print(t.loc)

t.add_measure('anchore_A',100)
t.add_measure('anchore_B',0)
t.add_measure('anchore_C',100)

P.solve()
print(t.loc)
