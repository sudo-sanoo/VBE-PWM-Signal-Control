import cv2
import time

class Camera:
    def __init__(self, camera_index=0+cv2.CAP_DSHOW):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise IOError("Failed to open webcam")
        print("Camera successfully initialized..")
        time.sleep(1)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def release_camera(self):
        self.cap.release()
        print("Camera released")

def main():
    cam = Camera()
    print("Press 'q' to quit video steam.")

    while True:
        frame = cam.get_frame()

        if frame is not None:
            frame = cv2.flip(frame, 1)
            cv2.imshow("VBE-PWM Signal Control", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break

    cam.release_camera()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()