# Drone Project

# Finds face from image feed, returns bounding box?
from turtle import position


def find_face(frame):
    # Rotations of face
    # Position of face in picture

    # TODO
    return None

# Find movement direction of person

# Standby mode

# Adjust position of drone so that face is straight in front of drone
def adjust_position(face):
    # get position of head in image
    position = (0, 0)
    # Need distance from drone and some maths
    dist = get_face_distance()
    
    # adjust position
    # exit when relatively central
    # TODO
    return None

# Return estimated distance from face to drone
def get_face_distance(face):
    # TODO
    return None

# Move drone to maintain some distance from face (maybe 2m?)
def adjust_distance(face):
    # TODO
    return None


# Main loop of program

# find person

# stay with person
# is person still in view?
person = True

while True:
    if person:
        face = find_face()
        adjust_position(face)
        adjust_distance(face)
    else:
        # Find new person or deactivate
        print("lost person")


    
