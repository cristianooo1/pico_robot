#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/pwm.h"
#include "hardware/pio.h"
#include "quadrature_encoder.pio.h"
#include "MotorMANAGER.h"

#define LEFT_CW_PIN 26
#define LEFT_CCW_PIN 19
#define LEFT_ENC_A 27
#define LEFT_ENC_B 28 

#define RIGHT_CW_PIN 21
#define RIGHT_CCW_PIN 20
#define RIGHT_ENC_A 16
#define RIGHT_ENC_B 17

int main(void){
    stdio_init_all();
    sleep_ms(2000);
    printf("Starting, Testing, VAMOOOOOOOS\n");
    
    MotorManager left(LEFT_CW_PIN, LEFT_CCW_PIN, LEFT_ENC_A, LEFT_ENC_B, 0, 0.02, 0.03, 0.00);
    MotorManager right(RIGHT_CW_PIN, RIGHT_CCW_PIN, RIGHT_ENC_A, RIGHT_ENC_B, 1, 0.02, 0.03, 0.00);
    bool cw = true;
    sleep_ms(1000);
    float thr = 10.0f;
    int ko = 1;
    while(1){
        left.set_TargetRPM(thr, cw);
        right.set_TargetRPM(thr, cw);
        // printf("LEFTThrottle: %.2f, LEFTRPM: %.2f, LEFTDelta: %.2f, LEFTAvgRPM: %.2f, LEFTOmega: %.2f\n", 
        // left.get_Throttle(), 
        // left.get_RPM(),
        // left.get_delta(),
        // left.get_AvgRPM(), 
        // left.get_RadPerSec());
        printf("DIR: %s,R_Thr: %.2f, R_Revo: %.2f, R_RPM: %.2f, R_OutThr: %.2f\n", 
        right.get_Direction() ? "CW" : "CCW",
        right.get_Throttle(), 
        right.get_Revolutions(),
        right.get_RPM(),
        right.get_OutputThrottle());
        printf("DIR: %s,L_Thr: %.2f, L_Revo: %.2f, L_RPM: %.2f, L_OutThr: %.2f\n", 
        left.get_Direction() ? "CW" : "CCW",
        left.get_Throttle(), 
        left.get_Revolutions(),
        left.get_RPM(),
        left.get_OutputThrottle());
        ko += 1;
        printf("THR: %.2f, KO: %d\n", thr, ko);
        if (ko > 500) {
            ko = 1;
            thr += 10.0f;
            
            if (thr > 52.0f) {
                thr = 10.0f;
                ko = 1;
                cw = !cw;
            }
        }

        sleep_ms(10);
    }
    


    // while(1){
    //     for (float i = 0.3; i <= 1.0; i += 0.1){
    //         left.set_Throttle(i, cw);
    //         right.set_Throttle(i, !cw);
    //         for(int j = 0; j < 20; j++){
    //             left.update(pio0, 0);
    //             right.update(pio0, 1);
    //             printf("LEFTThrottle: %.2f, LEFTRPM: %.2f, LEFTAvgRPM: %.2f, LEFTOmega: %.2f\n", 
    //             left.get_Throttle(), 
    //             left.get_RPM(),
    //             left.get_AvgRPM(), 
    //             left.get_RadPerSec());
    //             printf("RIGHTThrottle: %.2f, RIGHTRPM: %.2f, RIGHTAvgRPM: %.2f, RIGHTOmega: %.2f\n", 
    //             right.get_Throttle(), 
    //             right.get_RPM(),
    //             right.get_AvgRPM(), 
    //             right.get_RadPerSec());

    //             sleep_ms(500);
    //         }
            
    //     }
    //     cw = !cw; // Toggle direction
    // }

    return 0;
}