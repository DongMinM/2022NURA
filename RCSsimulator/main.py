from Visualization import Visualizer
from environment import Environment
from rocketStatus import RocketStatus
from rcsThruster import RCS
from rocketLauncher import Rocket_launcher


if __name__ == '__main__':

  rocketStatus = RocketStatus()
  rcs_thruster = RCS()
  rocket = Rocket_launcher(rocketStatus, rcs_thruster)

  # Simulation Time (sec)
  simTime = 20
  timestep = 0.01

  # Simulation
  rocket.launch(environment = Environment(),timestep = timestep, simTime = simTime)

  # Visualization
  # which = ['Vx','Vy','Vz','V','Ax','Ay','Az','A','roll','pitch','yaw','','Wx','Wy','Wz','','Mass','Thrust','Drag']
  # which = ['roll','pitch','yaw','Windx','Windy','Windz','Dragx','Dragy','Dragz']
  # which = ['Vx','Vy','Vz','pitch','yaw']
  which = '3d'
  Visualizer(rocket,simTime,timestep,which,scale=10)

  '''
    witch :

     3d

     or

     Vx  Vy  Vz  V
     Ax  Ay  Az  A

     roll pitch yaw
     Wx   Wy   Wz

     Mass Thrust

     Dragx Dragy Dragz Drag

     Windx Windy Windz Wind

     (Everything you choose)

     '''