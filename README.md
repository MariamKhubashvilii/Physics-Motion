# Motion and Free Fall Physics Simulator with Hand Tracking

A Python project about motion, free fall, and basic physics concepts, controlled with webcam hand tracking.

The simulator lets you create and move objects in real time while showing how gravity, speed, bouncing, and energy change during motion.

The app uses your webcam to detect your hand, turns simple hand poses into gestures, and lets you interact with moving objects on screen.

It is meant to make physics topics like falling, throwing, bouncing, velocity, and energy easier to see.

## Features

* Real-time hand tracking with MediaPipe
* Gesture-based controls
* Spawn, grab, throw, and delete objects
* Motion based on gravity and free fall
* Basic bouncing and ground friction
* Object collisions
* Toggle between 2D and 3D views
* On-screen display for gesture, mode, speed, kinetic energy, and potential energy
* Motion trails to help visualize movement over time

## Demo Controls

The simulator recognizes these gestures:

* **Point** - grab and throw an object
* **Pinch** - spawn a new object
* **Fist** - delete the nearest object
* **Open palm** - pause or resume the simulation
* **Peace sign** - toggle between 2D and 3D mode
* **Q key** - quit the app

## Project Structure

```text
.
├── main.py
├── hand_tracker.py
├── gestures.py
├── physics_engine.py
├── renderer.py
└── README.md
```

### File Overview

* **main.py** - Runs the webcam loop, processes gestures, updates physics, and renders the simulation
* **hand_tracker.py** - Detects hands and returns landmark coordinates using MediaPipe
* **gestures.py** - Converts hand landmarks into gesture labels such as `point`, `pinch`, and `fist`
* **physics_engine.py** - Handles object motion, gravity, collisions, bounce, and friction
* **renderer.py** - Draws objects, trails, vectors, stats, and the HUD on screen

## What Physics Ideas It Shows

This project is mainly about motion.

It helps show ideas like:

* free fall
* gravity
* velocity
* acceleration
* bouncing
* friction
* kinetic energy
* potential energy
* collisions

Instead of only reading about these ideas, you can see them happen on screen and interact with them.

## How It Works

1. The webcam captures a video frame.
2. The program detects your hand landmarks.
3. The gesture system decides which hand pose you are making.
4. That gesture triggers an action, like creating, grabbing, throwing, or deleting an object.
5. The physics engine updates the motion of all objects.
6. The renderer draws the updated scene, vectors, and physics values.
7. The result is shown in an OpenCV window.

## Requirements

* Python 3.10 or newer recommended
* A working webcam
* macOS, Windows, or Linux

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hand-tracking-physics-simulator.git
cd hand-tracking-physics-simulator
```

### 2. Create and activate a virtual environment

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install opencv-python mediapipe numpy
```

## Run the Project

```bash
python main.py
```

If that does not work on your system, try:

```bash
python3 main.py
```

## Notes

* The webcam view is mirrored, so movement feels more natural.
* Right now, the simulator uses the first detected hand.
* Gesture detection is based on simple rules, so lighting, camera angle, and hand position can affect accuracy.
* The 3D mode is a simple depth effect to help visualize motion. It is not a full 3D engine.
* This project is best seen as an interactive physics demo, not a fully realistic physics simulator.

## Known Limitations

* Thumb detection is simplified and may be less reliable for different hand orientations
* Pinch detection uses a fixed pixel distance threshold
* Object grabbing directly sets object position instead of applying a physical constraint
* The red arrow shown on screen represents gravity direction, not the exact current net force vector

## Possible Improvements

* Make the hand gestures more stable and reliable
* Add sliders for gravity, friction, or bounce strength
* Show acceleration more accurately on screen
* Add a mode focused only on vectors and motion graphs
* Add more physics topics, like projectile motion or spring motion
* Add a non-camera mode for keyboard or mouse interaction

## Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy
