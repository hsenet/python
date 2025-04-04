import cv2
import numpy as np
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def collect_face_data(name):
    """Collect face data for training."""
    
    # Create directories if they don't exist
    if not os.path.exists("dataset"):
        os.makedirs("dataset")
    if not os.path.exists("trainer"):
        os.makedirs("trainer")

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    # Get the next available face ID
    face_id = len(os.listdir("dataset")) + 1
    
    count = 0
    logger.info(f"Collecting face data for {name}. Press 'q' to quit.")

    while count < 30:  # Collect 30 face samples
        ret, frame = cap.read()
        # Convert image to grayscale because opencv requires grayscale image
        # for face detection algorithms typically work better with greyscale 
        # since there is only 1 channel to process
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
            
            # Save the face image
            cv2.imwrite(f"dataset/{name}.{face_id}.{count}.jpg",
                       gray[y:y+h, x:x+w])
            
        cv2.imshow('Collecting Faces', frame)
        cv2.waitKey(100)

        if count >= 30:
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # Save the name mapping
    with open("names.txt", "a") as f:
        f.write(f"{face_id}:{name}\n")
    
    logger.info(f"Face data collection completed for {name}")
    return face_id

def train_model():
    """Train the face recognition model."""
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
    logger.info("Training faces. Please wait...")
    
    faces = []
    ids = []
    
    # Get all images from dataset
    for image_file in os.listdir("dataset"):
        if image_file.endswith(".jpg"):
            img_path = os.path.join("dataset", image_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            face_id = int(image_file.split('.')[1])
            faces.append(img)
            ids.append(face_id)
    
    recognizer.train(faces, np.array(ids))
    recognizer.write('trainer/trainer.yml')
    logger.info(f"Training completed. {len(np.unique(ids))} faces trained.")

if __name__ == "__main__":
    while True:
        name = input("Enter name of person (or 'train' to finish collecting data): ")
        if name.lower() == 'train':
            break
        collect_face_data(name)
    
    train_model()
