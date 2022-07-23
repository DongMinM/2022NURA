from transformer import Transformer

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import axes3d

import numpy as np

class Visualizer:
    def __init__ (self,rocket,simTime,timestep,witch,scale=100):
        print('======Wait for Visualization======')

        if witch == '3d':
            self.animation(rocket,simTime,timestep,scale)
        else:
            self.set_variables(rocket)
            self.set_visualmodel(witch,simTime,timestep)
            self.visualization_start(witch)

    #  Set up
    def set_variables(self,rocket):
        self.Vx = rocket.velocitylist[:,1]
        self.Vy = rocket.velocitylist[:,2]
        self.Vz = rocket.velocitylist[:,0]
        self.V = np.empty(len(rocket.velocitylist))
        for i in range(len(rocket.velocitylist)):
            self.V[i]  = np.linalg.norm(rocket.velocitylist[i])

        self.Ax = rocket.accellist[:,1]
        self.Ay = rocket.accellist[:,2]
        self.Az = rocket.accellist[:,0]
        self.A = np.empty(len(rocket.accellist))
        for i in range(len(rocket.accellist)):
            self.A[i]  = np.linalg.norm(rocket.accellist[i])

        self.roll  = rocket.anglelist[:,0]*180/np.pi
        self.pitch = rocket.anglelist[:,1]*180/np.pi
        self.yaw   = rocket.anglelist[:,2]*180/np.pi

        self.Wx = rocket.angulerVelocitylist[:,0]*180/np.pi
        self.Wy = rocket.angulerVelocitylist[:,1]*180/np.pi
        self.Wz = rocket.angulerVelocitylist[:,2]*180/np.pi

        self.mass = rocket.masslist
        self.thrust = rocket.thrustlist[:,0]
        self.drag   = np.empty(len(rocket.totalDraglist))
        for i in range(len(rocket.totalDraglist)):
            self.drag[i] = np.linalg.norm(rocket.totalDraglist[i])
        self.time = rocket.timeFlowList

        self.landingTime = rocket.landingTime

    #  Set up
    def set_visualmodel(self,witch,simTime,timestep):
        n = len(witch)
        self.witch = witch
        self.simTime = simTime
        self.timestep = timestep

        if n <= 6:
            if n%2 == 0:
                self.row = n/2
                self.col = 2
            else:
                self.row = (n+1)/2
                self.col = 2

        elif n <= 9:
            if n%3 == 0:
                self.row = n/3
                self.col = 3
            else:
                self.row = n//3+1
                self.col = 3

        elif n > 9:
            if n%4 == 0:
                self.row = n/4
                self.col = 4
            else:
                self.row = n//4+1
                self.col = 4

        self.fig = plt.figure(figsize=(min(self.col*4,20),min(self.row*3,12)),facecolor='w')
        self.set_figures(n)

    # Set Common params
    def set_figures(self,n):
        self.ax = [0]*n
        for i in range(n):
            self.ax[i] = self.fig.add_subplot(self.row,self.col,i+1)
            self.ax[i].set_title(self.witch[i])
            self.ax[i].set_xlim(0,self.simTime) 
            self.ax[i].set_xlabel(r'Time $[s]$',fontsize=10) 
            self.ax[i].grid(True)
            self.ax[i].axhline(y=0,ls='--',color='k')
            self.ax[i].axvline(x=self.landingTime,ls='--',color='r')

    # Visualization start
    def visualization_start(self,witch):
        n = len(witch)
        for i in range(n):
            self.set_plot(witch[i],i)
        plt.tight_layout()
        plt.show()

    # plotting
    def set_plot(self,witch,i):
        if   witch == 'Vx':
            self.ax[i].set_ylabel(r'Vx $[m/s]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Vx)-3,max(self.Vx)+10)
            self.ax[i].plot(self.time,self.Vx)
        elif witch == 'Vy':
            self.ax[i].set_ylabel(r'Vy $[m/s]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Vy)-3,max(self.Vy)+10)
            self.ax[i].plot(self.time,self.Vy)
        elif witch == 'Vz':
            self.ax[i].set_ylabel(r'Vz $[m/s]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Vz)-3,max(self.Vz)+10)
            self.ax[i].plot(self.time,self.Vz)
        elif witch == 'V':
            self.ax[i].set_ylabel(r'V $[m/s]$',fontsize=10)
            self.ax[i].set_ylim(0,max(self.V)+10)
            self.ax[i].plot(self.time,self.V)
        elif witch == 'Ax':
            self.ax[i].set_ylabel(r'$A_x [m/s^{2}]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Ax)-3,max(self.Ax)+10)
            self.ax[i].plot(self.time,self.Ax)
        elif witch == 'Ay':
            self.ax[i].set_ylabel(r'$A_y [m/s^{2}]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Ay)-3,max(self.Ay)+10)
            self.ax[i].plot(self.time,self.Ay)
        elif witch == 'Az':
            self.ax[i].set_ylabel(r'$A_z [m/s^{2}]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Az)-3,max(self.Az)+10)
            self.ax[i].plot(self.time,self.Az)
        elif witch == 'A':
            self.ax[i].set_ylabel(r'$A [m/s^{2}]$',fontsize=10)
            self.ax[i].set_ylim(0,max(self.A)+10)
            self.ax[i].plot(self.time,self.A)
        elif witch == 'roll':
            self.ax[i].set_ylabel(r'roll $[degree]$',fontsize=10)
            self.ax[i].set_ylim(min(self.roll)-3,max(self.roll)+3)
            self.ax[i].plot(self.time,self.roll)
        elif witch == 'pitch':
            self.ax[i].set_ylabel(r'pitch $[degree]$',fontsize=10)
            self.ax[i].set_ylim(min(self.pitch)-3,max(self.pitch)+3)
            self.ax[i].plot(self.time,self.pitch)
        elif witch == 'yaw':
            self.ax[i].set_ylabel(r'yaw $[degree]$',fontsize=10)
            self.ax[i].set_ylim(min(self.yaw)-3,max(self.yaw)+3)
            self.ax[i].plot(self.time,self.yaw)
        elif witch == 'Wx':
            self.ax[i].set_ylabel(r'$\omega_x [degree/s]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Wx)-3,max(self.Wx)+3)
            self.ax[i].plot(self.time,self.Wx)
        elif witch == 'Wy':
            self.ax[i].set_ylabel(r'$\omega_y [degree/s]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Wy)-3,max(self.Wy)+3)
            self.ax[i].plot(self.time,self.Wy)
        elif witch == 'Wz':
            self.ax[i].set_ylabel(r'$\omega_z [degree/s]$',fontsize=10)
            self.ax[i].set_ylim(min(self.Wz)-3,max(self.Wz)+3)
            self.ax[i].plot(self.time,self.Wz)
        elif witch == 'Mass':
            self.ax[i].set_ylabel(r'mass $[kg]$',fontsize=10)
            self.ax[i].set_ylim(min(self.mass)*0.9,max(self.mass)*1.1)
            self.ax[i].plot(self.time,self.mass)
        elif witch == 'Thrust':
            self.ax[i].set_ylabel(r'thrust $[N]$',fontsize=10)
            self.ax[i].set_ylim(-3,max(self.thrust)*1.1)
            self.ax[i].plot(self.time,self.thrust)
        elif witch == 'Drag':
            self.ax[i].set_ylabel(r'drag $[N]$',fontsize=10)
            self.ax[i].set_ylim(-3,max(self.drag)*1.1)
            self.ax[i].plot(self.time,self.drag)
        else:
            self.ax[i].text(3.5,0.5,r'$Check$'+' '+ r'$Variable$'+' '+r'$Name$'+f'\n : {witch}',fontsize=15)

    # 3D animation
    def animation(self,rocket,simTime,timestep,time_scale):
        self.rocket = rocket
        self.simTime = simTime
        self.time_scale = time_scale
        self.timestep = timestep*time_scale

        fig = plt.figure()
        self.ax = fig.add_subplot(111,projection='3d')

        animate = animation.FuncAnimation(fig,self.animate, frames = int((simTime)/self.timestep+2), interval=1)
        plt.show()
        # animate.save('Simulation.mp4',fps=20)

    # Set animation
    def animate(self,i):
        index = i*self.time_scale
        if i == int((self.simTime)/self.timestep+1):
            index = len(self.rocket.accellist)-1

        self.ax.clear()
        self.ax.set_xlim(0, 500)
        self.ax.set_ylim(0, 500)
        self.ax.set_zlim(0, 500)
        self.ax.grid(False)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])

        M = Transformer().body_to_earth(self.rocket.anglelist[index,:])
        v = 50*M@[1,0,0]

        mc = self.rocket.positionlist[index,:] + 50*M@[self.rocket.massCenterlist[index],0,0]
        l = mc-v

        self.ax.plot(self.rocket.positionlist[:index,1],self.rocket.positionlist[:index,2],self.rocket.positionlist[:index,0],'b-',label = '1st')   

        self.ax.text(100,100,100,'Time = %.2fs'%(index*self.timestep/self.time_scale))                                                           # plot time
        self.ax.text(100,100,250,'Altitude = %.1fm'%self.rocket.positionlist[index,0])
        self.ax.text(100,100,300,'Apogee = %.1fm'%max(self.rocket.positionlist[:,0]))
        self.ax.text(100,100,200,'Velocity = %.1fm/s'%np.linalg.norm(self.rocket.velocitylist[index]))
        self.ax.text(100,100,150,'Thrust = %.1fN'%self.rocket.thrustlist[index,0])


        return self.ax.quiver(l[1],l[2],l[0],v[1],v[2],v[0], color='k',lw = 2,arrow_length_ratio=0.2) 
     