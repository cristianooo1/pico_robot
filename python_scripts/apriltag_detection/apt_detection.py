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


def make_aptDetector(fam = "tagStandard41h12", nthreads = 1, 
                    quad_decimate = 1.0, quad_sigma = 0.0, 
                    refine_edges = 1, decode_sharpening = 0.25, 
                    debug = 0):

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


class Apriltag:
    def __init__(self, detection):
        self.tag_id = detection.tag_id
        self.center = tuple(map(int, detection.center))
        self.corners = np.array(detection.corners, dtype=np.int32)
        self.pose_t = detection.pose_t
        self.pose_R = detection.pose_R

def detect_Tags(apt_detector, frame ,cam_mtx:np.ndarray, pose: bool = True, tag_size : float = 0.1):
    detections = apt_detector.detect(   img = frame, 
                                        estimate_tag_pose=pose, 
                                        camera_params=(
                                                cam_mtx[0,0],
                                                cam_mtx[1,1],
                                                cam_mtx[0,2],
                                                cam_mtx[1,2]),
                                        tag_size=tag_size)
    
    tags = {det.tag_id: Apriltag(det) for det in detections}
    return tags

def draw_detection(img, tags, font=cv2.FONT_HERSHEY_SIMPLEX):
    for tag in tags.values():
        for i in range(4):
            pt1 = tuple(tag.corners[i])
            pt2 = tuple(tag.corners[(i + 1) % 4])
            cv2.line(img, pt1, pt2, (0, 255, 0), 2)

        cv2.circle(img, tag.center, 5, (0, 0, 255), 2)
        cv2.putText(img, f"{tag.tag_id}", 
                    tag.center, font, 
                    2, (255, 0, 0), 
                    2, cv2.LINE_AA)
    return (img)

def distance_between_tags(tag1: Apriltag, tag2: Apriltag):
    pos1 = np.array(tag1.pose_t).reshape(3)
    pos2 = np.array(tag2.pose_t).reshape(3)

    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    dist = np.sqrt(dx**2 + dy**2)

    # return np.linalg.norm(pos1 - pos2)
    return (dx, dy, dist)

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