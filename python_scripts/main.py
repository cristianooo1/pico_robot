import time
from secretss import *
from utils.ps4_controller import PS4Controller
from utils.TCP_connection import TCPClient
import apriltag_detection.apt_detection as apd
import cv2


def main():
    # curr_vel = 0.0
    # curr_turn = 0.0
    # controller = PS4Controller()
    # controller.connect()

    # client = TCPClient(host = SERVER_IP, port=PORT, timeout= 5.0)
    # client.connect()

    # while controller.running:
    #     controller.run_controller_loop(controller.handlerr)
    #     # time.sleep(controller.poll_interval)

    #     try:
    #         fwd = float(controller.linear)
    #         turn = float(controller.angular)
    #     except ValueError:
    #         print("invalid numbers, try again")
    #         continue
    #     if (fwd != curr_vel or turn != curr_turn):
    #         client.send_floats(fwd, turn)
    #         curr_vel = fwd
    #         curr_turn = turn
        
    #     # Optionally read response:
    #     # resp = client.receive()
    #     # if resp:
    #     #     print("Received:", resp)
    #     time.sleep(0.1)

    url = PHONE_CAMERA_URL

    cam = cv2.VideoCapture(url)
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    apriltag_detector = apd.get_aptDetector()
    cam_matrix = apd.get_calib_matrix()

    while True:
        ret, frame = cam.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detection = apd.make_detection(apriltag_detector, gray_frame, cam_matrix)
        
        det_frame, t, r = apd.draw_detection(frame, detection)
        cv2.imshow('Detected', det_frame)
        print(f"translation: {t}")
        print(f"rotation: {r}")

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the capture and writer objects
    cam.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()