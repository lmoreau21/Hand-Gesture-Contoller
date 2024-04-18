# Hand Symbol Detector and Controller
#### Lilly Moreau

This project is a static gesture detector that allows you to press computer keys using hand symbol. It uses computer vision techniques to recognize predefined hand gestures and trigger corresponding actions.
 
## Requierements
* Python 3.10+
* Node.js

## Installation
1. Clone this repository to your local machine.
2. Create a virtual environment and activiate it
3. Install the required dependencies by running the following command:

    ```bash
    $ pip install -r requirements.txt
    ```
4. Change to frontend directory
    ```bash
    $ cd frontend
    ```
5. Install react dependecies
    ```bash
    $ npm install
    ```


## Usage
1. Change to frontend directory
2. Run the following command to run the frontend and the backend

    ```bash
    $ npm start
    ```
2. Need a camera for your laptop. It should use your built in camera by deafult
3. Should load website on this link: http://localhost:3000/
4. Follow the instructions displayed on the website to create a model and custom keybind.
5. The program will recognize the gestures and trigger the corresponding actions.

## Tech Stack
#### Frontend: React
- The frontend is a one page react page. It includes buttons for handling user interactions, such as creating keybinds, recording images, training the model, and running the classifier.
#### Backend: Python
- The backend includes a Flask server that handles various routes for managing keybinds, creating images, training the classifier, and running the classifier.
#### Computer Vision: OpenCV and MediaPipe
- OpenCV is a library of programming functions mainly aimed at real-time computer vision. 
- MediaPipe offers customizable machine learning solutions for live and streaming media.
#### Machine Learning: Scikit-learn
- Scikit-learn is a free software machine learning library for Python. It features various classification, regression, and clustering algorithms.

[![Demo Video]](https://www.youtube.com/watch?v=GkLSWfltXjA)
[![Intial project inspired by this youtube video]](https://www.youtube.com/watch?v=MJCSjXepaAM)
