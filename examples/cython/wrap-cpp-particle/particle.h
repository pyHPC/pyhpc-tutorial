#ifndef _PARTICLE_H_
#define _PARTICLE_H_

#include <cmath>
#include <vector>

    template<typename T>
inline const T norm2(const T x, const T y, const T z)
{
    return sqrt(x * x + y * y + z * z);
}

class Particle 
{
    public:

        Particle() : _x(0), _y(0), _z(0),
        _vx(0), _vy(0), _vz(0),
        _mass(0), _charge(0) {};

        Particle(float x, float y, float z,
                float vx, float vy, float vz,
                float mass, float charge) :
            _x(x), _y(y), _z(z),
            _vx(vx), _vy(vy), _vz(vz),
            _mass(mass), _charge(charge) {};

        const float get_speed() const {
            return norm2(_vx, _vy, _vz);
        }

        const float& get_x() const {
            return _x;
        }

    private:
        float _x, _y, _z;
        float _vx, _vy, _vz;
        float _mass;
        float _charge;
};

#endif
