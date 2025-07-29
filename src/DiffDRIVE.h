#ifndef DIFF_DRIVE_H
#define DIFF_DRIVE_H

#include "MotorMANAGER.h"

class DiffDriveKinematics {

public:
    DiffDriveKinematics(float wheelRadius, float wheelBase, MotorManager& left, MotorManager& right);

    void setWheelVelocity(float linear, float angular);

private:
    float wheelRadius_;
    float wheelBase_;
    MotorManager& leftMotor_;
    MotorManager& rightMotor_;

    float targetLinearVelocity_ = 0.0f;
    float targetAngularVelocity_ = 0.0f;

    float LeftWheelVelocity_ = 0.0f;
    float RightWheelVelocity_ = 0.0f;

    

};

#endif // DIFF_DRIVE_H