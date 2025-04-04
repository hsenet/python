import cv2

# Use openCV to recognise the face

def recognize_faces():
    """Recognizes faces from the laptop camera."""

    # Load the pre-trained Haar cascade classifier for face detection.
    # You may need to download 'haarcascade_frontalface_default.xml'
    # and place it in the same directory as this script, or provide the full path.
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    if face_cascade.empty():
        raise IOError('Unable to load the face cascade classifier')

    # Open the default camera (camera index 0).
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera.
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale for face detection.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame.
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3, # Adjust scaleFactor for better detection
            minNeighbors=5,  # Adjust minNeighbors to reduce false positives
            minSize=(30, 30) # Minimum face size
        )

        # Draw rectangles around the detected faces.
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Green rectangle

        # Display the frame with detected faces.
        cv2.imshow('Face Recognition', frame)

        # Exit the loop when the 'q' key is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window.
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()