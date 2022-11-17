import cv2
import mediapipe as mp

detection = mp.solutions.face_detection
drawing = mp.solutions.drawing_utils

input = cv2.VideoCapture(0)
with detection.FaceDetection(model_selection = 0,min_detection_confidence=0.5) as faceDetection: 
    while input.isOpened():
        success, frame = input.read()
        if not success:
            print("Cannot get frame")

        # To improve performance, optionally mark the frame as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceDetection.process(frame)

        # Draw the face detection annotations on the frame.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                drawing.draw_detection(frame, detection)
        # Flip the frame horizontally for a selfie-view display.
        cv2.imshow('face detection', cv2.flip(frame, 1))
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

input.release()