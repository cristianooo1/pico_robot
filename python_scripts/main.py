import time
from secretss import *
from utils.ps4_controller import PS4Controller
from utils.TCP_connection import TCPClient
import apriltag_detection.apt_detection as apd
import cv2
import numpy as np


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

    url = PHONE_CAMERA_URL_IPWEB

    cam = cv2.VideoCapture(url)
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    apriltag_detector = apd.make_aptDetector()
    cam_matrix = apd.get_calib_matrix()
    prev_dist = 0.0

    while True:
        ret, frame = cam.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tags = apd.detect_Tags(apriltag_detector, gray_frame, cam_matrix)
        detection = tags
        
        det_frame = apd.draw_detection(frame, detection)
        cv2.imshow('Detected', det_frame)
        # cv2.imshow('Detected', gray_frame)
        
        # try:
        #     print(tags[15].tag_id, np.array(tags[15].pose_t).reshape(3))
        # except Exception as e:
        #     pass

        # print(frame_width, frame_height)
        
        try:
            if(tags[15].pose_t is not None and tags[14].pose_t is not None):
                dx, dy, dist = apd.distance_between_tags(tags[15], tags[14])
                if abs(dist - prev_dist) > 0.05:
                    prev_dist = dist
                print(prev_dist)
        except Exception as e:
            pass    
        
        
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the capture and writer objects
    cam.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()