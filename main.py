from flask import Flask, render_template, request, Response
from flask_cors import CORS
import computer_vision as cv
from computer_vision import update_keybinds_dict, get_keybinds_dict
import cv2


app = Flask(__name__)
CORS(app)

@app.route('/get_dicts', methods=['GET'])
def get_dicts():
    folder_name = request.args.get('folder')
    return get_keybinds_dict(folder_name), 200

@app.route('/update_dicts', methods=['POST'])
def update_dicts():
    update_keybinds_dict(request.json['keybinds_dict'], request.json['folder_name'])
    return 'Dictionaries updated', 200


@app.route('/create_images', methods=['POST'])
def create_images():
    cv.create_images(request.json['folder_name'], request.json['keybinds_dict'])
    cv.create_data(request.json['folder_name'])
    cv.train_classifier(request.json['folder_name'])
    return 'Images created successfully'

@app.route('/inference_classifier', methods=['POST'])
def inference_classifier():
    cv.inference_classifer(request.json['folder_name'], request.json['keybinds_dict'])
    return 'Inference classifier run successfully'

@app.route('/get_folder_list', methods=['GET'])
def folder_list():
    print(cv.get_all_folders())
    return cv.get_all_folders(), 200

@app.route('/create_folder', methods=['POST'])
def create_folder():
    cv.create_new_folder(request.json['folder_name'])
    return 'Folder created successfully'

@app.route('/set_folder_name', methods=['POST'])
def set_folder_name():
    cv.update_folder_name(request.json['folder_name'])
    return 'Folder name updated successfully'


if __name__ == '__main__':
    app.run(debug=True)

