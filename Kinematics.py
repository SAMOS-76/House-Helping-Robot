import numpy as np
import math

class Kinematics:

    def __init__(self):
        self.ShoulderX = 0
        self.ShoulderY = 0
        self._angles = None
        self._joints_coords = None
        self.__object_coords = None
        self.__endeffector = None
        self._ArmSection = None

    def initialise(self, ShoulderX, ShoulderY, bicep, forearm, ShoulderAngle, ElbowAngle):
        """This subroutine is responsible for setting up the arrays containing the required data of the arm"""
        # Coordinates of shoulder joint

        # The joint array follows the T portion of the DH parameters so that's why they end in 0, 1
        self._joints_coords = np.array([[ShoulderX, ShoulderY, 0, 1]], dtype=np.float64)

        # Coordinates of elbow joint
        self._joints_coords = np.vstack((self._joints_coords, np.array([0, 0, 0, 1])))

        # Coordinates of end effector
        self._joints_coords = np.vstack((self._joints_coords, np.array([[0, 0, 0, 1]])))

        # Stores the lengths of each section of the arm
        self._ArmSection = np.array([bicep, forearm])
        self._angles = np.array([], dtype=np.float64)
        self._angles = np.append(self._angles, math.radians(ShoulderAngle))
        self._angles = np.append(self._angles, math.radians(ElbowAngle))

        self._configure_coordinate_system()

    def _get_transformation_matrix(self, angle, x, y):
        """Follows the DH parameters needed to fill the matrix where angle is the angle around the z-axis, and x and y
        are the locations of the joints with respect to the joints coordinate system.
        Returns a 4x4 matrix """
        Matrix = np.array([
            [math.cos(angle), -math.sin(angle), 0, x],
            [math.sin(angle), math.cos(angle), 0, y],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        return Matrix

    def _configure_coordinate_system(self):
        """In this subroutine, I'm multiplying each transformation matrix for each joint to get each joints coordinates
        in terms of the coordinates at joint one. This is through matrix multiplication with dot product """
        Matrix = self._get_transformation_matrix(self._angles[0].item(), self.ShoulderX, self.ShoulderY)
        #print(f"Shoulder matrix: {Matrix}")
        NextMatrix = self._get_transformation_matrix(self._angles[1], self._ArmSection[0], 0)
        Matrix = Matrix.dot(NextMatrix)
        #print(f"Elbow matrix: {Matrix}")
        #print(Matrix[:,[3]].flatten())
        self._joints_coords[1] = Matrix[:,[3]].flatten()
        NextMatrix = self._get_transformation_matrix(0, self._ArmSection[1], 0)
        Matrix = Matrix.dot(NextMatrix)
        #print(f"End effector matrix: {Matrix}")
        self._joints_coords[2] = Matrix[:,[3]].flatten()
        self._set_endeffector_coords(self._joints_coords[2])

        #print(self._joints_coords)

    def _jacobian(self):
        """This method is responsible for creating the jacobian matrix with the partial derivates. This involves complex
        matrix calculations and manipulation. First, we create the axis of rotation which will always be the z-axis.
        This is used for the matrix cross product to get the partial derivatives for the coordinates of the endeffector
        in therms of each joint angle"""

        # Creates the z-axis unit vector to be used to calculate the cross product
        zAxisVector = np.array([0, 0, 1], dtype=np.float64)

        self._set_endeffector_coords(self._joints_coords[2])  # Gets the endEffector Coordinates
        partial1 = np.cross(zAxisVector, (self._get_endeffector_coords()[:3] - self._joints_coords[0][:3]))
        partial2 = np.cross(zAxisVector, (self._get_endeffector_coords()[:3] - self._joints_coords[1][:3]))

        # Create the jacobian matrix by combining the two partial arrays together. This is then transposed
        # to get the matrix in the correct scale
        jacobianMatrix = np.stack((partial1, partial2)).T

        return jacobianMatrix

    def move_to_object(self):
        """Function is responsible for incrementally moving the robot arm to the object's location."""
        self._set_endeffector_coords(self._joints_coords[2])  # Set the end effector coordinates
        # Vector pointing from the end effector to the object
        DirectionVector = self.get_object_coords() - self._get_endeffector_coords()
        DirectionVector = DirectionVector[:3]

        # Gets the magnitude of the direction vector to give a scalar value for the distance between the endeffector and
        # the object
        magnitude = np.linalg.norm(DirectionVector)

        if magnitude > 1:  # If the distance between the end effector and the object is greater than 1 cm, move closer
            Jacobianmatrix = self._jacobian()  # get the jacobian matrix from the function
            JacobianInverse = np.linalg.pinv(Jacobianmatrix)  # Inverse the matrix
            newangle = JacobianInverse.dot(DirectionVector.T)
            self._update_angle(newangle)
            self._configure_coordinate_system()
            self.move_to_object()
        else:
            print(self._angles[0], self._angles[1])

    def _update_angle(self, newangle):
        # subroutine that adds the change of the angle to the value of the previous angle to get the new angle
        self._angles += newangle

    def _get_endeffector_coords(self):  # Getter and setter for end effector
        return self.__endeffector

    def _set_endeffector_coords(self, coords):
        self.__endeffector = coords

    def get_angles(self):  # Getter for angles
        return self._angles

    def set_object_coords(self, x, y):  # Sets the coordinates of the object that the end effector is reaching for
        self.__object_coords = np.array([x, y, 0, 1])

    def get_object_coords(self):  # Gets the object coordinates
        return self.__object_coords
