import pupil_apriltags as pat
import cv2
import numpy as np
from pathlib import Path
import sys



def get_calib_matrix():
    curr_dir = Path(__file__).parent

    try:
        calibration = np.load(curr_dir / "calibration.npz")

    except FileNotFoundError:
        sys.exit(f"Calibration file not found in {curr_dir}")

    camera_matrix = calibration["camera_matrix"]

    return camera_matrix

def get_aptDetector(fam = "tagStandard41h12", nthreads = 1, quad_decimate = 1.0, quad_sigma = 0.0, refine_edges = 1, decode_sharpening = 0.25, debug = 0):

    apriltag_detector = pat.Detector(
        families=fam,
        nthreads=nthreads,
        quad_decimate= quad_decimate,
        quad_sigma=quad_sigma,
        refine_edges=refine_edges,
        decode_sharpening=decode_sharpening,
        debug=debug
    )
    return apriltag_detector


def make_detection(apt_detector, frame ,cam_mtx:np.ndarray, pose: bool = True, tag : float = 0.11111111):
    detection = apt_detector.detect(   img = frame, 
                                                estimate_tag_pose=pose, 
                                                camera_params=(
                                                        cam_mtx[0,0],
                                                        cam_mtx[1,1],
                                                        cam_mtx[0,2],
                                                        cam_mtx[1,2]),
                                                tag_size=tag)
    
    return detection

def draw_detection(img, detections, font=cv2.FONT_HERSHEY_SIMPLEX):
    for det in detections:
        corners = det.corners
        center = det.center
        pose_t = det.pose_t
        pose_r = det.pose_R

        corners = np.array(corners, dtype=np.int32)
        center = tuple(map(int, center))

        for i in range(4):
            pt1 = tuple(corners[i])
            pt2 = tuple(corners[(i + 1) % 4])
            cv2.line(img, pt1, pt2, (0, 255, 0), 2)

        cv2.circle(img, center, 5, (0, 0, 255), 2)
        cv2.putText(img, f"{det.tag_id}", (150,150), font, 
                5, (255, 0, 0), 2, cv2.LINE_AA)
        

        

    return (img, pose_t, pose_r)

if __name__ == "__main__":
    pass
    # cam_matrix = get_calib_matrix()
    # while True:
    #     ret, frame = cam.read()
    #     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #     # Display the captured frame
    #     # cv2.imshow('Camera', frame)
    #     # print(frame.shape)
    #     # print(gray_frame.shape)
    #     detection = apriltag_detector.detect(   img = gray_frame, 
    #                                             estimate_tag_pose=True, 
    #                                             camera_params=(
    #                                                     cam_matrix[0,0],
    #                                                     cam_matrix[1,1],
    #                                                     cam_matrix[0,2],
    #                                                     cam_matrix[1,2]),
    #                                             tag_size=0.11111111)
        
    #     det_frame, t, r = draw_detection(frame, detection)
    #     cv2.imshow('Detected', det_frame)
    #     print(f"translation: {t}")
    #     print(f"rotation: {r}")




    #     # for i in detection:
    #     #     print(f"Detection has {len(detection)} items.")
    #     #     print(f"Center: {i.center}")
    #     #     print(f"Corners: {i.corners}")
    #     # print(type(detection))
    #     # print(dir(detection))



    #     # Press 'q' to exit the loop
    #     if cv2.waitKey(1) == ord('q'):
    #         break

    # # Release the capture and writer objects
    # cam.release()
    # cv2.destroyAllWindows()



    # # print(detection.center)