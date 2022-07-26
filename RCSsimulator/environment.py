from cmath import nan
import numpy as np
from transformer import Transformer
import random
import time

class Environment:
  def __init__ (self):

    # 중력
    self.g     = np.array([9.81,0,0])                # m / s^2

    # 바람
    self.wind = np.array([0,0,0])

    self.sec_Time = 0

  # 낙하
  def free_fall(self,rocket,dt):

        ''' Set Parameters'''

        # 추력 불러오기
        T = np.linalg.norm(rocket.status.thrust)

        # 위치, 속도 불러오기
        p_v = np.append(rocket.status.position,rocket.status.velocity)

        # 질량 불러오기
        m = rocket.status.structureMass + rocket.status.propellantMass
        # 헤드 방향 불러오기
        head = rocket.status.head
        # 구면 좌표 각 불러오기
        theta = rocket.status.theta
        phi   = rocket.status.phi
        # 관성 모멘트 계산
        I = np.around(0.5*m*rocket.status.length**2,5)

        # 항력 계수 불러오기
        Cd = rocket.status.dragCoeff
        # 단면적 계산
        S = np.pi*rocket.status.diameter**2/4
        
        # 대기 밀도 계산
        if p_v[2] <= 35000:
            rho = 1.225*(1-1.8e-5*p_v[2])**5.656                                  ## calculate atmospheric density
        else :
            rho = 0.001

        # 상태 공간 방정식 / X = A@X + B@U
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

        # 추력 구면좌표 -> 직교 좌표 변환
        T = Transformer().spherical_to_earth(T,theta,phi)
        
        # RCS 작동 조건 설정
        left_rcs = 0
        if rocket.status.position[0] >= 100:
            if rocket.status.pitch*180/np.pi > 0:
                left_rcs = 3
            elif rocket.status.pitch*180/np.pi <-0:
                left_rcs = -3
            else:
                left_rcs = 0
        l_T = Transformer().spherical_to_earth(left_rcs,theta,phi-0.5*np.pi)

        # 재점화 설정
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

        # 속도에 의한 항력 계산
        D = -0.5*rho*S*Cd*np.linalg.norm(p_v[3:6])*np.array(p_v[3:6])
        
        # 공력 중심에 작용하는 총 항력(힘o 토크x) 계산
        total_force_at_ac = D - l_T

        # 무게 중심에 작용하는 총 힘 계산
        total_accel = (T+D+l_T)/m-self.g

        # 상태 공간 방정식 (Translation)
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


        # 추진 중 추진제 감소
        if rocket.timeFlow <= rocket.status.burnTime:
            rocket.status.propellantMass  -= rocket.status.burnratio*dt


        # 상태 업데이트
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
        


