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
            return (None, None)
        if faceX < 0.33333: #draw a rectangle based on which third the face is in
            if faceY < 0.33333: #top left
                return ('high', 'right')
            elif faceY > 0.66666: #bottom left
                return ('low', 'right')
            else: #middle left
                return ('centre', 'right')
        elif faceX > 0.66666:
            if faceY < 0.33333: #top left
                return ('high', 'left')
            elif faceY > 0.66666: #bottom left
                return ('low', 'left')
            else: #middle left
                return ('centre', 'left')
        else:
            if faceY < 0.33333: #top left
                return ('high', 'centre')
            elif faceY > 0.66666: #bottom left
                return ('low', 'centre')
            else: #middle left
                return ('centre', 'centre')


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
            time.sleep(1)

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
            time.sleep(1)

def get_frame():
    frame = drone.get_frame_read().frame
    frame = cv2.resize(frame, (1000, 1000))
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ##maybe wrong
    return frame


global drone
drone = Tello()

drone.connect()
print("Battery: ", drone.get_battery())
drone.takeoff()

drone.streamon()

detection = mp.solutions.face_detection

search_for_face(100, 300)
## Input loop
while True:
    frame = get_frame()
    (vertical, horizontal) = findReigon(frame)
    # Pivot
    if horizontal == 'right':
        drone.rotate_counter_clockwise(15)
    elif horizontal == 'left':
        drone.rotate_clockwise(15)
    # Move vertical
    # if vertical == 'high':
    #     drone.move_down(20)
    # elif vertical == 'low':
    #     drone.move_up(20)
    # No face is found
    if vertical == None:
        drone.rotate_clockwise(360)
        time.sleep(5)
    
    # Show image and exit if 'q' pressed
    cv2.imshow('face detection', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

drone.streamoff()
drone.land()