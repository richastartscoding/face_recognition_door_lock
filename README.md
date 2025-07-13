# face_recognition_door_lock
It's a prototype of a security system using Open CV , which recognises the authorised persons face image and rotates the servo motor to unlock , and notifies about the unauthorised entry attempts through a telegram bot , also creates a sheet of unauthorised entry attempts timing and their captures.
===================================================
       SMART DOOR LOCK USING FACE RECOGNITION
===================================================

Author: RICHA MUCHHAL  
Date: July 2025  
Language: Python 3.10  
Environment: Conda (faceenv)

---------------------------------------------------
 PROJECT OVERVIEW
---------------------------------------------------
This Smart Door Lock system uses face recognition to control a door lock via Arduino.  
It captures faces through a webcam, matches them with stored encodings,  
and grants or denies access accordingly. Unauthorized access attempts are logged and notified via Telegram.

---------------------------------------------------
 FEATURES
---------------------------------------------------
✔ Real-time face recognition using OpenCV + dlib  
✔ Door control using Arduino + Servo Motor  
✔ Unauthorized attempt logging in CSV  
✔ Image capture of unauthorized attempts  
✔ Telegram alert with image  
✔ GUI status display using Tkinter  


---------------------------------------------------
 HARDWARE CONNECTION
---------------------------------------------------
- Arduino UNO/Nano connected to PC via USB  
- Servo signal pin connected to D9  
- Servo VCC to 5V and GND to GND on Arduino  
- Arduino receives command via Serial:
    'o' = open (unlock)
    'c' = close (lock)

---------------------------------------------------
 INSTALLATION GUIDE
---------------------------------------------------
1. Install Python 3.10 (recommended)
2. Create and activate a virtual environment:
   - `conda create -n faceenv python=3.10`
   - `conda activate faceenv`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Install dlib via conda (recommended for Windows):
   - `conda install -c conda-forge dlib`
5. Add face images of the people you wish to grant access to the `train_faces` folder

---------------------------------------------------
 TELEGRAM ALERT SETUP
---------------------------------------------------
1. Create a Telegram bot via BotFather
2. Get your bot token
3. Get your chat ID using https://api.telegram.org/bot<token>/getUpdates
4. Paste your bot token and chat ID in `door_lock.py`:
   ```python
   BOT_TOKEN = "your_bot_token"
   CHAT_ID = "your_chat_id"
