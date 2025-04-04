import cv2
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_name_mappings():
    """Load the name mappings from names.txt"""
    names = {}
    with open("names.txt", "r") as f:
        for line in f:
            face_id, name = line.strip().split(":")
            names[int(face_id)] = name
    return names

def recognize_faces():
    """Recognizes faces from the laptop camera."""

    # Load the trained model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        raise IOError('Unable to load the face cascade classifier')

    # Load name mappings
    names = load_name_mappings()
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            # Recognize the face
            roi_gray = gray[y:y+h, x:x+w]
            id_, confidence = recognizer.predict(roi_gray)
            
            # If confidence is less than 100, it's a perfect match
            # Lower confidence is better
            if confidence < 100:
                name = names.get(id_, "unknown")
                confidence_text = f"{round(100 - confidence)}%"
                logger.info(f"Detected {name} with confidence {confidence_text}")
            else:
                name = "unknown"
                confidence_text = f"{round(100 - confidence)}%"
            
            # Draw rectangle and put text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x+5, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, confidence_text, (x+5, y+h-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()