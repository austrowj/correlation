from numpy import zeros, ones, convolve

def triangle(wsize, total_size):
  if wsize<=total_size/2:
    thetaT = zeros(int(total_size/2)+1)
    thetaT[:int(wsize)] = 1.0
    z = convolve(thetaT[::-1], thetaT)
  else:
    thetaT = ones(int(wsize)+1)
    z = convolve(thetaT[::-1], thetaT)
    z = z[int(wsize-total_size/2):int(2*wsize-total_size/2)+1]
  return z

def square(wsize, total_size):
  phiT = zeros(total_size)
  phiT[int(total_size/2)-wsize:int(total_size/2)+1+wsize]=1.0
  return phiT
