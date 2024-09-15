import cv2
import numpy as np
import time
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import tkinter as tk
from tkinter import messagebox
from threading import Thread

class MoodDetector:
    def __init__(self, camera_number = 0):
        # Initialization
        self.face_classifier = cv2.CascadeClassifier(r'C:\Expression\haarcascade_frontalface_default.xml')
        self.classifier = load_model(r'C:\Expression\model.h5')
        self.cap = cv2.VideoCapture(camera_number)
        self.emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

        # FPS calculation
        self.new_frame = 0
        self.prev_frame = 0

        # Camera / Frame Dimensions
        self.width = 640
        self.height = 480

        # For mood detection
        self.current_emotion = None
        self.running = True

    def calculateFPS(self):
        self.new_frame = time.time()
        fps = int(1 / (self.new_frame - self.prev_frame))
        self.prev_frame = self.new_frame
        return fps

    def detect_emotion(self):
        while self.running:
            isTrue, frame = self.cap.read()

            frame = cv2.resize(frame, (self.width, self.height))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            fps = self.calculateFPS()
            if fps <= 20:
                cv2.putText(frame, f'FPS: {fps}', (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                cv2.putText(frame, f'FPS: {fps}', (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 1, cv2.LINE_AA)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)
                    prediction = self.classifier.predict(roi)[0]
                    self.current_emotion = self.emotions[prediction.argmax()]
                    label_pos = (x,y)
                    cv2.putText(frame, self.current_emotion, label_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    self.current_emotion = 'No Faces'

            cv2.imshow("Mood Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

        self.cap.release()
        cv2.destroyAllWindows()

    def start_detection(self):
        self.running = True
        self.thread = Thread(target=self.detect_emotion)
        self.thread.start()

    def stop_detection(self):
        self.running = False
        self.thread.join()
        return self.current_emotion



class MoodDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("Mood Based Spofity Recommendations")
        self.detector = MoodDetector()  # Change the camera number if needed

        self.title_label = tk.Label(root, text="WELCOME TO MOOD GROOVE", width=70, height=3, font=('Helvetica', 25))
        self.title_label.pack(padx=5, pady=5)
        self.slogan_label = tk.Label(root, text="Serving you with mood based Spotify song recommendations...Click Start to Begin", width=100, font=("", 10))
        self.slogan_label.pack()

        self.start_button = tk.Button(root, text="START", command=self.start_detection,
                                      width=40, height=5, bg="green")
        self.start_button.pack(pady=10)

        self.capture_button = tk.Button(root, text="CAPTURE", command=self.capture_mood,
                                        width=40, height=5, bg="red")
        self.capture_button.pack(pady=10)

        self.final_mood = ""

    def start_detection(self):
        self.detector.start_detection()

    def retMood(self):
        return self.final_mood

    def capture_mood(self):
        mood = self.detector.stop_detection() # current mood stored in!!!
        self.root.quit()
        self.final_mood = mood
        

# TESTING CODE FOR SINGLE FILE
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MoodDetectorApp(root)
#     root.mainloop()
