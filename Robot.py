import sys
from math import *

import time
import serial

from ComputerVision import Vision
from Kinematics import Kinematics


class Robot():
    def __init__(self, bicep, forearm, configuration, weights, trainingfile):
        self.Vision = Vision(configuration, weights, trainingfile)
        self.Kinematics = Kinematics()
        self.distance = None
        self.cameraAngle = pi/4
        self.ObjectX = 0
        self.ObjectY = 0
        self.bicep = bicep
        self.forearm = forearm

    def get_object(self):
        """Subroutine calls the get distance subroutine from the Vision class to return the item wanting to be found"""
        item = self.Vision.get_distance()
        self.distance = item[3]*100
        # If the object is more than the length of the arm then the main class is called again
        if self.distance > self.bicep + self.forearm:
            print("Object is out of range")
            main()

    def get_object_coordinates(self):
        self.get_object()
        self.ObjectX = cos(self.cameraAngle)*self.distance
        self.ObjectY = sin(self.cameraAngle)*self.distance

    def move_to_object(self):
        solved = self.Kinematics.move_to_object()
        return solved

    def initialise(self):
        self.Kinematics.initialise(0, 0, self.bicep, self.forearm, 10, 20)

def main():
    # Serial setup
    # Used to flush serial line to allow data to be sent
    """ser = serial.Serial("COM3", 115200, timeout=1)
    ser.setDTR(False)
    time.sleep(1)
    ser.flushInput()
    ser.setDTR(True)
    time.sleep(2)"""

    # These are the dimensions of my robot arm in cm
    BICEP = 23
    FOREARM = 36
    # The robot class is called, inputting the dimensions and the CNN model.
    robot = Robot(BICEP, FOREARM, "yolov3-tiny.cfg", "yolov3-tiny.weights", "coco.names")

    robot.initialise()
    robot.get_object_coordinates()

    robot.Kinematics.set_object_coords(robot.ObjectX, robot.ObjectY)

    robot.move_to_object()

    # The angles are received from the kinematics class and then sent over serial to the arduino.
    angles = robot.Kinematics.get_angles()
    shoulder = str(round(degrees(angles[0])))
    elbow = str(round(degrees(angles[1])))
    data = shoulder + " " + elbow
    #ser.write(data.encode())
    sys.exit()


if __name__ == "__main__":
    main()