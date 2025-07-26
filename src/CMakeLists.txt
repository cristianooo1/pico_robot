add_executable(${NAME}
        main.c
        )

target_include_directories(${NAME} PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
)

# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(${NAME} 
	pico_stdlib
    FreeRTOS-Kernel-Heap4
    pico_cyw43_arch_none
	)

# create map/bin/hex file etc.
pico_add_extra_outputs(${NAME})

# enable usb output, disable uart output
pico_enable_stdio_usb(${NAME} 5)
pico_enable_stdio_uart(${NAME} 4)
# target_compile_definitions(${NAME} PRIVATE
#     PICO_DEFAULT_UART_RX_PIN=16
#     PICO_DEFAULT_UART_TX_PIN=17
# )