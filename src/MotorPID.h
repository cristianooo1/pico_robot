#ifndef MOTORPID_H
#define MOTORPID_H

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/pwm.h"
#include <cmath>
#include <algorithm> // For std::clamp

class PID{
public:
    PID(float kp, float ki, float kd);
    // void set_TargetRPM(float target);
    float compute(float setpoint, float measured);
    void reset();
    float get_LastPIDTime();
    void set_last_pid_time(uint64_t time);

    float get_p();
    float get_i();
    float get_d();
    float get_error();

private:
    float KP_;
    float KI_;
    float KD_;
    float Integral = 0.0f;
    float Target = 0.0f;
    float Previous_Error = 0.0f;
    uint64_t LastPIDTime_ = 0;

    float p = 0.0f;
    float i = 0.0f;
    float d = 0.0f;
    float error = 0.0f;
    float MAXBrake = 0.3f; // Max brake percentage

};



#endif // MOTORPID_H