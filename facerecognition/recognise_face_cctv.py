import cv2
import logging
import os
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_name_mappings():
    """Load the trained mappings from faces.txt"""
    names = {}
    with open("faces.txt", "r") as f:
        for line in f:
            face_id, name = line.strip().split(":")
            names[int(face_id)] = name
    return names

def recognize_faces(rtsp_url):
    """
    Recognizes faces from RTSP stream.
    Args:
        rtsp_url: RTSP stream URL (e.g., 'rtsp://username:password@ip:port/path')
    """
    # Load the trained model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        raise IOError('Unable to load the face cascade classifier')

    # Load name mappings
    names = load_name_mappings()
    
    # Configure RTSP stream
    cap = cv2.VideoCapture(rtsp_url)
    
    # Optimize RTSP stream settings
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)  # Reduce buffer size
    
    # Connection retry loop
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        if not cap.isOpened():
            logger.error(f"Failed to connect to RTSP stream. Attempt {retry_count + 1}/{max_retries}")
            time.sleep(2)  # Wait before retrying
            cap = cv2.VideoCapture(rtsp_url)
            retry_count += 1
            continue
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.error("Failed to read frame from stream")
                    break

                # Process frame
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

                # Add FPS counter
                fps = cap.get(cv2.CAP_PROP_FPS)
                cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow('RTSP Face Recognition', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return  # Clean exit

        except Exception as e:
            logger.error(f"Stream processing error: {str(e)}")
            retry_count += 1
            time.sleep(2)  # Wait before retrying
            cap = cv2.VideoCapture(rtsp_url)
            continue

    logger.error("Max retries reached. Exiting.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Replace with your RTSP stream URL
    rtsp_url = "rtsp://hsenet:cam123@192.168.1.165:554/stream2"
    
    try:
        recognize_faces(rtsp_url)
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
    finally:
        cv2.destroyAllWindows()
