from scipy.integrate import quad
import scipy.integrate as integrate

from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
from math import cos, exp, pi

fig, ax = plt.subplots(1, 1)


x_axis=10
Handoff_time=2.5
sigma=5
TL=-90
RSSD=-20
eta=10
v=2
# print(norm.ppf(0.01))
# print(norm.ppf(0.99))
t = np.linspace(0.1, x_axis/v-0.1, 150)
# print(x)
def PA(t):
    return norm.sf((-TL+RSSD-10*eta*np.log10(v*t))/sigma)
def PB(t):
    return norm.sf((-TL+RSSD-10*eta*np.log10(x_axis-v*t))/sigma)
def PH(t):
    return norm.sf(Handoff_time-t)
def loss(t):
    return PB(t)*PH(t) + PA(t)*(1-PH(t))
# PB = lambda t:norm.sf((-TL+RSSD-10*eta*np.log10(v*t))/sigma)
# PA=lambda t:norm.sf((-TL+RSSD-10*eta*np.log10(12-v*t))/sigma)
# PH=lambda t:norm.sf(6-t)
# LOSS= lambda t: PA(t)*PH(t) + PB(t)*(1-PH(t))
# def loss(x):
#     return x

y1=PA(t)
y2=PB(t)
y3=PH(t)
Ploss=loss(t)
# plt.xlabel('Time (s)', fontsize=14) 
# plt.ylabel('Probability', fontsize=14) 

# x = np.linspace(0, x_axis, 150)
# # y1=norm.sf((-TL+RSSD-10*eta*np.log10(2*x))/sigma)
# # y2=norm.sf((-TL+RSSD-10*eta*np.log10(0.5*x))/sigma)

# ax.plot(x, 1-norm.sf((x-x_axis)/sigma),'k.', lw=2, alpha=0.6, label='$P(R_a<T_l)$')


ax.plot(t, y1,'k-', lw=2, alpha=0.6, label='$P(R_b<T_l)$')

ax.plot(t, y2,'r-', lw=2, alpha=0.6, label='$P(R_a<T_l)$')

# ax.plot(t, y2,'b+', lw=2, alpha=0.6, label='$P(R_b<T_l)$')
ax.plot(t, y3,'g.', lw=2, alpha=0.6, label='$P(t_{Handoff}<t)$')
ax.plot(t, Ploss,'k-', lw=2, alpha=0.6, label='$P_{Loss}(t)$')

plt.xlabel('Time (s)', fontsize=14) 
plt.ylabel('Probability', fontsize=14) 


plt.legend(fontsize=14)
plt.show()



# rv = norm(x_axis/2)
# ax.plot(x, rv.pdf(x), 'k-', lw=2, label='$P_{rec}$')



# call quad to integrate f from -2 to 2
# res, err = quad(loss, 0, x_axis)



# ls=[]
# ran = np.linspace(4, 6, 100)
# for k in ran:
#     Handoff_time=k
#     res, err = quad(loss, 0, x_axis)
#     ls.append(res/10.0)

# print(ls)

# plt.xlabel('Mean Handoff Time (s)', fontsize=14) 
# plt.ylabel('Total Probability of Loss', fontsize=14) 

# ax.plot(ran,ls,lw=2, alpha=0.6)
# plt.show()