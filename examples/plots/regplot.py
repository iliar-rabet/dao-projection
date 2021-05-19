# import libraries 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
  
# create random data 
np.random.seed(0) 
x = np.random.randint(0, 10, 10) 
y = x+np.random.normal(0, 1, 10) 
  
print(x)
print(y)
# create regression plot 
ax = sns.lineplot(x, y, ci=90)
plt.show(ax)