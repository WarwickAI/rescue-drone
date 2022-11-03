from djitellopy import Tello
import cv2
import threading

def main():
    # set up drone
    global drone
    drone = Tello()
    drone.connect()

    #create video thread
    GetVideo = threading.Thread(target=GetVideo)
    GetVideo.daemon = True
    GetVideo.start()

    #get keyboard input
    while True:
        key = cv2.waitKey(1) & 0xff
        if key == 27: # ESC
            drone.emergency()
            break
        elif key == ord(' '):
            drone.land()
            break
        elif key == ord('w'):
            drone.move_forward(30)
        elif key == ord('s'):
            drone.move_back(30)
        elif key == ord('a'):
            drone.move_left(30)
        elif key == ord('d'):
            drone.move_right(30)
        elif key == ord('e'):
            drone.rotate_clockwise(30)
        elif key == ord('q'):
            drone.rotate_counter_clockwise(30)
        elif key == ord('r'):
            drone.move_up(30)
        elif key == ord('f'):
            drone.move_down(30)

def GetVideo():
    # get video stream from drone
    drone.streamon()
    while True:
        frame = drone.get_frame_read().frame
        frame = cv2.resize(frame, (1000, 1000))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("Drone cam", frame)
        cv2.waitKey(1)

main()
