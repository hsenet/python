import cv2
import logging
import os
import time
import numpy as np
import requests
from urllib.parse import urlparse
import threading
from queue import Queue
import concurrent.futures

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamProcessor:
    def __init__(self, stream_url, stream_name, recognizer, face_cascade, names):
        self.stream_url = stream_url
        self.stream_name = stream_name
        self.recognizer = recognizer
        self.face_cascade = face_cascade
        self.names = names
        self.running = False
        self.last_frame_time = time.time()
        self.fps = 0
        self.frame_queue = Queue(maxsize=10)
        self.retry_count = 0
        self.max_retries = 5

    def start(self):
        """Start processing the stream"""
        self.running = True
        # Start capture thread
        self.capture_thread = threading.Thread(target=self.capture_stream)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        # Start processing thread
        self.process_thread = threading.Thread(target=self.process_frames)
        self.process_thread.daemon = True
        self.process_thread.start()

    def stop(self):
        """Stop processing the stream"""
        self.running = False
        if hasattr(self, 'cap'):
            self.cap.release()

    def capture_stream(self):
        """Capture frames from the stream"""
        while self.running and self.retry_count < self.max_retries:
            try:
                self.cap = cv2.VideoCapture(self.stream_url)
                if not self.cap.isOpened():
                    raise Exception("Failed to open stream")

                while self.running:
                    ret, frame = self.cap.read()
                    if not ret:
                        raise Exception("Failed to read frame")
                    
                    if not self.frame_queue.full():
                        self.frame_queue.put(frame)
                    
                    # Reset retry count on successful frame
                    self.retry_count = 0

            except Exception as e:
                logger.error(f"Stream {self.stream_name} error: {str(e)}")
                self.retry_count += 1
                time.sleep(2)
                continue

    def process_frames(self):
        """Process frames from the queue"""
        while self.running:
            try:
                if not self.frame_queue.empty():
                    frame = self.frame_queue.get()
                    
                    # Calculate FPS
                    current_time = time.time()
                    self.fps = 1 / (current_time - self.last_frame_time)
                    self.last_frame_time = current_time

                    # Process frame
                    processed_frame = self.process_single_frame(frame)
                    
                    # Display the frame
                    cv2.imshow(f'Stream: {self.stream_name}', processed_frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.running = False
                        break
            except Exception as e:
                logger.error(f"Processing error in {self.stream_name}: {str(e)}")
                continue

    def process_single_frame(self, frame):
        """Process a single frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            id_, confidence = self.recognizer.predict(roi_gray)
            
            if confidence < 100:
                name = self.names.get(id_, "unknown")
                confidence_text = f"{round(100 - confidence)}%"
                logger.info(f"Stream {self.stream_name}: Detected {name} with confidence {confidence_text}")
            else:
                name = "unknown"
                confidence_text = f"{round(100 - confidence)}%"
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x+5, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, confidence_text, (x+5, y+h-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

        # Add FPS and stream info
        cv2.putText(frame, f'FPS: {self.fps:.1f}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Stream: {self.stream_name}', (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame

def load_name_mappings():
    """Load the trained mappings from faces.txt"""
    names = {}
    with open("faces.txt", "r") as f:
        for line in f:
            face_id, name = line.strip().split(":")
            names[int(face_id)] = name
    return names

def is_valid_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def process_multiple_streams(stream_configs):
    """
    Process multiple streams simultaneously
    Args:
        stream_configs: List of dictionaries containing stream URLs and names
    """
    # Load face recognition resources
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        raise IOError('Unable to load the face cascade classifier')

    names = load_name_mappings()

    # Create stream processors
    processors = []
    for config in stream_configs:
        if not is_valid_url(config['url']):
            logger.error(f"Invalid URL format for stream {config['name']}")
            continue
            
        processor = StreamProcessor(
            config['url'],
            config['name'],
            recognizer,
            face_cascade,
            names
        )
        processors.append(processor)

    # Start all processors
    for processor in processors:
        processor.start()

    try:
        # Keep main thread alive
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.1)  # Reduce CPU usage

    except KeyboardInterrupt:
        logger.info("Program terminated by user")
    finally:
        # Stop all processors
        for processor in processors:
            processor.stop()
        cv2.destroyAllWindows()

def main():
    stream_configs = [
        {
            "url": "http://singapore:9081",
            "name": "Camera 1"
        },
        {
            "url": "http://singapore:9082",
            "name": "Camera 2"
        },
        {
            "url": "http://d09:9083",
            "name": "Camera 3"
        }
    ]
    
    process_multiple_streams(stream_configs)

if __name__ == "__main__":
    main()
