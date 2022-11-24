import cv2
import mediapipe as mp

def findFace(frame): #gets wether a face is on a given frame
    detection = mp.solutions.face_detection 

    with detection.FaceDetection(model_selection = 0,min_detection_confidence=0.5) as faceDetection: 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = faceDetection.process(frame) #processes frame
        if result.detections: #return wether a face was found or not
            return True
        else:
            return False

def findReigon(frame):
    detection = mp.solutions.face_detection

    with detection.FaceDetection(model_selection = 0,min_detection_confidence=0.5) as faceDetection: 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = faceDetection.process(frame)
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
        if faceX < 0.33333: #draw a rectangle based on which third the face is in
            if faceY < 0.33333: #top right
                return 2
            elif faceY > 0.66666: #bottom right
                return 8
            else: #middle right
                return 5
        elif faceX > 0.66666:
            if faceY < 0.33333: #top left
                return 0
            elif faceY > 0.66666: #bottom left
                return 6
            else: #middle left
                return 3
        else:
            if faceY < 0.33333: #top middle
                return 1
            elif faceY > 0.66666: #bottom middle
                return 7
            else: #middle middle
                return 4