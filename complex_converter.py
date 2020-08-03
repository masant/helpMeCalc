import cmath
import math

def rect2pol(real,imag,angle):
    z = real + 1j*imag
    z_polar_temp = cmath.polar(z)

    temp = []

    temp.append(z_polar_temp[0])
    
    if (angle):
        temp.append(z_polar_temp[1])
    else:
        temp.append(math.degrees(z_polar_temp[1]))        
    z_polar = temp
    z_polar = tuple(z_polar)

    return z_polar

def pol2rect(r, phi, angle):

    if (angle):
        z_rect = cmath.rect(r,phi)
    else:
        phi = math.radians(phi)
        z_rect = cmath.rect(r,phi)
    
    z_rect = (z_rect.real, z_rect.imag)
    return z_rect