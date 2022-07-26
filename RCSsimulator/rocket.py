import numpy as np
import time

class Rocket:
  def __init__(self,RocketStatus,RCS):
    self.status = RocketStatus
    self.rcs = RCS

    self.timeFlow = 0
    self.landingTime = 0
    self.totalDrag = np.array([0,0,0])
    self.normal    = np.array([0,0,0])

    # 시각화를 위한 변수 저장소
    self.positionlist = np.array([self.status.position])
    self.velocitylist = np.array([self.status.velocity])
    self.accellist    = np.array([self.status.acceleration])
    self.pitchlist    = np.array([self.status.pitch])
    self.yawlist      = np.array([self.status.yaw])

    self.masslist            = np.array([self.status.structureMass + self.status.propellantMass])
    self.massCenterlist      = np.array([self.status.massCenter])
    self.thrustgroundlist          = np.array([self.status.thrust_ground])
    self.totalDraglist       = np.array([self.totalDrag])
    self.thetalist           = np.array([self.status.theta])
    self.philist             = np.array([self.status.phi])
    self.headlist            = np.array([self.status.head])
    self.timeFlowList            = np.array([0])

    self.rcsleftlist            = np.array([self.rcs.left_thrust])

    self.normallist    = np.array([[0,0,0]])

  # 발사 ( 계산 시작 )
  def launch(self,environment,timestep = 0.001, simTime = 20):
    print('======start simulation======')
    time.sleep(1)

    # 시뮬레이션 시간 동안만 계산
    while self.timeFlow <= simTime:

      # 연소 중엔 추력 OK (status에 있음)
      if self.timeFlow <= self.status.burnTime:
        environment.free_fall(self,timestep)

      # 연소 후엔 추력 0
      else :
        self.status.thrust = np.array([0,0,0])

        # 연소 후 공중에 있는 경우 
        if self.status.position[0] > 0:
          environment.free_fall(self,timestep)

        # 연소 후 지면에 도착
        else :
          # 랜딩 타임 계산
          if self.landingTime == 0:
            self.landingTime = self.timeFlow
          # 로켓 정지
          self.status.velocity  = np.array([0,0,0])
          self.status.acceleration     = np.array([0,0,0])
          self.status.angulerVelocity  = np.array([0,0,0])
          self.totalDrag               = np.array([0,0,0])

      # 변수 저장
      self.saveDatas()

      # 진행도 표시
      if self.timeFlow%2 == 0:
        print("Progress : %.1f%%"%(self.timeFlow/simTime*100))
      
      # 시간 흐름
      self.timeFlow += timestep
      self.timeFlow = np.around(self.timeFlow,5)

    print('======finish simulation======')

  # 변수 저장하는 함수
  def saveDatas(self):
    self.positionlist = np.append(self.positionlist,np.array([self.status.position]),axis=0)
    self.velocitylist = np.append(self.velocitylist,np.array([self.status.velocity]),axis=0)
    self.accellist    = np.append(self.accellist,np.array([self.status.acceleration]),axis=0)

    self.pitchlist    = np.append(self.pitchlist,np.array([self.status.pitch]),axis=0)
    self.yawlist      = np.append(self.yawlist,np.array([self.status.yaw]),axis=0)

    # self.angulerVelocitylist = np.append(self.angulerVelocitylist,np.array([self.status.angulerVelocity]),axis=0)
    self.masslist            = np.append(self.masslist,np.array([self.status.structureMass + self.status.propellantMass]),axis=0)
    self.massCenterlist      = np.append(self.massCenterlist,np.array([self.status.massCenter]),axis=0)
    self.thrustgroundlist    = np.append(self.thrustgroundlist,np.array([self.status.thrust_ground]),axis=0)
    self.totalDraglist       = np.append(self.totalDraglist,np.array([self.totalDrag]),axis = 0)
    self.thetalist           = np.append(self.thetalist,np.array([self.status.theta]),axis=0)
    self.philist             = np.append(self.philist,np.array([self.status.phi]),axis=0)
    self.headlist            = np.append(self.headlist,np.array([self.status.head]),axis=0)
    self.timeFlowList        = np.append(self.timeFlowList,np.array([self.timeFlow]),axis=0)
    self.normallist          = np.append(self.normallist,np.array([self.normal]),axis=0)

    self.rcsleftlist         = np.append(self.rcsleftlist,np.array([self.rcs.left_thrust]),axis=0)
