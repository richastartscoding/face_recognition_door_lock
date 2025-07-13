import face_recognition
import cv2
import numpy as np
import os
import time
import serial
from tkinter import Tk, Label
from PIL import Image, ImageTk
from datetime import datetime
import csv
import requests


BOT_TOKEN = ""
CHAT_ID = ""
SERIAL_PORT = "COM3" 
BAUD_RATE = 9600



# Serial connection to Arduino
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
    time.sleep(2)
    print(" Connected to Arduino.")
except:
    print(" Could not connect to Arduino.")
    arduino = None

# Load known face encodings
known_face_encodings = []
known_face_names = []

if not os.path.exists("train_faces"):
    os.mkdir("train_faces")

for filename in os.listdir("train_faces"):
    if filename.endswith((".jpg", ".png")):
        image = face_recognition.load_image_file(f"train_faces/{filename}")
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])

# Create folders if not present
if not os.path.exists("captures"):
    os.mkdir("captures")

if not os.path.exists("unauthorized_log.csv"):
    with open("unauthorized_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Status", "Image_Name"])

# GUI setup
root = Tk()
root.title("Smart Door Lock")
root.geometry("400x100")
status_label = Label(root, text="Initializing...", font=("Helvetica", 16), fg="blue")
status_label.pack()

def update_status(message, color="black"):
    status_label.config(text=message, fg=color)
    root.update()

update_status("System Ready", "green")

# Start webcam
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
video_capture.set(cv2.CAP_PROP_BRIGHTNESS, 0.3)

skip_frames = 0
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    if skip_frames > 0:
        skip_frames -= 1
        cv2.imshow("Smart Door Lock", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches and matches[best_match_index]:
            name = known_face_names[best_match_index]
            update_status(f"Access Granted: {name}", "green")
            print(f"[{datetime.now()}] ✅ Access Granted to {name}")

            # Optional: display name on screen
            cv2.putText(frame, f"Welcome, {name}", (left * 4, top * 4 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if arduino:
                arduino.write(b'o')  # Open servo
                print(" Door unlocked")
                time.sleep(1.5)
                arduino.write(b'c')  # Close servo
                print(" Door locked")

            skip_frames = 60  # Skip next 60 frames (~2 seconds at 30fps)

        else:
            update_status("Unauthorized Attempt!", "red")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_name = f"unauthorized_{timestamp}.jpg"
            image_path = f"captures/{image_name}"

            # Save unauthorized image
            cv2.imwrite(image_path, frame)

            # Log to CSV
            with open("unauthorized_log.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Unauthorized", image_name])

            print(f"[{datetime.now()}] ❌ Unauthorized access - Locked")

            # Send Telegram Alert
            try:
                alert_msg = f"🚨 Unauthorized access attempt at {timestamp}"
                requests.get(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    params={"chat_id": CHAT_ID, "text": alert_msg}
                )

                with open(image_path, 'rb') as photo:
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                        data={"chat_id": CHAT_ID},
                        files={"photo": photo}
                    )

            except Exception as e:
                print(f" Telegram alert failed: {e}")

            skip_frames = 60  # Prevent duplicate alerts

    cv2.imshow("Smart Door Lock", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
root.destroy()
