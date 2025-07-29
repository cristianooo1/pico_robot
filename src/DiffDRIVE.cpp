#include "DiffDRIVE.h"

DiffDriveKinematics::DiffDriveKinematics(float wheelRadius, float wheelBase, MotorManager& left, MotorManager& right)
    : wheelRadius_(wheelRadius), wheelBase_(wheelBase), leftMotor_(left), rightMotor_(right) {}

void DiffDriveKinematics::setWheelVelocity(float linear, float angular) {
    targetLinearVelocity_ = linear; //m/s
    targetAngularVelocity_ = angular; //rad/s

    if (targetLinearVelocity_ == 0.0f && targetAngularVelocity_ == 0.0f) {
        // If both velocities are zero, stop the motors
        LeftWheelVelocity_ = 0.0f;
        RightWheelVelocity_ = 0.0f;
        leftMotor_.set_TargetRadPerSec(0.0f, true);
        rightMotor_.set_TargetRadPerSec(0.0f, false);
        return;
    }

    if (targetLinearVelocity_ != 0.0f && targetAngularVelocity_ == 0.0f){
        float rps = targetLinearVelocity_ / wheelRadius_;
        bool cw = true;
        if (rps < 0){
            cw = false;
            rps = -rps;
        }
        LeftWheelVelocity_ = rps;
        RightWheelVelocity_ = rps;
        leftMotor_.set_TargetRadPerSec(LeftWheelVelocity_, cw);
        rightMotor_.set_TargetRadPerSec(RightWheelVelocity_, !cw);
    }

    if (targetLinearVelocity_ == 0.0f && targetAngularVelocity_ != 0.0f){
        // omega positive is left turn - CCW
        float rps = (targetAngularVelocity_ * wheelBase_ / 2.0f) / wheelRadius_;
        bool cw = true;
        if (rps < 0){
            cw = false;
            rps = -rps;
        }
        LeftWheelVelocity_ = rps;
        RightWheelVelocity_ = rps;
        leftMotor_.set_TargetRadPerSec(LeftWheelVelocity_, !cw);
        rightMotor_.set_TargetRadPerSec(RightWheelVelocity_, !cw);
    }
    

}