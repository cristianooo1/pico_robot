import numpy as np
import math
import time

def wrap_to_pi(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi

def get_robot_yaw(pose_R):
    R = np.asarray(pose_R)
    yaw = math.atan2(R[1, 0], R[0, 0])
    return wrap_to_pi(yaw)

def get_robot_xy(pose_t):
    pose_tt = np.array(pose_t).reshape(3)
    x = pose_tt[0]
    y = pose_tt[1]
    return x, y

def get_closest_direction_and_axis(pose_t, pose_R, target_point, xy_threshold = 0.05):
    current_yaw = get_robot_yaw(pose_R)
    curr_x, curr_y = get_robot_xy(pose_t)
    target_x, target_y = target_point

    dx = target_x - curr_x
    dy = target_y - curr_y

    poss_dir = []

    if abs(dx) > xy_threshold:
        if dx >= 0:
            poss_dir.append("right")
        else:
            poss_dir.append("left")
    
    if abs(dy) > xy_threshold:
        if dy >= 0:
            poss_dir.append("down")
        else:
            poss_dir.append("up")

    if not poss_dir:
        return None, None  # Already close enough to target

    best_dir = min(poss_dir, key=lambda d: abs(wrap_to_pi(current_yaw - get_target_yaw(d))))

    # Map direction to axis
    axis_map = {"right": "x", "left": "x", "up": "y", "down": "y"}
    return axis_map[best_dir], best_dir

def get_target_yaw(direction):
    directions = {
        "right": 0.0,
        "down": math.radians(90),
        "left": math.radians(180),
        "up": math.radians(-90)
    }

    return directions[direction.lower()]

def rotate_robot_to(direction, pose_R, threshold_deg = 3, ang_speed = 0.8):
    current_yaw = get_robot_yaw(pose_R)
    target_yaw = get_target_yaw(direction)

    error = wrap_to_pi(target_yaw - current_yaw)
    print(f"current_yaw: {current_yaw}, target_yaw: {target_yaw}, error: {error}")
    threshold = math.radians(threshold_deg)

    if abs(error) > threshold:
        direction_sign = 1 if error > 0 else -1
        return 0.0, direction_sign * ang_speed
    else:
        return 0.0, 0.0
    
def rotate_robot_toNEW(direction, pose_R, threshold_deg = 10, ang_speed_fast = 0.8, ang_speed_slow = 0.4):
    current_yaw = get_robot_yaw(pose_R)
    target_yaw = get_target_yaw(direction)

    error = wrap_to_pi(target_yaw - current_yaw)
    error_deg = math.degrees(error)
    # print(f"current_yaw: {current_yaw}, target_yaw: {target_yaw}, error: {error}")
    # print(f"current_yaw: {math.degrees(current_yaw)}, target_yaw: {math.degrees(target_yaw)}, error:{error}= {error_deg}deg")

    threshold = math.radians(threshold_deg)

    if abs(error) <= threshold:
        return 0.0, 0.0, error_deg
    elif error_deg <= 30:  # Close to target - use slow speed
        direction_sign = -1 if error > 0 else 1
        return 0.0, direction_sign * ang_speed_slow, error_deg
    else:  # Far from target - use fast speed
        direction_sign = -1 if error > 0 else 1
        return 0.0, direction_sign * ang_speed_slow, error_deg
    
def move_robot_to(target_point, pose_t, pose_R, position_threshold = 0.05, lin_speed = 0.15):
    curr_x, curr_y = get_robot_xy(pose_t)
    target_x, target_y = target_point
    curr_yaw = get_robot_yaw(pose_R)

    dx = target_x - curr_x
    dy = target_y - curr_y

    if abs(dx) < position_threshold and abs(dy) < position_threshold:
        return 0.0, 0.0, "reached", "completed"
