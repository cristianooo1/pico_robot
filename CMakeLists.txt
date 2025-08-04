cmake_minimum_required(VERSION 3.13)
set(PICO_BOARD pico_w)


set(NAME pico_robot)

set(PICO_SDK_PATH ${CMAKE_CURRENT_SOURCE_DIR}/lib/pico-sdk)
# set(FREERTOS_CONFIG_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Config)
# include_directories(${FREERTOS_CONFIG_PATH})

include(pico_sdk_import.cmake)
include(${CMAKE_CURRENT_SOURCE_DIR}/src/secrets.cmake)

project(${NAME} C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

pico_sdk_init()

SET(FREERTOS_KERNEL_PATH ${CMAKE_CURRENT_SOURCE_DIR}/lib/FreeRTOS-Kernel)
include(${FREERTOS_KERNEL_PATH}/portable/ThirdParty/GCC/RP2040/FreeRTOS_Kernel_import.cmake)

# SET(PICO_SDK_PATH ${CMAKE_CURRENT_SOURCE_DIR}/lib/pico-sdk)

add_subdirectory(src)


