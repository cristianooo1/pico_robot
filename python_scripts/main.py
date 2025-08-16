import time
import cv2
import numpy as np
import threading
import math
import sys

sys.path.insert(0, "/home/cristianooo/pico_robot/lib/hand_tracking/ai")
import hand_tracking as ht


from secretss import *
from utils.ps4_controller import PS4Controller
from utils.TCP_connection import TCPClient
import apriltag_detection.apt_navigation as apd_nav
import apriltag_detection.apt_detection as apd
# import lib.hand_tracking as ht 

ROBOT_TAG_ID = 13

def controller_thread():
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
        
        # Optionally read response:
        # resp = client.receive()
        # if resp:
        #     print("Received:", resp)
        time.sleep(0.1)

def autonomous_rotation_loop(direction, tcp_client):
    url = PHONE_CAMERA_URL_IPWEB

    # cam = cv2.VideoCapture(url)
    cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    apriltag_detector = apd.make_aptDetector()
    cam_matrix = apd.get_calib_matrix()

    curr_lin = 0.0
    curr_ang = 0.0

    while True:
        ret, frame = cam.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tags = apd.detect_Tags(apriltag_detector, gray_frame, cam_matrix)
        detection = tags
        
        det_frame = apd.draw_detection(frame, detection)
        cv2.imshow('Detected', det_frame)
        if cv2.waitKey(1) == ord('q'):
            break

        if ROBOT_TAG_ID in tags:
            pose_R = tags[ROBOT_TAG_ID].pose_R
            fwd, turn, error = apd_nav.rotate_robot_toNEW(direction, pose_R) #last version with constant speed
            print(f"Forward: {fwd}, Turn: {turn}, Error: {error}")

            if (fwd != curr_lin or turn != curr_ang):
                tcp_client.send_floats(fwd, turn)
                curr_lin = fwd
                curr_ang = turn

        else:
            tcp_client.send_floats(0.0, 0.0)
            curr_lin = 0.0
            curr_ang = 0.0

        time.sleep(0.01)

    cam.release()
    cv2.destroyAllWindows()

def autonomous_get_to_point(tcp_client, target_point, cam, xy_threshold = 0.05, yaw_threshold_deg = 5, lin = 0.15, ang = 0.4):
    if cam is None or not cam.isOpened():
        print("autonomous_get_to_point: provided camera is not open")
        return (False, False)

    apriltag_detector = apd.make_aptDetector()
    cam_matrix = apd.get_calib_matrix()

    curr_lin = 0.0
    curr_ang = 0.0

    reached_goal = False
    already_at_target = False

    try:
        while True:
            ret, frame = cam.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            tags = apd.detect_Tags(apriltag_detector, gray_frame, cam_matrix)
            detection = tags
            
    
            det_frame = apd.draw_detection(frame, tags)
            cv2.imshow('Apriltag Detected', det_frame)
            if cv2.waitKey(1) == ord('q'):
                break

            if ROBOT_TAG_ID in tags:
                poseR = tags[ROBOT_TAG_ID].pose_R
                poseT =tags[ROBOT_TAG_ID].pose_t
                axis, direction = apd_nav.get_closest_direction_and_axis(poseT, poseR, target_point)
                # print(f"go: {axis}, {direction}")
                
                if axis is None:
                    tcp_client.send_floats(0.0, 0.0)
                    print("reached goal")
                    reached_goal = True
                    already_at_target = True
                    break   

                fwd, angg, errr = apd_nav.rotate_robot_toNEW(direction, poseR)
                # print(f"Forward: {fwd}, Turn: {angg}, Error: {errr}")

                if(angg != 0.0):
                    curr_lin = 0.0
                    if (angg != curr_ang):
                        tcp_client.send_floats(0.0, angg)
                        curr_ang = angg
                else:
                    fwd = lin
                    if(fwd != curr_lin):
                        tcp_client.send_floats(fwd, 0.0)
                        curr_lin = fwd
            else:
                tcp_client.send_floats(0.0, 0.0)
                curr_lin = 0.0
                curr_ang = 0.0

            time.sleep(0.01)
    finally:
        try:
            cv2.destroyWindow('Apriltag Detected')
        except:
            pass

    return (reached_goal, already_at_target)



