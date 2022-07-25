from transformer import Transformer
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

r = np.array([1,0,0])
an = np.array([0,50,50])*np.pi/180
an2 = np.array([0,100,100])*np.pi/180
M = Transformer().body_to_earth(an)
M2 = Transformer().body_to_earth(an2)
r2 = M@r
r3 = M2@r

print(r2)
r = np.array([r])
r2 = np.array([r2])
r3 = np.array([r3])

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_zlim(0, 10)
ax.quiver(0,0,0,r[:,0],r[:,1],r[:,2],color='k',lw = 2,arrow_length_ratio=0.2) 
ax.quiver(0,0,0,r2[:,0],r2[:,1],r2[:,2],color='b',lw = 2,arrow_length_ratio=0.2) 
ax.quiver(0,0,0,r3[:,0],r3[:,1],r3[:,2],color='r',lw = 2,arrow_length_ratio=0.2) 

plt.show()