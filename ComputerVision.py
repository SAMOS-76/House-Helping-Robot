import pyrealsense2 as rs
import numpy as np
import cv2

from SpeechRecognition import *
"""Code references:
https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html
https://dev.intelrealsense.com/docs/python2
"""


class Vision:
    def __init__(self, configuration, weights, trainingfile):
        #self._Speech = Speech()
        """ Used composition association to have the speech class part of the Vision class. This is because the output
        of the Vision class directly depends on the output from the speech class as this is the object we're trying
        to detect."""

        self._box_threshold = 0.5  # Confidence threshold used for whether to keep a bounding box or not
        self._nmsThreshold = 0.4  # Non-maximum suppression threshold discards bounding boxes if they are below a certain
                                 # probability.

        self._pipeline = rs.pipeline()  # This is the pyrealsense class that runs the depth image screen
        self._config = rs.config()  # Configuration method part of pyrealsense that is used for setup
        self._classes = None  # Stores the detected object per frame

        self._ImageWidth = 416  # Width of input image
        self._ImageHeight = 416  # Height of input image
        self._screenWidth = 640
        self._screenHeight = 480

        self._YoloConfig = configuration  # This is the pretrained models configuration file
        self._YoloWeights = weights  # This is the pretrained model
        self._object_file = trainingfile  # This file contains the names of the objects the model was trained on
        # and what can be detected
        self.__name = []
        self._detected = []

    def _intel_setup(self):
        """This is standard setup code for the Intel Realsense camera which is found in the documentation to allow
        the accurate control of the camera. Have edited variables to make them more human-readable and removed redundant
        code while adding code to make it robust.
        https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/opencv_viewer_example.py
        """

        # Added exception handling to exit the program if a camera is not connected to begin with. This uses the
        # returned RuntimeError from the config.
        pipeline_wrapper = rs.pipeline_wrapper(self._pipeline)
        try:
            pipeline_profile = self._config.resolve(pipeline_wrapper)
        except RuntimeError:
            print("Device is not connected!")
            sys.exit()

        camera = pipeline_profile.get_device()
        device_product_line = str(camera.get_info(rs.camera_info.product_line))

        found_rgb_sensor = False  # Set to True if camera has both depth and colour sensor

        for s in camera.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb_sensor = True
                break
        if not found_rgb_sensor:
            print("This robot requires both depth and colour sensor")
            sys.exit()

        # Configure video stream with screen width and height.
        self._config.enable_stream(rs.stream.depth, self._screenWidth, self._screenHeight, rs.format.z16, 30)

        # configures stream depending on intel camera used
        if device_product_line == 'L500':
            self._config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            self._config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start video stream
        self._pipeline.start(self._config)

    def _get_output_layers(self, net):
        """In YOLO there are multiple output video layers and this is a standard function that gets the layers out.
        Seen here at https://towardsdatascience.com/yolo-object-detection-with-opencv-and-python-21e50ac599e9"""
        layersNames = net.getLayerNames()
        output_layers = [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

    def _drawPredicted(self, classId, left, top, right, bottom, frame, x, y):
        """This function is responsible for drawing the bounding boxes on the image."""
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 3)  # Draw bounding box with coordinates

        # Gets the depth map created by the camera
        depth_frame = self._pipeline.wait_for_frames().get_depth_frame().as_depth_frame()
        distance = depth_frame.get_distance(x, y)  # Gets the exact depth of the pixel located at the centre of the box

        ObjectName = ""
        if self.classes:
            ObjectName = str(self.classes[classId])

        # If the name is in the COCO file then label the name
        cv2.putText(frame, ObjectName, (left, top), 2, 0.75, (57, 255, 20), 2)

        #object_distance = "Dist: " + str(round(distance, 2)) + " m"
        # display the distance on the screen
        #cv2.putText(frame, object_distance, (left, top + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (57, 255, 20), 2)

        return distance

    def _bounding_boxes(self, frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self._box_threshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self._box_threshold, self._nmsThreshold)
        for item in indices:
            box = boxes[item]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            x = int(left + width / 2)
            y = int(top + height / 2)
            distance = self._drawPredicted(classIds[item], left, top, left + width, top + height, frame, x, y)

            self._set_name(self.classes[classIds[item]], x, y, distance)

    def _get_name(self):
        return self.__name

    def _set_name(self, name, x, y, distance):
        self.__name = [name, x, y, distance]

    def _start_speech(self):
        # This runs the speech class to get the user to say the object they want
        self._Speech.speech_recognition()
        object = self._Speech.object
        return object

    def _get_detected(self, colour_image, outs):
        self._bounding_boxes(colour_image, outs)
        detected = self._get_name()
        return detected

    def get_distance(self):
        self._intel_setup()
        # Load names of classes
        """The yolo model this code uses is trained with the coco database. 
        Therefore, the coco.names file is read from to get all the possible objects the robot can detect.
        """
        try:
            with open(self._object_file, "rt") as f:
                self.classes = f.read().rstrip('\n').split('\n')
        except FileNotFoundError:
            print("No object file found")
            sys.exit()


        """The convolutional neural network is loaded from the class parameters using cv2.
        The desired parameters for the cnn are made such as wanting the code to work though the CPU rather than the GPU
        """
        net = cv2.dnn.readNetFromDarknet(self._YoloConfig, self._YoloWeights)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        """I'm calling the associated Speech class to then get the object we want."""
        #object = self._start_speech()
        object = input()

        try:
            while True:
                # Wait for a coherent pair of frames: depth and colour
                frames = self._pipeline.wait_for_frames()
                colour_frame = frames.get_color_frame()
                if not colour_frame:
                    continue
                # Convert images to numpy arrays
                colour_image = np.asanyarray(colour_frame.get_data())
                blob = cv2.dnn.blobFromImage(colour_image, 1 / 255.0, (self._ImageWidth, self._ImageHeight), [0, 0, 0],
                                                                        swapRB=True, crop=False)
                net.setInput(blob)
                outs = net.forward(self._get_output_layers(net))
                # Apply colourmap on depth image (image must be converted to 8-bit per pixel first)


                """This code block, gets the detected array from process detection. If there is actually is an object
                in frame or anyobject was said to begin with then it checks if the object in frame matches the object
                we are looking for. If it does match then it returns the detected object leaving the loop and ending the 
                stream."""

                detected = self._get_detected(colour_image, outs)
                if len(detected) > 0 and object is not None:
                    if (detected[0]).upper() in object.upper():
                        print(detected)
                        cv2.destroyAllWindows()
                        return detected

                cv2.imshow('Computer Vision', colour_image)
                # breaks loop/video stream if q is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            # Stop streaming
            self._pipeline.stop()
