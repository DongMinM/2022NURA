import numpy as np
import time

class Rocket_launcher:
  def __init__(self,RocketStatus,RCS):
    self.status = RocketStatus
    self.rcs = RCS

    self.timeFlow = 0
    self.landingTime = 0
    self.totalDrag = np.array([0,0,0])
    self.normal    = np.array([0,0,0])

    # Saved datas (for Visualization)
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

  # rocket launcher (in environment)
  def launch(self,environment,timestep = 0.001, simTime = 20):
    self.windlist = np.array([environment.wind])
    print('======start simulation======')
    time.sleep(1)

    while self.timeFlow <= simTime:
      # in burnning
      if self.timeFlow <= self.status.burnTime:
        environment.free_fall(self,timestep)

      # finish burnning
      else :
        self.status.thrust = np.array([0,0,0])

        # finish burnning but still fying
        if self.status.position[0] > 0:
          environment.free_fall(self,timestep)

        # landing
        else :
          if self.landingTime == 0:
            self.landingTime = self.timeFlow
          self.status.velocity  = np.array([0,0,0])
          self.status.acceleration     = np.array([0,0,0])
          self.status.angulerVelocity  = np.array([0,0,0])
          self.totalDrag               = np.array([0,0,0])

      # Save datas for Visualization
      self.saveDatas()
      self.windlist = np.append(self.windlist,np.array([environment.wind]),axis=0)

      # Progress
      if self.timeFlow%2 == 0:
        print("Progress : %.1f%%"%(self.timeFlow/simTime*100))
      self.timeFlow += timestep
      self.timeFlow = np.around(self.timeFlow,5)

    print('======finish simulation======')

  def saveDatas(self):
    self.positionlist = np.append(self.positionlist,np.array([self.status.position]),axis=0)
    self.velocitylist = np.append(self.velocitylist,np.array([self.status.velocity]),axis=0)
    self.accellist    = np.append(self.accellist,np.array([self.status.acceleration]),axis=0)

    self.pitchlist    = np.append(self.pitchlist,np.array([self.status.pitch]),axis=0)
    self.yawlist      = np.append(self.yawlist,np.array([self.status.yaw]),axis=0)

    # self.angulerVelocitylist = np.append(self.angulerVelocitylist,np.array([self.status.angulerVelocity]),axis=0)
    self.masslist            = np.append(self.masslist,np.array([self.status.structureMass + self.status.propellantMass]),axis=0)
    self.massCenterlist      = np.append(self.massCenterlist,np.array([self.status.massCenter]),axis=0)
    self.thrustgroundlist          = np.append(self.thrustgroundlist,np.array([self.status.thrust_ground]),axis=0)
    self.totalDraglist       = np.append(self.totalDraglist,np.array([self.totalDrag]),axis = 0)
    self.thetalist           = np.append(self.thetalist,np.array([self.status.theta]),axis=0)
    self.philist             = np.append(self.philist,np.array([self.status.phi]),axis=0)
    self.headlist            = np.append(self.headlist,np.array([self.status.head]),axis=0)
    self.timeFlowList        = np.append(self.timeFlowList,np.array([self.timeFlow]),axis=0)
    self.normallist              = np.append(self.normallist,np.array([self.normal]),axis=0)

    self.rcsleftlist            = np.append(self.rcsleftlist,np.array([self.rcs.left_thrust]),axis=0)
