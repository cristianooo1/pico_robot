# Pico Robot 
The project represents my personal attempt to bring a differential drive mobile robot to life, focusing on a Raspberry Pi Pico microcontroller as its brain. The low-level logic (differential drive controller) is written in C++ (with C headers), while additional features are implemented in Python.

# Project Features
- 🥧 Built on Pico SDK C++ for hardware control
- 🔧 CMake build system for Pico cross-compilation and flashing
- ⚡ PIO-based motor encoder reading for position feedback
- 🎛️ MotorManager class for dual motor coordination (adapted after [this](https://github.com/jondurrant/DDD-Exp))
- 🎯 Custom PID controller for smooth speed regulation
- 🤖 Differential drive kinematics for motion control
- 🌐 TCP server hosted on Pico for wireless commands
- 📡 Python client for velocity command transmission
- 🎮 PS4 controller integration for teleoperation (made use of this library [this](https://github.com/piborg/Gamepad/tree/016628623078f0efb8b366c59d83a841827c21c6))
- 👁️ AprilTag detection for autonomous navigation (in works)
##
# Demo
  to be added
##

# Hardware 🔨
- **Chassis & Drive**  
  - 2× 65mm Wheels
  - 2x 100RPM DC Gear Motors  
  - 1x Motor driver board (**TB6612FNG**)  
- **Board**  
  - Raspberry Pi Pico W
  - Custom PCB board

Electrical schematic:
<img width="1392" height="807" alt="Electrical_schematic" src="https://github.com/user-attachments/assets/fc5d7038-79b6-4b46-afbd-1d9a569c9a41" />



##

# Project structure 📂

### pico_robot/
### ├── src/    
 -------└── # C++ source files (.cpp/.h) for robot classes and CMakeLists.txt for build configuration 


### ├── python_scripts/            

-------└── apriltag_detection/       ------- # AprilTag detection and pose estimation for autonomous navigation       

-------└── utils/   ------- #  Joystick input handling and TCP velocity command transmission

   
### ├── lib/      
-------└── # External libraries and submodules for project dependencies         
##
  
# How to run the software (Linux) 🕹
1) Clone the repo, build the project with CMake, and flash the Pico by copying the generated **.uf2** file to the Pico in BOOTSEL mode.
```bash
git clone https://github.com/cristianooo1/pico_robot.git
cd ~/pico_robot
mkdir build
cd build
cmake ..
make
```
For the TCP server to work on your local network, you need to manually create a secrets.cmake file containing your WiFi credentials. 
```bash
cd ~/pico_robot/src
touch secrets.cmake
echo 'set(WIFI_SSID "XXXXX")' > secrets.cmake
echo 'set(WIFI_PASSWORD "XXXXX")' >> secrets.cmake
```
2) To use any of the Python applications, navigate to the **/python_scripts** folder and run the **main.py** script. The project is managed using UV.
```bash
cd ~/pico_robot/python_scripts
uv run main.py
```
To send commands wirelessly to the TCP server hosted on the Raspberry Pi Pico, create a **secretss.py** file containing the IP address and port displayed on your Pico's serial output.
```bash
cd ~/pico_robot/python_scripts
touch secretss.py
echo 'SERVER_IP = "X.X.X.X" ' > secretss.py
echo 'PORT=XXXX' >> secretss.py
```
Additionally, you can run any individual script from the **/python_scripts** folder:
```bash
cd ~/pico_robot/python_scripts
uv run path/to/script.py
```
##
# ToDo List
- A lot
 
👻 This is my second major project and represents my personal learning journey in robotics. There's always room for improvement, and I welcome feedback and contributions from the community!
