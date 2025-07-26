#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
// #include "MotorManager.h"

#define LEFT_ENC_A 27
#define LEFT_ENC_B 28 

uint8_t RotEncCW[4] = {2, 0, 3, 1};
uint8_t RotEncCCW[4] = {1, 3, 0, 2};

int16_t Pos = 0;
int32_t DeltaPos = 0;

uint16_t NumTicks=632;

uint8_t Last=0;

int8_t Count=0;

uint32_t LastTime = 0;

uint8_t c;

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
            Count = 0;
        }
        Last = c;
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

    while (1){
        // tight_loop_contents(); 
        printf("is this on?\n");
        printf("ticks:%d, Pos:%d, Count:%d, DeltaPos:%d\n", NumTicks,Pos, Count, DeltaPos);
        sleep_ms(100);
    }

    return 0;
}