import numpy as np
from transformer import Transformer
class RocketStatus:
  def __init__(self):
    # 로켓의 헤딩 방향  : x축 / roll
    # 로켓의 앞쪽       : y축 / pitch
    # 로켓의 오른쪽     : z축 / yaw

    # 아래의 변수는 (x,y,z) 또는 (roll, pitch, yaw) 순서.

    # 로켓 길이, 직경
    self.length   = 1.3                           # m
    self.diameter = 0.09                          # m

    # 로켓 무게중심, 공력중심
    self.massCenter = 0.6                         # m from bottom
    self.aeroCenter = 0.45                        # m from bottom

    # 로켓 위치, 속도, 가속도
    self.position     = np.array([0,0,0])         # m 
    self.velocity     = np.array([0,0,0])         # m/s
    self.acceleration = np.array([0,0,0])         # m/s^2

    # 요축(z축)으로부터의 각도
    self.theta = np.array([90])*np.pi/180
    # 롤축(x축)으로부터의 각도
    self.phi = np.array([10])*np.pi/180

    # 무게중심 부터 상단까지의 거리
    rho = self.length - self.massCenter

    # 무게중심 부터 상단까지의 거리 --> 회전각 --> 구면좌표에서 직교좌표로 변환
    self.head = np.array([(rho*np.sin(self.theta)*np.cos(self.phi))[0],
                          (rho*np.sin(self.theta)*np.sin(self.phi))[0],
                          (rho*np.cos(self.theta))[0]])

    # 오차 제어
    self.head = np.around(self.head,10)

    # 피치, 요 계산
    self.pitch = np.arctan2(self.head[1],self.head[0])
    self.yaw   = np.arctan2(self.head[2],self.head[0])

    # 추력, 연소시간
    self.thrust   = np.array([100,0,0])                      # x,y,z thrust in rocket inertia frame
    self.burnTime = 3                             # sec

    # 추력을 ground 벡터로 변환
    self.thrust_ground = Transformer().spherical_to_earth(np.linalg.norm(self.thrust),self.theta,self.phi)

    # 구조체 무게, 추진제 무게, 연소율
    self.structureMass  = 3                       # kg
    self.propellantMass = 0.5                     # kg
    self.burnratio      = self.propellantMass/self.burnTime

    # 항력 계수
    self.dragCoeff  = 0.5