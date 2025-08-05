#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "lwip/pbuf.h"
#include "lwip/tcp.h"
#include <stdio.h>
#include <string.h>

// === config ===
#define TCP_PORT      4242
#define RECV_BUF_SZ   256

// === lwIP state ===
static struct tcp_pcb *server_pcb = NULL;
static struct tcp_pcb *client_pcb = NULL;

// === receive buffer & parse state ===
static char recv_buf[RECV_BUF_SZ];
static int  recv_idx = 0;

// === last‐seen command & flag ===
static volatile float last_vel  = 0.0f;
static volatile float last_turn = 0.0f;
static volatile bool  cmd_ready = false;

// err_t tcp_server_send(const char *fmt, ...);
// static err_t on_recv(void *arg, struct tcp_pcb *tpcb, struct pbuf *p, err_t err);
// static err_t on_accept(void *arg, struct tcp_pcb *newpcb, err_t err);
// bool tcp_server_poll(float *out_vel, float *out_turn);
// void tcp_server_init(void);

// Called whenever a full “\n”‑terminated line arrives
static err_t on_recv(void *arg, struct tcp_pcb *tpcb, struct pbuf *p, err_t err) {
    if (!p) {
        // connection closed
        tcp_close(tpcb);
        client_pcb = NULL;
        recv_idx = 0;
        return ERR_OK;
    }

    // copy data
    int to_copy = p->tot_len;
    if (recv_idx + to_copy > RECV_BUF_SZ - 1)
        to_copy = RECV_BUF_SZ - 1 - recv_idx;
    pbuf_copy_partial(p, recv_buf + recv_idx, to_copy, 0);
    recv_idx += to_copy;
    tcp_recved(tpcb, p->tot_len);
    pbuf_free(p);

    // scan for newline
    for (int i = 0; i < recv_idx; i++) {
        if (recv_buf[i] == '\n') {
            recv_buf[i] = '\0';
            float v = 0.0f, t = 0.0f;
            if (sscanf(recv_buf, "VEL,%f,%f", &v, &t) == 2) {
                last_vel  = v;
                last_turn = t;
                cmd_ready = true;
                // printf("Storing cmd: v=%.2f, t=%.2f\n", v, t);
            } else {
                printf("Unknown cmd: '%s'\n", recv_buf);
            }
            // ack
            const char *ack = "ACK\n";
            tcp_write(tpcb, ack, strlen(ack), TCP_WRITE_FLAG_COPY);
            tcp_output(tpcb);

            // shift buffer
            int rem = recv_idx - (i + 1);
            memmove(recv_buf, recv_buf + i + 1, rem);
            recv_idx = rem;
            i = -1;
        }
    }
    return ERR_OK;
}

err_t tcp_server_send(const char *fmt, ...)
{
    if (!client_pcb) {
        // no one to send to
        return ERR_CONN;
    }

    char out_buf[RECV_BUF_SZ];
    va_list args;
    va_start(args, fmt);
    int len = vsnprintf(out_buf, sizeof(out_buf), fmt, args);
    va_end(args);

    if (len <= 0) {
        return ERR_ARG;
    }

    if (len > (int)sizeof(out_buf) - 2) {
        len = sizeof(out_buf) - 2;
    }

    // Append newline if missing
    if (out_buf[len - 1] != '\n') {
        out_buf[len++] = '\n';
        out_buf[len]   = '\0';
    }

    u16_t avail = tcp_sndbuf(client_pcb);
    if (avail < (u16_t)len) {
        // Not enough room at this moment
        return ERR_MEM;
    }

    err_t err = tcp_write(client_pcb, out_buf, len, TCP_WRITE_FLAG_COPY);
    if (err != ERR_OK) return err;
    return tcp_output(client_pcb);
}

// Called when a client connects
static err_t on_accept(void *arg, struct tcp_pcb *newpcb, err_t err) {
    if (err != ERR_OK) return ERR_VAL;
    client_pcb = newpcb;
    printf("Client connected\n");
    tcp_arg(newpcb, NULL);
    tcp_recv(newpcb, on_recv);
    return ERR_OK;
}

// One‐time init; call this before your main loop
void tcp_server_init() {
    server_pcb = tcp_new();
    if (!server_pcb) {
        printf("ERROR: tcp_new()\n");
        return;
    }
    if (tcp_bind(server_pcb, IP_ADDR_ANY, TCP_PORT) != ERR_OK) {
        printf("ERROR: tcp_bind()\n");
        return;
    }
    server_pcb = tcp_listen(server_pcb);
    tcp_accept(server_pcb, on_accept);
    printf("Server listening on port %d\n", TCP_PORT);
}

// Call this every 10 ms in your main loop.
// Returns true if a new command was received since last call.
static bool tcp_server_poll(float *out_vel, float *out_turn) {
    // pump the CYW43/lwIP stack
#if PICO_CYW43_ARCH_POLL
    cyw43_arch_poll();
#else
    // if you don’t want polling, you could use an ISR or thread; 
    // but a 1 ms sleep here is fine.
    sleep_ms(1);
#endif

    if (cmd_ready) {
        *out_vel  = last_vel;
        *out_turn = last_turn;
        cmd_ready = false;
        return true;
    }
    return false;
}

// int main() {
//     stdio_init_all();
//     if (cyw43_arch_init()) {
//         printf("Wi‑Fi init failed\n");
//         return 1;
//     }
//     cyw43_arch_enable_sta_mode();
//     // (… connect to your AP …)

//     tcp_server_init();

//     // your control parameters
//     const uint32_t LOOP_MS = 10;
//     float vel, turn;

//     while (true) {
//         if (tcp_server_poll(&vel, &turn)) {
//             // new command arrived
//             Set_TargetRadPerSec(vel, turn);
//         } else {
//             // no new command — you could hold last values, or stop:
//             // Set_TargetRadPerSec(0, 0);
//         }
//         sleep_ms(LOOP_MS);
//     }

//     return 0;
// }
