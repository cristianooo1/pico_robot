add_executable(${NAME}
        main.cpp
        MotorMANAGER.cpp
        MotorPID.cpp
        DiffDRIVE.cpp
        TCP_Server.c
        )

target_compile_definitions(${NAME} PRIVATE
        WIFI_SSID="${WIFI_SSID}"
        WIFI_PASSWORD="${WIFI_PASSWORD}"
        )

target_include_directories(${NAME} PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
)

pico_generate_pio_header(${NAME} ${CMAKE_CURRENT_LIST_DIR}/quadrature_encoder.pio)


# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(${NAME} 
	pico_stdlib
    

    pico_cyw43_arch_lwip_threadsafe_background
    # pico_cyw43_arch_lwip_none

    # pico_cyw43_arch_lwip_background

    hardware_pwm
    pico_multicore
    hardware_pio
    FreeRTOS-Kernel-Heap4
	)

# create map/bin/hex file etc.
pico_add_extra_outputs(${NAME})

# enable usb output, disable uart output
pico_enable_stdio_usb(${NAME} 1)
pico_enable_stdio_uart(${NAME} 0)
# target_compile_definitions(${NAME} PRIVATE
#     PICO_DEFAULT_UART_RX_PIN=16
#     PICO_DEFAULT_UART_TX_PIN=17
# )