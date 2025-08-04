import time
from secretss import *
from ps4_controller import PS4Controller
from TCP_connection import TCPClient
# from button_logic import *

def main():
    curr_vel = 0.0
    curr_turn = 0.0
    controller = PS4Controller()
    controller.connect()

    client = TCPClient(host = SERVER_IP, port=PORT, timeout= 5.0)
    client.connect()

    while controller.running:
        controller.run_controller_loop(controller.handlerr)
        # time.sleep(controller.poll_interval)

        try:
            fwd = float(controller.linear)
            turn = float(controller.angular)
        except ValueError:
            print("invalid numbers, try again")
            continue
        if (fwd != curr_vel or turn != curr_turn):
            client.send_floats(fwd, turn)
            curr_vel = fwd
            curr_turn = turn
        time.sleep(0.1)
        # Optionally read response:
        # resp = client.receive()
        # if resp:
        #     print("Received:", resp)

if __name__ == "__main__":
    main()