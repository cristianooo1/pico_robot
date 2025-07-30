#include "MotorPID.h"

PID::PID(float kp, float ki, float kd) : KP_(kp), KI_(ki), KD_(kd), Integral(0.0), Target(0.0), Previous_Error(0.0), LastPIDTime_(0) {}

void PID::reset() {
    Integral = 0.0;
    Previous_Error = 0.0;
    LastPIDTime_ = 0;
}

float PID::compute(float setpoint, float measured) {
    uint64_t now = time_us_64();
    float dt = (LastPIDTime_ > 0) ? (now - LastPIDTime_) * 1e-6 : 0.01;  // default
    LastPIDTime_ = now;

    error = setpoint - measured;
    p = KP_ * error;

    Integral += error*dt;
    Integral = std::clamp(Integral, -35.0f, 35.0f); // Clamp integral to prevent windup
    i = KI_ * Integral;

    d = 0.0;
    if(dt >= 0.0f) {
        float derivative = (error - Previous_Error) / dt;
        d = KD_ * derivative;
    }

    float output = p + i + d;
    // printf("Er: %.2f, P: %.2f, I: %.2f, D: %.2f, Out: %.2f\n", error, p, i, d, output);
    output = std::clamp(output, 0.0f, 1.0f); 
    Previous_Error = error;
    // printf("Er: %.2f, P: %.2f, I: %.2f, D: %.2f, Out: %.2f\n", error, p, i, d, output);
    float last_output = output;

    if (fabs(error) < 2.0f){
        return last_output; // Apply brake if error is negative
    } else {
        return output;
    }
    // return output; // Return the PID output
}

float PID::get_LastPIDTime() {
    return LastPIDTime_;
}

void PID::set_last_pid_time(uint64_t time) {
    LastPIDTime_ = time;
}

float PID::get_p() {
    return p;
}

float PID::get_i() {
    return i;
}

float PID::get_d() {
    return d;
}

float PID::get_error() {
    return error;
}
