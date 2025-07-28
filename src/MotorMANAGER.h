#ifndef MOTOR_MANAGER_H
#define MOTOR_MANAGER_H

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/pwm.h"
#include "hardware/pio.h"
#include "quadrature_encoder.pio.h"
#include "MotorPID.h"

#define EDGES_PER_REV 2492

class MotorManager {
    public:
        MotorManager(uint8_t pinCW, uint8_t pinCCW, uint8_t pinENCA, uint8_t pinENCB, uint sm, 
                    float kp=1.0, float ki=0.0, float kd=0.0);

        // virtual ~MotorManager();

        void set_Throttle(float percent, bool cw);
        float get_Throttle();
        bool get_Direction();
        
        void update(PIO pio, uint sm);
        float get_RPM();
        float get_AvgRPM();
        float get_RadPerSec();
        float get_delta();
        void set_TargetRPM(float target, bool cw);

        float get_Revolutions();
        float get_OutputThrottle();
        
    private:
        uint8_t gpCW;
        uint8_t gpCCW;
        uint8_t gpENCA;
        uint8_t gpENCB;

        PIO pio = pio0;
        uint SM_;
        int32_t Delta_Count = 0;

        uint64_t Last_Time=0;
        uint32_t Last_Value=0;

        float Throttle = 0.0f;

        float RPM = 0.0f;
        float AvgRPM = 0.0f;
        float Omega = 0.0f;
        float Revolutions = 0.0f;
        float OutputThrottle = 0.0f;

        
        PID pidController;
        
        
    protected:
        bool CW_ = true;
};




#endif // MOTOR_MANAGER_H