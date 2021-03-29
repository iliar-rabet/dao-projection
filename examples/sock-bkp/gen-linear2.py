import numpy as np
for i in np.arange(0,320,1):
    time='{:.2f}'.format(i/10.)
    x='{:.2f}'.format(i/20.)
    print("0 " + time +" "+x+" 3")

for i in np.arange(0,320,1):
    time='{:.2f}'.format(i/10.+ 32) 
    x='{:.2f}'.format(16.0-i/20.)
    print("0 " + time +" "+x+" 3")
