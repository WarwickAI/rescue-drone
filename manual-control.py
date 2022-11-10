from djitellopy import Tello
import cv2
import threading
import keyboard

def main():
    # set up drone
    global drone
    drone = Tello()
    drone.connect()

    #create video thread
    v = threading.Thread(target=GetVideo)
    v.daemon = True
    v.start()

    drone.takeoff()

    # Do pip install keyboard
    #get keyboard input
    while True:
        try:
            if keyboard.is_pressed('esc'): # ESC
                drone.emergency()
                break
            elif keyboard.is_pressed(' '):
                drone.land()
                break
            elif keyboard.is_pressed('w'):
                print('forward')
                drone.move_forward(30)
            elif keyboard.is_pressed('s'):
                drone.move_back(30)
            elif keyboard.is_pressed('a'):
                drone.move_left(30)
            elif keyboard.is_pressed('d'):
                drone.move_right(30)
            elif keyboard.is_pressed('e'):
                drone.rotate_clockwise(30)
            elif keyboard.is_pressed('q'):
                drone.rotate_counter_clockwise(30)
            elif keyboard.is_pressed('r'):
                drone.move_up(30)
            elif keyboard.is_pressed('f'):
                drone.move_down(30)
        except:
            continue

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