def main_camera_loop():
    url = PHONE_CAMERA_URL_IPWEB

    # cam = cv2.VideoCapture(url,)
    cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

    fourcc_int = int(cam.get(cv2.CAP_PROP_FOURCC))
    fourcc_str = "".join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])

    # print("Video format (FOURCC):", fourcc_str)

    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print(frame_width, frame_height)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # cam.set(cv2.CAP_PROP_FPS, 60)
    # cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Prevent internal buffering


    apriltag_detector = apd.make_aptDetector()
    cam_matrix = apd.get_calib_matrix()
    prev_dist = 0.0

    prev_x = 0.0
    prev_y = 0.0
    prev_yaw = 0.0

    while True:
        ret, frame = cam.read()
        # print(frame.shape)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tags = apd.detect_Tags(apriltag_detector, gray_frame, cam_matrix)
        detection = tags
        
        det_frame = apd.draw_detection(frame, detection)
        cv2.imshow('Detected', det_frame)
        # cv2.imshow('Detected', gray_frame)

        """use to debug the position of the apriltag number 13 - associated with the robot"""
        # try:
        #     pose_tt = np.array(tags[13].pose_t).reshape(3)
        #     x_w = pose_tt[0]
        #     y_w = pose_tt[1]

        #     R = np.asarray(tags[13].pose_R)
        #     yaw = math.atan2(R[1, 0], R[0, 0])


        #     # R = np.array(tags[13].pose_R)
        #     # yaw_rad = math.atan2(R[1,0], R[0,0])
        #     # yaw_deg = math.degrees(yaw_rad)
        #     if abs(x_w - prev_x) > 0.05:
        #         prev_x= x_w
        #     if abs(y_w - prev_y) > 0.05:
        #         prev_y = y_w
        #     if abs(yaw - prev_yaw) > 0.05:
        #         prev_yaw = yaw
        #     # print(f"x: {prev_x}, y: {prev_y}, yaw: {prev_yaw}")
        #     print(f"x: {x_w}, y: {y_w}, yaw: {yaw}")
        # except Exception as e:
        #     pass

        try:
            poseR = tags[12].pose_R
            pose_t =tags[12].pose_t

            R = np.array(tags[12].pose_R)
            yaw_rad = math.atan2(R[1,0], R[0,0])
            pose_tt = np.array(tags[12].pose_t).reshape(3)
            x_w = pose_tt[0]
            y_w = pose_tt[1]

            point = (-0.32, -0.20)
            a, b = apd_nav.get_closest_direction_and_axis(pose_t, poseR, point)
            print(a, b)
            print(x_w, y_w, yaw_rad)
        except Exception as e:
            pass
        """use to debug the distance between tags"""
        # try:
        #     if(tags[11].pose_t is not None and tags[12].pose_t is not None):
        #         dx, dy, dist = apd.distance_between_tags(tags[11], tags[12])
        #         if abs(dist - prev_dist) > 0.05:
        #             prev_dist = dist
        #         print(prev_dist)
        #         print(dist)
        # except Exception as e:
        #     pass    
        
        
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def main():
    # control_thread = threading.Thread(target = controller_thread, daemon= True)
    # control_thread.start()

    """use to debug the camera loop"""
    # main_camera_loop()

    """use for autonomous navigation - connect to tcp server on pico 
    and send velocities based on apriltag detection"""
    client = TCPClient(host = SERVER_IP, port=PORT, timeout= 5.0)
    client.connect()

    # try:
        
    #     autonomous_get_to_point(client, (0.36, 0.16))
    #     autonomous_get_to_point(client, (0.36, -0.15))
    #     autonomous_get_to_point(client, (-0.43, -0.15))
    #     autonomous_get_to_point(client, (-0.43, 0.16))

    # except Exception as e:
    #     print(e)
    #     client.close()

    """use to debug some math"""
    # e = (-1.57 + 1.6 + math.pi) % (2 * math.pi) - math.pi
    # e_deg = math.degrees(e)
    # print(e, e_deg)
    # print(math.radians(180))

    # point = (50, 50)
    # print(apd_nav.get_quadrant(point))

    LEFT_TARGET = (-0.65, -0.05)
    RIGHT_TARGET = (0.7, 0.5)

    cam_phone = cv2.VideoCapture(0, cv2.CAP_V4L2)

    cam_laptop = cv2.VideoCapture("/dev/video1")
    cam_laptop.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cam_laptop.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam_laptop.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # cv2.namedWindow("Live Feed", cv2.WINDOW_NORMAL)  # Or cv2.WINDOW_AUTOSIZE
    # cv2.moveWindow("Live Feed", 1920, 0)  # Position (X=200, Y=150) on screen


    if not cam_laptop.isOpened():
        raise RuntimeError("Cannot open laptop camera")
    if not cam_phone.isOpened():
        raise RuntimeError("Cannot open phone camera")

    
    main.result = None

    left_active = False
    prev_left = False
    right_active = False
    prev_right = False

    try:
        landmarker = ht.define_model()
        start = time.monotonic()

        while True:
            ret1, frame1 = cam_laptop.read()
            ret2, frame2 = cam_phone.read()
            if not ret1 or not ret2:
                time.sleep(0.1)
                continue

            ts = int((time.monotonic() - start) * 1000)
            mp_img = ht.mp.Image(image_format=ht.mp.ImageFormat.SRGB, data=frame1)
            landmarker.detect_async(mp_img, ts)

            tip = ht.get_index_tip_coords(landmarker.get_result(), frame1.shape) 
            frame1, left_active, right_active = ht.draw_ui_sections(frame1, tip, left_active, right_active)

            if left_active and not prev_left:
                print(">>> finger ENTERED LEFT box")
                reached, already = autonomous_get_to_point(client, LEFT_TARGET, cam=cam_phone)
                if already:
                    print("already at LEFT target")
                if reached:
                    print("reached LEFT target")
                else:
                    print("failed to reach LEFT target")

            if right_active and not prev_right:
                print(">>> finger ENTERED RIGHT box")
                reached, already = autonomous_get_to_point(client, RIGHT_TARGET, cam=cam_phone)
                if already:
                    print("already at RIGHT target")
                if reached:
                    print("reached RIGHT target")
                else:
                    print("failed to reach RIGHT target")

            # update previous state for the next frame
            prev_left = left_active
            prev_right = right_active

            if landmarker.get_result():
                frame1 = ht.draw_hand_landmarks(frame1, landmarker.get_result())

            cv2.imshow("Live Feed", frame1)
            cv2.imshow("Phone Feed", frame2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam_phone.release()
        cam_laptop.release()
        cv2.destroyAllWindows()






if __name__ == "__main__":
    main()