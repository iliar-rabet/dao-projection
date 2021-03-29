from __future__ import division
import matplotlib.pyplot as plt


s2=[248,394, 438, 378, 397,  264,  573,  315, 1723] #RP-1000
r2=[248, 394, 437,  378, 396,  264, 571, 315, 1721]

s3=[ 57, 115, 171,  225,  284,  330,  348,  572, 1348] #RP-500
r3=[57, 115,  171, 225,  284,  322,  342, 569, 1314]

# s1=[29, 58, 82, 104,  119, 150, 171,  156,  995]
# r1=[29, 58, 81, 97,  113, 142, 169, 152, 968]


# s1=[59, 118,  176, 468, 1, 519, 6, 128, 123]
# r1=[59, 118,  175, 468, 1, 454, 6, 78, 30]

s1=[59,  100, 96, 245, 94, 112, 949] #RPL-500
r1=[58,  95, 92, 211, 74, 59,  479]

s4=[29,  59, 87, 104,110, 125, 197, 319] #RPL 1000
r4=[29,  59, 85, 90,  96, 99, 149,  185]


rpl1=[]
rpl500=[]
proj500=[]
proj1=[]


barWidth=0.2
end=6
x=range(end)
x1 = [1+i  for i in range(end)]
x2 = [1+i + barWidth for i in range(end)]
x3 = [1+i + barWidth*2 for i in range(end)]
x4 = [1+i + barWidth*3 for i in range(end)]

for i in x:
    rpl500.append(r1[i]/s1[i]*100)
    rpl1.append(r4[i]/s4[i]*100)
    proj1.append(r2[i]/s2[i]*100)
    proj500.append(r3[i]/s3[i]*100)

colors = iter([plt.cm.tab20(i) for i in range(20)])
next(colors)
next(colors)


plt.ylabel('PDR (percent)', fontweight ='bold') 
plt.xlabel('Number of Active Flows', fontweight ='bold') 
plt.bar(x1, rpl1,label='RPL low traffic',width=barWidth,color=[next(colors)],edgecolor='black',hatch = '/')


plt.bar(x2, rpl500,label='RPL high traffic',width=barWidth,color=[next(colors)],edgecolor='black',hatch = '-')



plt.bar(x3, proj1,label='RPL-RP low traffic',width=barWidth,color=[next(colors)],edgecolor='black',hatch = 'x')


plt.bar(x4, proj500,label='RPL-RP high traffic',width=barWidth,color=[next(colors)],edgecolor='black')


plt.gca().set_ylim([40,120])
plt.legend(ncol=2)

plt.show()