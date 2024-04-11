# Hand Symbol Detector and Controller
#### Lilly Moreau

This project is a static gesture detector that allows you to press computer keys using hand symbol. It uses computer vision techniques to recognize predefined hand gestures and trigger corresponding actions.
 

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies by running the following command:

    ```bash
    $ pip install -r requirements.txt
    ```

## Usage

1. Need a camera for your laptop. It should use your built in camera by deafult
2. Run the following command to start the gesture detector:

    ```bash
    $ python main.py
    ```

3. Follow the instructions displayed on the website to create a model and custom keybind.
4. The program will recognize the gestures and trigger the corresponding actions.

## Tech Stack
#### Frontend: HTML
- The frontend is a simple HTML page for demo purposes. It includes scripts for handling user interactions, such as creating keybinds, recording images, training the model, and running the classifier.
#### Backend: Python
- The backend includes a Flask server that handles various routes for managing keybinds, creating images, training the classifier, and running the classifier.
#### Computer Vision: OpenCV and MediaPipe
- OpenCV is a library of programming functions mainly aimed at real-time computer vision. 
- MediaPipe offers customizable machine learning solutions for live and streaming media.
#### Machine Learning: Scikit-learn
- Scikit-learn is a free software machine learning library for Python. It features various classification, regression, and clustering algorithms.

[![Inspired by this video](https://img.youtube.com/vi/MJCSjXepaAM/0.jpg)](https://www.youtube.com/watch?v=MJCSjXepaAM)
