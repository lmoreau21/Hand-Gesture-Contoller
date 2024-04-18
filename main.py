from flask import Flask, request
from flask_cors import CORS
import computer_vision as cv
from computer_vision import update_keybinds_dict, get_keybinds_dict

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
    """
    Creates images for hand gestures based on the provided folder name and keybinds dictionary.
    Then, it creates data and trains the classifier using the created images.
    
    Returns:
        str: A success message indicating that the images were created successfully.
    """
    cv.create_images(request.json['folder_name'], request.json['keybinds_dict'])
    cv.create_data(request.json['folder_name'])
    cv.train_classifier(request.json['folder_name'])
    return 'Images created successfully'

@app.route('/inference_classifier', methods=['POST'])
def inference_classifier():
    """
    Run the inference classifier using the provided folder name and keybinds dictionary.

    Returns:
        str: A message indicating the successful execution of the inference classifier.
    """
    cv.inference_classifer(request.json['folder_name'], request.json['keybinds_dict'])
    return 'Inference classifier run successfully'

@app.route('/get_folder_list', methods=['GET'])
def folder_list():
    """
    Retrieves a list of all folders using the cv module.
    
    Returns:
        A tuple containing the list of folders and the HTTP status code 200.
    """
    print(cv.get_all_folders())
    return cv.get_all_folders(), 200

@app.route('/create_folder', methods=['POST'])
def create_folder():
    """
    Creates a new folder based on the provided folder name.

    Args:
    - folder_name (str): The name of the folder to be created.

    Returns:
    - str: A success message indicating that the folder was created successfully.
    """
    cv.create_new_folder(request.json['folder_name'])
    return 'Folder created successfully'


if __name__ == '__main__':
    app.run(debug=True)

