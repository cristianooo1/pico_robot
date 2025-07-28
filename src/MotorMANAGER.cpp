#include "MotorMANAGER.h"
#include "hardware/pwm.h"
#include "hardware/pio.h"
#include "quadrature_encoder.pio.h"
#include <cmath>



MotorManager::MotorManager(uint8_t pinCW, uint8_t pinCCW, uint8_t pinENCA, uint8_t pinENCB, uint sm, 
    float kp, float ki, float kd): gpCW(pinCW), gpCCW(pinCCW), gpENCA(pinENCA), gpENCB(pinENCB), SM_(sm), pidController(kp, ki, kd) {

    // gpCW = pinCW;
    // gpCCW = pinCCW;
    // gpENCA = pinENCA;
    // gpENCB = pinENCB;
    // SM_ = sm;

    gpio_init(gpCW);
    gpio_init(gpCCW);
    
    gpio_set_dir(gpCW, GPIO_OUT);
    gpio_set_dir(gpCCW, GPIO_OUT);

    gpio_set_function(gpCW, GPIO_FUNC_PWM);
    gpio_set_function(gpCCW, GPIO_FUNC_PWM);
    pwm_set_gpio_level(gpCW, 0);
    pwm_set_gpio_level(gpCCW, 0);
    uint slice_num = pwm_gpio_to_slice_num(gpCW);
    pwm_set_enabled(slice_num, true);
    slice_num = pwm_gpio_to_slice_num(gpCCW);
    pwm_set_enabled(slice_num, true);


    
    const uint PIN_AB = gpENCA;
    pio_add_program(pio, &quadrature_encoder_program);
    quadrature_encoder_program_init(pio, SM_, PIN_AB, 0);

    
}

// MotorManager::~MotorManager() {
//     // Destructor implementation if needed
// }


void MotorManager::set_Throttle(float percent, bool cw){
    if (percent < 0.0f) {
        percent = 0.0f;
    } else if (percent > 1.0f) {
        percent = 1.0f; // Ensure percent does not exceed 100%
    }

    Throttle = percent;
    CW_ = cw;

    if(Throttle <= 0.0f){
        Last_Time = 0;
        pwm_set_gpio_level(gpCW, 0);
        pwm_set_gpio_level(gpCCW, 0);
        return;
    }

    int pwm = (int)((float)(0xffff) * Throttle);
    if (cw){
        pwm_set_gpio_level(gpCW, pwm);
        pwm_set_gpio_level(gpCCW, 0);
    } else {
        pwm_set_gpio_level(gpCCW, pwm);
        pwm_set_gpio_level(gpCW, 0);
    }
}


void MotorManager::update(PIO pio, uint sm){
    uint32_t curr_Value   = quadrature_encoder_get_count(pio, sm);
    uint64_t curr_time_us = time_us_64();

    Delta_Count = (int32_t)(curr_Value - Last_Value);


    float dt_sec = (curr_time_us - Last_Time) * 1e-6f;

    Revolutions = (float)Delta_Count / (float)(2492);

    RPM = Revolutions / dt_sec * 60.0f;

    Last_Value = curr_Value;
    Last_Time = curr_time_us;


}

float MotorManager::get_Revolutions() {
    return Revolutions;
}

float MotorManager::get_delta() {
    return Delta_Count;
}


float MotorManager::get_RPM() {
    return fabs(RPM);
}

float MotorManager::get_RadPerSec() {
    AvgRPM = (RPM + AvgRPM * 3.0f) / 4.0f;
    Omega = (AvgRPM / 60.0f) * (2.0f * 3.14159265358979323846f);
    return Omega;
}

float MotorManager::get_AvgRPM() {
    return AvgRPM;
}

bool MotorManager::get_Direction() {
    return CW_;
}

float MotorManager::get_Throttle() {
    return Throttle;
}

void MotorManager::set_TargetRPM(float target, bool cw) {

    update(pio, SM_);  // This updates RPM internally
    CW_ = cw;
    float currentRPM = fabs(get_RPM());

    OutputThrottle = pidController.compute(target, currentRPM);

    // Apply throttle
    set_Throttle(OutputThrottle, CW_);
}

float MotorManager::get_OutputThrottle() {
    return OutputThrottle;
}

