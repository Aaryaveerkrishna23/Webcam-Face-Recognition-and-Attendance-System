# Webcam-Face-Recognition-and-Attendance-System
This project implements a real-time webcam face recognition system with attendance logging. The application is built using Python, OpenCV, face_recognition, and Streamlit.

[Link to My Video](https://drive.google.com/file/d/1zzOF8KITbfT6efRL0zU7ubV8Sm4eNJOh/view?usp=sharing)

## Features

- **Webcam Face Recognition:**
  - Uses face_recognition library for real-time face detection and recognition.
  - Recognizes faces from a pre-defined set of known faces.

- **Attendance System:**
  - Logs the attendance with timestamps when recognized faces appear on the webcam feed.
  - Attendance data is stored in a text file (`attendance.txt`).

- **Streamlit Web App:**
  - Utilizes Streamlit to create a user-friendly web interface.
  - Allows starting the webcam feed and displaying attendance data.
- **Run the Application**:
  -streamlit run app.py
  -Click on the "Start Webcam" button to initiate face recognition.
  -View attendance data on the right sidebar.
- **Additional Notes**
  -This project is based on the OpenCV and face_recognition libraries.
  -Ensure you have a working webcam connected to your machine.
## Dependencies

- **Python Version:**
  - 3.11.3
  - dlib==19.22.0
  - opencv-python==4.5.1
  - streamlit==1.0.0
face_recognition==1.3.0
