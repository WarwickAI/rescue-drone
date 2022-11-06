# Drone Project

# Finds face from image feed, returns bounding box?
def find_face(frame):
    # TODO
    return None

# Adjust position of drone so that face is straight in front of drone
def adjust_position(face):
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
while True:
    face = find_face()
    adjust_position(face)
    adjust_distance(face)

    
