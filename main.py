from flask import Flask, render_template, request, Response
import computer_vision as cv
from computer_vision import keybinds_dict, update_keybinds_dict, get_keybinds_dict
import cv2


app = Flask(__name__)

@app.route('/get_dicts', methods=['GET'])
def get_dicts():
    return get_keybinds_dict(), 200

@app.route('/update_dicts', methods=['POST'])
def update_dicts():
    # Update keybinds_dict in computer_vision.py
    print("test", request.json['keybinds_dict'])
    update_keybinds_dict(request.json['keybinds_dict'])
    
    return 'Dictionaries updated', 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_images', methods=['POST'])
def create_images():
    cv.create_images()
    return 'Images created successfully'

@app.route('/create_data', methods=['POST'])
def create_data():
    cv.create_data()
    return 'Data created successfully'

@app.route('/train_classifier', methods=['POST'])
def train_classifier():
    cv.train_classifier()
    return 'Classifier trained successfully'

@app.route('/inference_classifier', methods=['POST'])
def inference_classifier():
    
    cv.inference_classifer()
    return 'Inference classifier run successfully'

@app.route('/get_folder_list', methods=['GET'])
def folder_list():
    print(cv.get_all_folders())
    return cv.get_all_folders(), 200

@app.route('/create_folder', methods=['POST'])
def create_folder():
    cv.create_new_folder(request.json['folder_name'])
    cv.update_folder_name(request.json['folder_name'])
    return 'Folder created successfully'

@app.route('/set_folder_name', methods=['POST'])
def set_folder_name():
    cv.update_folder_name(request.json['folder_name'])
    return 'Folder name updated successfully'


if __name__ == '__main__':
    app.run(debug=True)

