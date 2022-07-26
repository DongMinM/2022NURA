from cmath import nan
import numpy as np
from transformer import Transformer
import random
import time

class Environment:
  def __init__ (self):
    np.random.seed(2)
    # gravity
    self.g     = np.array([9.81,0,0])                # m / s^2
    # self.wind  = np.around(np.random.randn(3),3)
    self.wind = np.array([0,0,0])
    self.Cw = 1
    self.sec_Time = 0

  # Kinematics
  def free_fall(self,rocket,dt):

        ''' Set Parameters'''
        # Thrust
        T = np.linalg.norm(rocket.status.thrust)
        # position and velocity about ground
        p_v = np.append(rocket.status.position,rocket.status.velocity)

        # mass
        m = rocket.status.structureMass + rocket.status.propellantMass
        head = rocket.status.head
        theta = rocket.status.theta
        phi   = rocket.status.phi
        # inertia
        I = np.around(0.5*m*rocket.status.length**2,5)

        # drag coefficient
        Cd = rocket.status.dragCoeff
        # cross section
        S = np.pi*rocket.status.diameter**2/4
        
        # rho
        if p_v[2] <= 35000:
            rho = 1.225*(1-1.8e-5*p_v[2])**5.656                                  ## calculate atmospheric density
        else :
            rho = 0.001

        # Kinematics / X = A@X + B@U / Kinetics / X = A@X + B@U
        ''' |x |      |1, 0, 0, dt ,0 ,0||x |     |0.5*dt**2, 0,           0|
            |y |      |0, 1, 0, 0, dt ,0||y |     |0,         0.5*dt**2,   0||ax|
            |z |  =   |0, 0, 1, 0, 0, dt||z |  +  |0,         0,   0.5*dt**2||ay|
            |Vx|      |0, 0, 0, 1 ,0 ,0 ||Vx|     |dt,        0,           0||az|
            |Vy|      |0, 0, 0, 0, 1 ,0 ||Vy|     |0,         dt,          0|
            |Vz|      |0, 0, 0, 0, 0, 1 ||Vz|     |0,         0,          dt|                                 
            p_v = A@p_v + B@a

        '''
        


        A = np.array([[1, 0, 0, dt ,0 ,0],
                      [0, 1, 0, 0, dt ,0],
                      [0, 0, 1, 0, 0, dt],
                      [0, 0, 0, 1 ,0 ,0],
                      [0, 0, 0, 0, 1 ,0],
                      [0, 0, 0, 0, 0, 1]])
                      
        B = np.array([[0.5*dt**2, 0,         0],
                      [0,         0.5*dt**2, 0],
                      [0,         0,         0.5*dt**2],
                      [dt,        0,         0],
                      [0,         dt,        0],
                      [0,         0,         dt]])

        # Calculate thrust and transform thrust
        T = Transformer().spherical_to_earth(T,theta,phi)
        
        left_rcs = 0
        if rocket.status.position[0] >= 100:
            if rocket.status.pitch*180/np.pi > 0:
                left_rcs = 3
            elif rocket.status.pitch*180/np.pi <-0:
                left_rcs = -3
            else:
                left_rcs = 0

        if rocket.status.position[0] > 100 and rocket.status.velocity[0] < 0 and self.sec_Time == 0:
            T = 100
            T = Transformer().spherical_to_earth(T,theta,phi)
            self.sec_Time += dt
        
        if self.sec_Time != 0:
            T = 20
            T = Transformer().spherical_to_earth(T,theta,phi)
            self.sec_Time += dt

        if self.sec_Time > 10:
            T = np.array([0,0,0])


        l_T = Transformer().spherical_to_earth(left_rcs,theta,phi-0.5*np.pi)
        # l_T = Transformer().quaternions_rotation(head,0.5*np.pi,l_T)

        # Calculate drag and transform drag
        D = -0.5*rho*S*Cd*np.linalg.norm(p_v[3:6])*np.array(p_v[3:6])
        
        # Total force at aerocenter
        total_force_at_ac = D - l_T

        # Calculate total acceleration
        total_accel = (T+D+l_T)/m-self.g

        # State-space equation : Translation
        p_v = A@p_v + B@total_accel

        # Rotation equation
        if not np.array_equal(D,np.array([0,0,0])):

            aoa_normal = np.cross(-1*head,total_force_at_ac)
            aoa_normal = aoa_normal
            rocket.normal = aoa_normal

            total_anguler_accel = np.linalg.norm((total_force_at_ac))*0.15/I  # 방향에 따른 I도 만들어줘야할듯?

            rot_angle = total_anguler_accel*dt

            next_head = Transformer().quaternions_rotation(aoa_normal,rot_angle,head)
            rocket.status.head             = next_head


        if rocket.timeFlow <= 3:
            rocket.status.propellantMass  -= rocket.status.burnratio*dt

        # Update status
        rocket.status.position         = p_v[0:3]
        rocket.status.velocity         = p_v[3:6]
        rocket.status.acceleration     = total_accel

        rocket.totalDrag          = D
        rocket.status.phi         = np.array([np.arctan2(rocket.status.head[1],rocket.status.head[0])])
        rocket.status.theta       = np.array([90*np.pi/180-rocket.status.head[2]/np.linalg.norm(rocket.status.head)])

        if head[0] != 0:
            rocket.status.pitch = np.arctan2(head[1],head[0])
            rocket.status.yaw   = np.arctan2(head[2],head[0])

        rocket.status.thrust_ground             = T
        rocket.rcs.left_thrust    = l_T
        


