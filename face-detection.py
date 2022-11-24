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

        # Set the frane as writable and convert to normal colour
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.detections: #if face detected
            drawing.draw_detection(frame, results.detections[0]) #draw detections if any

            noseX = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.NOSE_TIP).x #get coords for face points
            noseY = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.NOSE_TIP).y

            lEarX = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.LEFT_EAR_TRAGION).x
            lEarY = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.LEFT_EAR_TRAGION).y

            rEarX = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.RIGHT_EAR_TRAGION).x
            rEarY = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.RIGHT_EAR_TRAGION).y

            lEyeX = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.LEFT_EYE).x
            lEyeY = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.LEFT_EYE).y

            rEyeX = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.RIGHT_EYE).x
            rEyeY = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.RIGHT_EYE).y

            mouthX = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.MOUTH_CENTER).x
            mouthY = detection.get_key_point(results.detections[0], detection.FaceKeyPoint.MOUTH_CENTER).y

            faceX = (noseX + lEarX + rEarX + lEyeX + rEyeX + mouthX) / 6 #get overall face coords by averaging face point coords
            faceY = (noseX + lEarY + rEarY + lEyeY + rEyeY + mouthY) / 6
            cv2.line(frame, (int(faceX * frame.shape[1]), frame.shape[0]), (int(faceX * frame.shape[1]), 0), (255,0,0), 2) #draws lines representing these coords
            cv2.line(frame, (frame.shape[1], int(faceY * frame.shape[0])), (0, int(faceY * frame.shape[0])), (255,0,0), 2)

            if faceX < 0.33333: #draw a rectangle based on which third the face is in
                if faceY < 0.33333: #top right
                    cv2.rectangle(frame, (0,0), (int(frame.shape[1] * 0.33333), int(frame.shape[0] * 0.33333)), (0, 255, 0), 2)
                elif faceY > 0.66666: #bottom right
                    cv2.rectangle(frame, (0, frame.shape[0]), (int(frame.shape[1] * 0.33333), int(frame.shape[0] * 0.66666)), (0, 255, 0), 2)
                else: #middle right
                    cv2.rectangle(frame, (0,int(frame.shape[0]*0.66666)), (int(frame.shape[1] * 0.33333), int(frame.shape[0] * 0.33333)), (0, 255, 0), 2)
            elif faceX > 0.66666:
                if faceY < 0.33333: #top left
                    cv2.rectangle(frame, (int(frame.shape[1]),0), (int(frame.shape[1] * 0.66666), int(frame.shape[0] * 0.33333)), (0, 255, 0), 2)
                elif faceY > 0.66666: #bottom left
                    cv2.rectangle(frame, (int(frame.shape[1]), frame.shape[0]), (int(frame.shape[1] * 0.66666), int(frame.shape[0] * 0.66666)), (0, 255, 0), 2)
                else: #middle left
                    cv2.rectangle(frame, (int(frame.shape[1]),int(frame.shape[0]*0.66666)), (int(frame.shape[1] * 0.66666), int(frame.shape[0] * 0.33333)), (0, 255, 0), 2)
            else:
                if faceY < 0.33333: #top middle
                    cv2.rectangle(frame, (int(frame.shape[1] * 0.66666),0), (int(frame.shape[1] * 0.33333), int(frame.shape[0] * 0.33333)), (0, 255, 0), 2)
                elif faceY > 0.66666: #bottom middle
                    cv2.rectangle(frame, (int(frame.shape[1] * 0.66666), frame.shape[0]), (int(frame.shape[1] * 0.33333), int(frame.shape[0] * 0.66666)), (0, 255, 0), 2)
                else: #middle middle
                    cv2.rectangle(frame, (int(frame.shape[1] * 0.66666),int(frame.shape[0]*0.66666)), (int(frame.shape[1] * 0.33333), int(frame.shape[0] * 0.33333)), (0, 255, 0), 2)
            
        # Flip the frame
        cv2.imshow('face detection', cv2.flip(frame, 1))
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

input.release()