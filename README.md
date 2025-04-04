# Python Projects: Face Recognition

This repository contains my Python projects, with a primary focus on face recognition.

## 🚀 Face Recognition

This project allows you to detect and recognize faces in a camera feed or stream. It leverages the power of OpenCV for image processing and face detection.

### ✨ Features

*   **Face Detection:**  Identify the location of faces within video streams.
*   **Face Recognition:**  Train a model to recognize specific individuals and identify them in real-time.
*   **Easy to Use:**  Simple command-line interface for training and running the recognition system.

### 🛠️ Installation

1.  **Python:** Ensure you have Python installed. If not, download and install it from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **OpenCV:** Install OpenCV and the `contrib` module, which includes additional algorithms and features, including those used for face recognition. Open your terminal or command prompt and run:

    ```bash
    pip install opencv-python opencv-contrib-python
    ```

### 🕹️ Usage

#### 1. Face Detection (Basic)

To simply detect faces in camera, run the following command:

```bash
python recognise.py
```
#### 2. Face Detection (Advanced)

The trainer script takes pictures and creates data set for you

To train the app, run the folowing command:

```bash
python train_faces.py
```


To  detect faces in the Camera, run the following command:

```bash
python recognise_face.py
```
