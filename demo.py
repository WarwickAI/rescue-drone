import cv2
import mediapipe as mp
import time 
from djitellopy import Tello

def is_face_visible(frame): #gets wether a face is on a given frame
    detection = mp.solutions.face_detection 

    with detection.FaceDetection(model_selection = 0,min_detection_confidence=0.5) as faceDetection: 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = faceDetection.process(frame) #processes frame
        # Make sure the whole face is visible
        try:
            noseX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.NOSE_TIP).x #get coords for face points
            noseY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.NOSE_TIP).y
            lEarX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.LEFT_EAR_TRAGION).x
            lEarY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.LEFT_EAR_TRAGION).y
            rEarX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.RIGHT_EAR_TRAGION).x
            rEarY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.RIGHT_EAR_TRAGION).y
            lEyeX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.LEFT_EYE).x
            lEyeY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.LEFT_EYE).y
            rEyeX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.RIGHT_EYE).x
            rEyeY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.RIGHT_EYE).y
            mouthX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.MOUTH_CENTER).x
            mouthY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.MOUTH_CENTER).y
            faceX = (noseX + lEarX + rEarX + lEyeX + rEyeX + mouthX) / 6 #get overall face coords by averaging face point coords
            faceY = (noseY + lEarY + rEarY + lEyeY + rEyeY + mouthY) / 6
        except:
            return False
        return True

def findReigon(frame):
    detection = mp.solutions.face_detection

    with detection.FaceDetection(model_selection = 0,min_detection_confidence=0.5) as faceDetection: 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = faceDetection.process(frame)
        try:
            noseX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.NOSE_TIP).x #get coords for face points
            noseY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.NOSE_TIP).y
            lEarX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.LEFT_EAR_TRAGION).x
            lEarY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.LEFT_EAR_TRAGION).y
            rEarX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.RIGHT_EAR_TRAGION).x
            rEarY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.RIGHT_EAR_TRAGION).y
            lEyeX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.LEFT_EYE).x
            lEyeY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.LEFT_EYE).y
            rEyeX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.RIGHT_EYE).x
            rEyeY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.RIGHT_EYE).y
            mouthX = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.MOUTH_CENTER).x
            mouthY = detection.get_key_point(result.detections[0], detection.FaceKeyPoint.MOUTH_CENTER).y
            faceX = (noseX + lEarX + rEarX + lEyeX + rEyeX + mouthX) / 6 #get overall face coords by averaging face point coords
            faceY = (noseY + lEarY + rEarY + lEyeY + rEyeY + mouthY) / 6
        except:
            return 'centre'
        if faceX < 0.33333: #draw a rectangle based on which third the face is in
            if faceY < 0.33333: #top right
                return 'right'
            elif faceY > 0.66666: #bottom right
                return 'right'
            else: #middle right
                return 'right'
        elif faceX > 0.66666:
            if faceY < 0.33333: #top left
                return 'left'
            elif faceY > 0.66666: #bottom left
                return 'left'
            else: #middle left
                return 'left'
        else:
            if faceY < 0.33333: #top middle
                return 'centre'
            elif faceY > 0.66666: #bottom middle
                return 'centre'
            else: #middle middle
                return 'centre'


def search_for_face(minH, maxH):
    UPBY = 20
    while True:
        while drone.get_height() <= maxH:
            frame = get_frame()
            #drone.rotate_clockwise(360)
            cv2.imshow('face detection', frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            if is_face_visible(frame):
                return
           # time.sleep(2)
            drone.move_up(UPBY)
            time.sleep(2)

        while drone.get_height() >= minH :
            frame= get_frame()
            #drone.rotate_clockwise(360)
            cv2.imshow('face detection', frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            if is_face_visible(frame):
                return
           # time.sleep(2)
            drone.move_down(UPBY)
            time.sleep(2)

def get_frame():
    frame = drone.get_frame_read().frame
    frame = cv2.resize(frame, (1000, 1000))
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ##maybe wrong
    return frame

def rotate(direction):
    if direction == 'left':
        drone.rotate_counter_clockwise(30)
    elif direction == 'right':
        drone.rotate_clockwise(30)


global drone
drone = Tello()

drone.connect()
drone.takeoff()
print("Battery: ", drone.get_battery())

drone.streamon()

detection = mp.solutions.face_detection

search_for_face(100, 300)
## Input loop
while True:
    frame = get_frame()
    region = findReigon(frame)
    if region == 'right':
        rotate(region)
    elif region == 'left':
        rotate(region)
    elif region == 'centre':
        continue

    # Flip the frame
    cv2.imshow('face detection', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

drone.streamoff()
drone.land()