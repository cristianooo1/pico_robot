#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/pwm.h"
#include "hardware/pio.h"
#include "quadrature_encoder.pio.h"
#include "MotorMANAGER.h"
#include "DiffDRIVE.h"
#include "TCP_Server.c"

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

    if (cyw43_arch_init()) {
        printf("Wi-Fi init failed\n");
        return 1;
    }
    cyw43_arch_enable_sta_mode();

    printf("Connecting to Wi-Fi...\n");
    if (cyw43_arch_wifi_connect_timeout_ms(WIFI_SSID, WIFI_PASSWORD,
        CYW43_AUTH_WPA2_AES_PSK, 30 * 1000)) {
        printf("Wi-Fi connect failed\n");
        return 1;
    }
    printf("Connected, IP = %s\n", ip4addr_ntoa(&cyw43_state.netif[0].ip_addr));

    tcp_server_init();
    const uint32_t LOOP_MS = 10;
    float curr_vel = 0.0f, curr_turn = 0.0f;
    uint32_t ms_counter = 0;

    MotorManager left(LEFT_CW_PIN, LEFT_CCW_PIN, LEFT_ENC_A, LEFT_ENC_B, 0, 0.02, 0.03, 0.00);
    MotorManager right(RIGHT_CW_PIN, RIGHT_CCW_PIN, RIGHT_ENC_A, RIGHT_ENC_B, 1, 0.02, 0.03, 0.00);
    DiffDriveKinematics robotul(0.03, 0.2, left, right);
    bool cw = true;
    sleep_ms(1000);
    float thr = 10.0f;
    int ko = 1;

    while(1){
        float vel, turn;

        if (tcp_server_poll(&vel, &turn)) {
            curr_vel = vel;
            curr_turn = turn;}
            
            // printf("Command: forward=%.2f, turn=%.2f\n", vel, turn);
            // if (vel != curr_vel || turn != curr_turn){
            //     robotul.setWheelVelocity(vel, turn);
            // }
        robotul.setWheelVelocity(curr_vel, curr_turn);
        ms_counter += LOOP_MS;
        if (ms_counter > 100){
            ms_counter = 0;
            printf("%s,%.2f,%s,%.2f\n",left.get_Direction() ? "CW" : "CCW", left.get_RadPerSec(), right.get_Direction() ? "CW" : "CCW", right.get_RadPerSec());
        }
        // printf("DIR: %s,R_Thr: %.2f, R_RPM: %.2f, R_RPS: %.2f, R_OutThr: %.2f\n", 
        // right.get_Direction() ? "CW" : "CCW",
        // right.get_Throttle(),
        // right.get_RPM(), 
        // right.get_RadPerSec(),
        // right.get_OutputThrottle());
        // printf("DIR: %s,L_Thr: %.2f, L_RPM: %.2f, L_RPS: %.2f, L_OutThr: %.2f\n", 
        // left.get_Direction() ? "CW" : "CCW",
        // left.get_Throttle(),
        // left.get_RPM(), 
        // left.get_RadPerSec(),
        // left.get_OutputThrottle());
        // ms_counter += LOOP_MS;
        // if(ms_counter > 500){
        //     ms_counter = 0;
        //     tcp_server_send(
        //                     "STATUS,LRPM=%.1f,LDIR=%d,RRPM=%.1f,RDIR=%d", 
        //                     left.get_RadPerSec(), 
        //                     left.get_Direction(), 
        //                     right.get_RadPerSec(), 
        //                     right.get_Direction());
        //     }
        curr_vel = vel;
        curr_turn = turn;
            
        
        // robotul.setWheelVelocity(curr_vel, curr_turn);
        // ms_counter += LOOP_MS;
        // if(ms_counter > 500){
        //     ms_counter = 0;
        //     printf("DIR: %s,R_Thr: %.2f, R_RPM: %.2f, R_RPS: %.2f, R_OutThr: %.2f\n", 
        //     right.get_Direction() ? "CW" : "CCW",
        //     right.get_Throttle(),
        //     right.get_RPM(), 
        //     right.get_RadPerSec(),
        //     right.get_OutputThrottle());
        //     printf("DIR: %s,L_Thr: %.2f, L_RPM: %.2f, L_RPS: %.2f, L_OutThr: %.2f\n", 
        //     left.get_Direction() ? "CW" : "CCW",
        //     left.get_Throttle(),
        //     left.get_RPM(), 
        //     left.get_RadPerSec(),
        //     left.get_OutputThrottle());
            


        // }
        
        
        // robotul.setWheelVelocity(0.0f, -1.5f); // Linear:0.15 m/s = 5rad/s = 48 RPM; Angualr:1.5 rad/s -> 5rad/s per wheel
        
        // printf("DIR: %s,R_Thr: %.2f, R_RPS: %.2f, R_OutThr: %.2f\n", 
        // right.get_Direction() ? "CW" : "CCW",
        // right.get_Throttle(), 
        // right.get_RadPerSec(),
        // right.get_OutputThrottle());
        // printf("DIR: %s,L_Thr: %.2f, L_RPS: %.2f, L_OutThr: %.2f\n", 
        // left.get_Direction() ? "CW" : "CCW",
        // left.get_Throttle(), 
        // left.get_RadPerSec(),
        // left.get_OutputThrottle());
        // ko += 1;
        // printf("THR: %.2f, KO: %d\n", thr, ko);
        // if (ko > 500) {
        //     ko = 1;
        //     thr += 10.0f;
            
        //     if (thr > 52.0f) {
        //         thr = 10.0f;
        //         ko = 1;
        //         cw = !cw;
        //     }
        // }

        sleep_ms(LOOP_MS);
    }
    cyw43_arch_deinit();
    return 0;
}