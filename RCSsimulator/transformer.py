import numpy as np

class Transformer:
  def __init___(self):
      pass

  def spherical_to_earth(self, rho, theta, phi):

    earth_pos = np.array([(rho*np.sin(theta[0])*np.cos(phi[0])),
                          (rho*np.sin(theta[0])*np.sin(phi[0])),
                          (rho*np.cos(theta[0]))])

    return earth_pos

  def quaternions_rotation(self,v,angle,p):
    qx = v[0]*np.sin(angle/2)
    qy = v[1]*np.sin(angle/2)
    qz = v[2]*np.sin(angle/2)
    qw = 1*np.cos(angle/2)
    p = np.append(p,[1])
    
    M = np.array([[1-2*(qy**2+qz**2),    2*(qx*qy-qw*qz),      2*(qx*qz+qw*qy),0],
                  [   2*(qx*qy+qw*qz), 1-2*(qx**2+qz**2),      2*(qy*qz-qw*qx),0],
                  [   2*(qx*qz-qw*qy),    2*(qy*qz+qw*qx),   1-2*(qx**2+qy**2),0],
                  [0,0,0,1]])

    return np.dot(M,p)[:3]