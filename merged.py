import streamlit as st
import cv2
import numpy as np
import time
import face_recognition
from datetime import datetime

# Specify the path to your attendance file
attendance_file_path = "attendance.txt"

# Function to load known faces from images and their corresponding names
def load_known_faces(known_faces):
    known_face_encodings = []
    known_face_names = []

    for face_image, name in known_faces:
        img = face_recognition.load_image_file(face_image)
        face_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

    return known_face_encodings, known_face_names

# Example: Load known faces with their names (Add your own images and names)
known_faces = [
    ("0.jpg", "Aryaveer"),
    ("1.jpg", "Hrithik"),
    # Add more images and corresponding names as needed
]

known_face_encodings, known_face_names = load_known_faces(known_faces)

# Function to capture webcam feed
def capture_webcam():
    # Open a connection to the webcam (0 represents the default webcam)
    webcam = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not webcam.isOpened():
        st.error("Could not open webcam")
        return

    # Create a text file to store attendance
    with open(attendance_file_path, "a") as attendance_file:
        attendance_file.write("Attendance Log\n")

    attendance_marked = set()  # Set to store names for which attendance is already marked

    # Continuously capture frames from the webcam
    while st.session_state.webcam_running:  # Use session state to control the loop
        # Read a frame from the webcam
        status, frame = webcam.read()

        # Check if the frame is read successfully
        if not status:
            st.error("Could not read frame")
            break

        # Resize the frame to a smaller size for display
        small_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find faces in the current frame
        face_locations = face_recognition.face_locations(frame_rgb)
        face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

        # Loop through detected faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]

                # Mark attendance only if the person is not already marked
                if name not in attendance_marked:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(attendance_file_path, "a") as attendance_file:
                        attendance_file.write(f"{name} - {timestamp}\n")
                    attendance_marked.add(name)

            # Draw a rectangle around the face
            cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw the name below the face
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(small_frame, name, (left + 6, bottom + 30), font, 0.8, (255, 255, 255), 1)

        # Display the webcam feed with bounding boxes and names
        st.image(small_frame, channels="RGB", use_column_width=True)

        # Wait for a short time (e.g., 1 second) before processing the next frame
        time.sleep(1)

    # Release the webcam
    webcam.release()

# Streamlit app to display webcam feed and attendance data
st.title("Webcam with Face Recognition")

# Display the "Start Webcam" button on the left side
start_webcam_button = st.button("Start Webcam")
if start_webcam_button:
    # Run the webcam feed in a separate thread
    st.session_state.webcam_running = True  # Use session state to control the loop
    st.success("Webcam started successfully!")
    capture_webcam()
    st.session_state.webcam_running = False  # Reset session state

# Display attendance data on the right side
show_attendance_button = st.sidebar.button("Show Attendance")
if show_attendance_button:
    with open(attendance_file_path, "r") as attendance_file:
        attendance_data = attendance_file.read()
        st.sidebar.text(attendance_data)
