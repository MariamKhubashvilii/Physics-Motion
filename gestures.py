def get_gesture(landmarks):
    """
    landmarks: list of 21 (x, y, z) tuples for one hand
    returns: string gesture name
    """
    if not landmarks:
        return "none"

    # Tip indices and their corresponding knuckle (MCP) indices
    tips   = [4, 8, 12, 16, 20]
    mcps   = [2, 5, 9,  13, 17]  # base knuckles

    fingers_up = []

    # Thumb: compare x instead of y (it sticks out sideways)
    # If tip is to the left of its base, it's extended (for right hand)
    fingers_up.append(landmarks[4][0] < landmarks[2][0])

    # Other four fingers: tip y < mcp y means finger is pointing up
    # (y increases downward in image coordinates)
    for tip, mcp in zip(tips[1:], mcps[1:]):
        fingers_up.append(landmarks[tip][1] < landmarks[mcp][1])

    thumb, index, middle, ring, pinky = fingers_up

    # --- Gesture rules ---
    if index and not middle and not ring and not pinky:
        return "point"                        # grab / interact

    if index and middle and not ring and not pinky:
        return "peace"                        # toggle 2D / 3D

    if not any(fingers_up):
        return "fist"                         # delete object

    if all(fingers_up):
        return "open_palm"                    # pause simulation

    if not index and not middle and not ring and not pinky:
        # Thumb and no fingers = checking pinch distance
        pass

    # Pinch: thumb tip and index tip close together
    tx, ty, _ = landmarks[4]
    ix, iy, _ = landmarks[8]
    pinch_dist = ((tx - ix)**2 + (ty - iy)**2) ** 0.5
    if pinch_dist < 40:
        return "pinch"                        # spawn object

    return "none"