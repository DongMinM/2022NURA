import numpy as np
from transformer import Transformer
class RocketStatus:
  def __init__(self):
    # 로켓의 헤딩 방향  : x / roll
    # 로켓의 앞쪽       : y / pitch
    # 로켓의 오른쪽     : z / yaw

    # 아래의 변수는 (x,y,z) 또는 (roll, pitch, yaw) 순서.

    # (rocket)x,y,z
    self.length   = 1.3                           # m
    self.diameter = 0.09                          # m

    self.massCenter = 0.6                         # m from bottom
    self.aeroCenter = 0.45                        # m from bottom

    self.position     = np.array([0,0,0])         # m 
    self.velocity     = np.array([0,0,0])         # m/s
    self.acceleration = np.array([0,0,0])         # m/s^2

    self.angle               = np.array([0,0,0])*np.pi/180  # ras
    self.angulerVelocity     = np.array([0,0,0])*np.pi/180   # rad / s
    self.angulerAcceleration = np.array([0,0,0])*np.pi/180   # rad / s^2


    self.theta = np.array([60])*np.pi/180

    # 롤축(x축)으로부터의 각도
    self.phi = np.array([30])*np.pi/180

    rho = self.length - self.massCenter
    self.head = np.array([(rho*np.sin(self.theta)*np.cos(self.phi))[0],
                          (rho*np.sin(self.theta)*np.sin(self.phi))[0],
                          (rho*np.cos(self.theta))[0]])
    self.head = np.around(self.head,10)

    self.thrust   = np.array([100,0,0])                      # x,y,z thrust in rocket inertia frame
    self.burnTime = 3                             # sec

    self.structureMass  = 3                       # kg
    self.propellantMass = 0.5                     # kg
    self.burnratio      = self.propellantMass/self.burnTime


    self.massCenter = 0.6                         # m from bottom
    self.aeroCenter = 0.45                        # m from bottom

    self.dragCoeff  = 0.5