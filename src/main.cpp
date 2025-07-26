#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/pwm.h"
// #include "MotorManager.h"

#define LEFT_ENC_A 27
#define LEFT_ENC_B 28 
#define CW_PIN 19
#define CCW_PIN 26

uint8_t RotEncCW[4] = {2, 0, 3, 1};
uint8_t RotEncCCW[4] = {1, 3, 0, 2};

int16_t Pos = 0;
int32_t DeltaPos = 0;

uint16_t NumTicks=632;

uint8_t Last=0;

int8_t Count=0;

uint32_t LastTime = 0;

uint8_t c;

bool CW_ = true;

float ActRPM = 0.0;
float Throttle = 0.0;
float MvAvgRPM = 0.0;



void get_rpm(bool cw){
    uint32_t now = to_ms_since_boot (get_absolute_time());
    if (LastTime != 0){
        uint32_t ms = now - LastTime;
        float rpm = 60000.0 / (float)ms;
        rpm = rpm / (float)NumTicks;
        ActRPM = rpm;
        MvAvgRPM = (rpm * 1.0 + MvAvgRPM * 3.0) / 4.0; 
    }
    LastTime = now;
}

float get_ActRPM(){
    uint32_t now = to_ms_since_boot(get_absolute_time());
    uint32_t ms = now - LastTime;
    if (ms > 250){
        ActRPM = 0.0;
    }
    return ActRPM;
}

float get_MvAvgRPM(){
    if (get_ActRPM() == 0.0){
        MvAvgRPM = 0.0;
    }
    return MvAvgRPM;
}

float get_RadPerSec(){
    float rpm = get_MvAvgRPM();
    float rps = (rpm / 60.0) * (2.0 * 3.14159265358979323846);
    return rps;
}

void encoder_callback(uint gpio, uint32_t events) {
    c = gpio_get(LEFT_ENC_A);
    c = c << 1;
    c = (gpio_get(LEFT_ENC_B)) | c;
    
    if (RotEncCW[Last] == c){
        Count++;
        if (Count > 3){
            Pos++;
            DeltaPos++;
            if (Pos == NumTicks){
                Pos = 0;
            }
            // printf("CW %d %d\n", Pos, Count);
            get_rpm(true);
            Count = 0;
        }
        Last = c;
    }

    if (RotEncCCW[Last] == c){
        Count--;
        if (Count < -3){
            Pos--;
            DeltaPos--;
            if (Pos == -1){
                Pos = NumTicks - 1;
            }
            // printf("CCW %d %d\n", Pos, Count);
            get_rpm(false);
            Count = 0;
        }
        Last = c;
    }
    
    
}

void set_Throttle(float percent, bool cw){
    Throttle = percent;
    CW_ = cw;
    
    if (Throttle < 0.0){
        Throttle = 0.0;
    }

    if(Throttle == 0.0){
        ActRPM = 0.0;
        LastTime = 0;
        pwm_set_gpio_level(CW_PIN, 0);
        pwm_set_gpio_level(CCW_PIN, 0);
    }

    int pwm = (int)((float)(0xffff) * Throttle);
    if (cw){
        pwm_set_gpio_level(CW_PIN, pwm);
        pwm_set_gpio_level(CCW_PIN, 0);
    } else {
        pwm_set_gpio_level(CCW_PIN, pwm);
        pwm_set_gpio_level(CW_PIN, 0);
    }
}

int main(void) 
{
    stdio_init_all();
    sleep_ms(2000);
    printf("Starting, Testing, VAMOOOOOOOS\n");

    gpio_init(LEFT_ENC_A);
    gpio_set_dir(LEFT_ENC_A, GPIO_IN);
    // gpio_pull_up(LEFT_ENC_A);

    gpio_init(LEFT_ENC_B);
    gpio_set_dir(LEFT_ENC_B, GPIO_IN);
    // gpio_pull_up(LEFT_ENC_B);

    gpio_set_irq_enabled_with_callback(LEFT_ENC_A, GPIO_IRQ_EDGE_FALL | GPIO_IRQ_EDGE_RISE, true, encoder_callback);
    gpio_set_irq_enabled_with_callback(LEFT_ENC_B, GPIO_IRQ_EDGE_FALL | GPIO_IRQ_EDGE_RISE, true, encoder_callback);

    gpio_init(CW_PIN);
    gpio_set_function(CW_PIN, GPIO_FUNC_PWM);
    pwm_set_gpio_level(CW_PIN, 0);
    uint slice_num = pwm_gpio_to_slice_num(CW_PIN);
    pwm_set_enabled(slice_num, true);

    gpio_init(CCW_PIN);
    gpio_set_function(CCW_PIN, GPIO_FUNC_PWM);
    pwm_set_gpio_level(CCW_PIN, 0);
    slice_num = pwm_gpio_to_slice_num(CCW_PIN);
    pwm_set_enabled(slice_num, true);

    bool cw = true;
    while (1){
        // tight_loop_contents(); 
        // printf("is this on?\n");
        // printf("ticks:%d, Pos:%d, Count:%d, DeltaPos:%d\n", NumTicks,Pos, Count, DeltaPos);
        // printf("ActRPM:%.2f, MvAvgRPM:%.2f, RadPerSec:%.2f\n", get_ActRPM(), get_MvAvgRPM(), get_RadPerSec());
        // sleep_ms(100);
        for (float t = 0.3; t <= 1.0; t += 0.1) {
            printf("Setting Throttle to %.2f\n", t);
            set_Throttle(t, cw);
            for(int i = 0; i < 20; i++) {
                printf("ActRPM: %.2f, MvAvgRPM: %.2f, RadPerSec: %.2f\n", get_ActRPM(), get_MvAvgRPM(), get_RadPerSec());
                sleep_ms(500);
            }
            
        }
        cw = !cw; 
    }

    return 0;
}