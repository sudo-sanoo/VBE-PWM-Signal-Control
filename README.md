# VBE-PWM Signal Control
### Virtual-Based Input Emulation System with Pulse Width Modulation Control

**VBE-PWM Signal Control** is a Proof of Concept (POC) prototype designed to simulate analog steering inputs using standard digital keyboards. By utilizing Computer Vision (OpenCV) to track the orientation of a physical rectangular object, this software translates the "tilt" of the object into Variable Duty Cycle keystrokes.

This allows for smooth, "analog-like" steering in games that typically only support binary (WASD) input, such as **Roblox**, effectively turning a piece of cardboard into a steering wheel.

---

## 📖 Table of Contents
- [Concept and Theory](#concept-and-theory)
  - [Computer Vision Pipeline](#computer-vision-pipeline)
  - [Mathematical Logic](#mathematical-logic)
  - [Software-Based PWM](#software-based-pwm)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Disclaimer](#disclaimer)

---

## 🧠 Concept and Theory

### Computer Vision Pipeline
The core of this project relies on **OpenCV** to interpret the physical world. The pipeline follows these steps:

1.  **Color Isolation (`cv2.inRange`):** The system takes a video feed and converts it from BGR to HSV color space. It isolates a specific object (e.g., a green rectangle) by masking out all pixels that do not fall within the defined color thresholds.
2.  **Contour Detection (`cv2.findContours`):** The binary mask is analyzed to find the shapes (contours) of the isolated object.
3.  **Rotated Bounding Box (`cv2.minAreaRect`):** This is the critical function. Unlike a standard bounding box, `minAreaRect` returns a `Box2D` structure containing the `(center(x,y), (width, height), angle of rotation)`.

### Mathematical Logic
The software calculates the steering intensity based on the slope of the object's principal axis.

Let $\theta$ be the angle of inclination of the rectangle relative to the horizontal axis.

* **Neutral Position:** $\theta \approx 0^\circ$ (Car moves straight, 'W' is pressed).
* **Turning:** As $\theta$ deviates from $0$, the system calculates a steering magnitude $M$.

$$M = \frac{|\theta|}{\theta_{max}}$$

Where $\theta_{max}$ is the maximum rotation angle defined in the settings (e.g., 90 degrees).

### Software-Based PWM (Pulse Width Modulation)
Standard keyboards are binary: a key is either **Pressed (1)** or **Released (0)**. Real steering wheels are analog (0.0 to 1.0). To bridge this gap, we use Pulse Width Modulation.

The **Duty Cycle ($D$)** of the keystroke is directly proportional to the steering magnitude $M$.

* **Slight Turn ($Low \ M$):** The code taps the key.
    * *Example:* 50ms ON, 100ms OFF.
* **Sharp Turn ($High \ M$):** The code holds the key.
    * *Example:* 100ms ON, 0ms OFF (Constant signal).

This rapid toggling tricks the game physics engine into perceiving a partial input, resulting in a smooth curve rather than a jerky 45-degree turn.

---

## ⭐ Features

* **Real-Time Object Tracking:** utilizes high-speed contour detection to track a physical steering object with low latency.
* **DirectX Input Injection:** Uses the `pydirectinput` library instead of standard `pyautogui`. This sends hardware-level scancodes, ensuring compatibility with games like **Roblox**, GTA V, and other DirectX-based applications that ignore standard software keystrokes.
* **Dynamic PWM Steering:** Adjusts the frequency of key presses based on the steepness of the object's slope.
* **Visual Debugging Overlay:** Displays the calculated bounding box, the current angle $\theta$, and the active key state on the webcam feed for easy calibration.
* **Deadzone Configuration:** Includes a software deadzone (e.g., $\pm 5^\circ$) to prevent accidental steering when driving straight.

---

## 🛠 Prerequisites

To run this project, you will need Python installed along with the following libraries:

```bash
pip install opencv-python numpy pydirectinput keyboard
```
* **OpenCV**: For image processing.
* **NumPy**: For mathematical operations.
* **PyDirectInput**: To control the keyboard in games.

## ⚖️ Technical Disclaimer & Operational Constraints

**1. Synthetic Input Injection & Anti-Cheat Heuristics**
This software utilizes `pydirectinput`, which interfaces with the **Win32 `SendInput` API** to generate hardware-level scancodes. While this bypasses standard software-level hooks, modern heuristic-based anti-cheat systems (including **Roblox's Hyperion/Byfron**, BattlEye, or EAC) may analyze input timing distribution.
* **Risk:** The Pulse Width Modulation (PWM) algorithm generates rhythmic, mathematically perfect input patterns. Anti-cheat engines may flag this low-entropy data as "botting" or "macro-assisted" behavior. Use at your own risk in multiplayer environments.

**2. Input Buffer Saturation**
The PWM control loop operates at high frequencies to simulate analog voltage.
* **Constraint:** On standard non-real-time operating systems (Windows), the OS Input Buffer has a finite polling rate. Setting the `PWM_FREQUENCY` too high (>60Hz) combined with computationally expensive CV operations may cause **Input Interrupt collisions**. This can result in "phantom keys" (keys remaining pressed after the software stops) or significant input latency due to thread scheduling jitter.

**3. Non-Deterministic Control Loop**
Unlike a hardware potentiometer, this system relies on computer vision inference (`cv2.minAreaRect`).
* **Safety Warning:** The control signal is strictly dependent on environmental HSV consistency. Specular highlights, shadow occlusion, or rapid lighting changes can cause **contour detection artifacts**, resulting in immediate, unintended full-lock steering maneuvers. Do not use this software for controlling physical hardware (RC cars, drones) where safety is a concern.