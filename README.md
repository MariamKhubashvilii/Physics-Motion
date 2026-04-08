# Hand-Controlled Spring Simulator

A Python spring simulation you can control with **hand gestures** through your webcam.

This project combines:
- **OpenCV** for webcam input and on-screen rendering
- **MediaPipe** for hand tracking
- **Tkinter** for live controls
- **Matplotlib** for analytics charts
- a custom **spring physics engine** for displacement, velocity, force, and energy

The result is an interactive mass-spring system where you can drag the mass with your finger, pause the simulation, reset it, switch orientation, and adjust the spring stiffness with a pinch gesture.

## Features

- Real-time webcam hand tracking
- Gesture-based spring control
- Live spring simulation with damping
- Vertical and horizontal spring modes
- On-screen physics HUD
- Separate control panel with sliders and buttons
- Live charts for:
  - displacement vs time
  - velocity vs time
  - kinetic energy vs time
  - potential energy vs time
  - total energy vs time
  - phase diagram

## Demo Controls

### Hand Gestures
- **Point**: drag the mass
- **Peace sign**: switch between vertical and horizontal mode
- **Open palm**: pause or resume the simulation
- **Fist**: reset the simulation
- **Pinch and move up/down**: increase or decrease the spring constant `k`

### Control Panel
You can also adjust the simulation manually with the Tkinter control panel:
- `k` - spring constant
- `m` - mass
- `b` - damping coefficient
- `A` - initial amplitude

You can also:
- pause/resume
- reset
- toggle orientation

## How It Works

The physics engine models a damped spring using:

`F = -kx - bv`

Where:
- `k` is the spring constant
- `x` is displacement
- `b` is damping
- `v` is velocity

Acceleration is computed from Newton's second law:

`a = F / m`

The simulation then updates:
- acceleration
- velocity
- displacement
- time
- energy values
- work done

The renderer visualizes the spring, mass, displacement, velocity, and stress level.  
The chart window stores recent history and plots the motion in real time.

## Project Structure

```text
.
├── main.py
├── spring_engine.py
├── spring_renderer.py
├── hand_tracker.py
├── gestures.py
├── control_panel.py
├── charts_window.py
└── README.md
```

### File Overview

- `main.py` - main loop that connects camera input, gestures, physics, rendering, charts, and controls
- `spring_engine.py` - spring physics engine
- `spring_renderer.py` - OpenCV rendering for the spring, mass, arrows, HUD, and legend
- `hand_tracker.py` - MediaPipe-based hand tracking
- `gestures.py` - gesture recognition logic from hand landmarks
- `control_panel.py` - Tkinter control panel for live parameter changes
- `charts_window.py` - Matplotlib analytics window

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
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
pip install opencv-python mediapipe matplotlib numpy
```

Tkinter usually comes with Python. If it is missing on your system, install it separately using your OS package manager or Python distribution tools.

## Run the Project

```bash
python main.py
```

Make sure your webcam is connected and available.

## Requirements

- Python 3.10+ recommended
- Webcam
- Good lighting for hand tracking

Python packages:
- `opencv-python`
- `mediapipe`
- `matplotlib`
- `numpy`
- `tkinter` (usually bundled with Python)

## Notes

- The simulation uses **damping**, so the motion gradually dies out unless you keep interacting with it.
- The model is visually scaled for screen coordinates, so it is best viewed as an educational interactive simulation rather than a physically calibrated real-world system.
- Only the first detected hand is currently used for control.
- Gesture detection may behave differently depending on hand orientation and lighting conditions.

## Known Limitations

- Release velocity is not yet calculated from hand motion, so there is no true flick behavior when letting go.
- Thumb detection is simpler than the other fingers and may be less reliable depending on the hand used.
- The force shown in the HUD is slightly simplified compared with the full damped force used internally.

## Future Improvements

- Add hand release velocity for more natural motion
- Improve left-hand and right-hand gesture detection
- Add gesture smoothing
- Add multiple spring presets
- Add 3D visualization mode
- Save chart data to CSV
- Add fullscreen mode or a cleaner app layout

Built with Python, OpenCV, MediaPipe, Tkinter, and Matplotlib.
