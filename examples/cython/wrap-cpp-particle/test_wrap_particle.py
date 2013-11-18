import wrap_particle
import numpy as np

assert np.allclose(wrap_particle.norm2(1, 2, 3), np.sqrt(14.0))

args = [0] * 8

p = wrap_particle.Particle(*args)
p1 = wrap_particle.Particle(*args)
print "p.get_x():", p.get_x()

class subparticle(wrap_particle.Particle):
    def get_x(self):
        return super(subparticle, self).get_x() + 10.
    
subp = subparticle(*args)
print "subparticle.get_x():", subp.get_x()
