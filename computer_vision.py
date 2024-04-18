import os
import pickle
import time
import mediapipe as mp
import matplotlib.pyplot as plt
import cv2
import pyautogui
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.preprocessing.sequence import pad_sequences

folder_name = 'deafult'

def get_keybinds_dict(folder_name):
    print('Getting keybinds dict')

    try: 
        keybinds_dict = pickle.load(open(f'data/{folder_name}/keybinds_dict.p', 'rb'))
    except Exception as e:
        keybinds_dict = {}
    print(keybinds_dict)
    return keybinds_dict

def update_keybinds_dict(new_dict, folder_name):
    global keybinds_dict
    
    pickle.dump(new_dict, open(f'data/{folder_name}/keybinds_dict.p', 'wb'))
    
    keybinds_dict = new_dict
    
    
def update_folder_name(new_folder_name):
    global folder_name
    folder_name = new_folder_name
    print('Folder name updated to: ', new_folder_name)
 

def get_all_folders():
    folders = [f for f in os.listdir('data') if os.path.isdir(os.path.join('data', f))]
    print(folders)
    print(folders)
    return folders

def create_new_folder(new_folder_name):
    folder_name = 'data/'+new_folder_name
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        return True
    print(folder_name)
    return False
    
def create_images(folder_name, keybinds_dict):
    print('Creating images')
    print('Keybinds dict: ', keybinds_dict)
    DATA_DIR = f'./data/{folder_name}/data'
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    number_of_classes = len(keybinds_dict)
    print('Number of classes: {}'.format(number_of_classes))
    dataset_size = 100
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.2, min_tracking_confidence=0.2, max_num_hands=1)     
    
    cap = cv2.VideoCapture(0)
    for key in keybinds_dict:
        name = keybinds_dict[key]
        print('Name: ', name)
        print('Key: ', key)
        
        if not os.path.exists(os.path.join(DATA_DIR, str(key))):
            os.makedirs(os.path.join(DATA_DIR, str(key)))

        print('Collecting data for {}'.format(key))

        done = False
        while True:
            ret, frame = cap.read()
            
            results = hands.process(frame)
            if results.multi_hand_landmarks:
                # Only consider the first hand
                hand_landmarks = results.multi_hand_landmarks[0]

                mp_drawing.draw_landmarks(
                    frame,  # image to draw
                    hand_landmarks,  # model output
                    mp_hands.HAND_CONNECTIONS,  # hand connections
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
            
            cv2.putText(frame, 'Press "Q" to record: '+key, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 20, 20), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            
            if cv2.waitKey(25) == ord('q'):
                break

        counter = 0
        while counter < dataset_size:
            ret, frame = cap.read()
            results = hands.process(frame)
            if results.multi_hand_landmarks:
                # Only consider the first hand
                hand_landmarks = results.multi_hand_landmarks[0]

                mp_drawing.draw_landmarks(
                    frame,  # image to draw
                    hand_landmarks,  # model output
                    mp_hands.HAND_CONNECTIONS,  # hand connections
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
            
            cv2.imshow('frame', frame)
            cv2.waitKey(25)  
            cv2.imwrite(os.path.join(DATA_DIR, str(key), '{}.jpg'.format(counter)), frame)
            
            counter += 1

    cap.release()
    cv2.destroyAllWindows()


def create_data(folder_name):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    DATA_DIR = f'data/{folder_name}/data'

    data = []
    labels = []
    for dir_ in os.listdir(DATA_DIR):
        for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
            data_aux = []

            x_ = []
            y_ = []

            img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                data.append(data_aux)
                labels.append(dir_)

    f = open(f'data/{folder_name}/data.pickle', 'wb')
    pickle.dump({'data': data, 'labels': labels}, f)
    f.close()

def train_classifier(folder_name):
    data_dict = pickle.load(open(f'./data/{folder_name}/data.pickle', 'rb'))
    data_padded = pad_sequences(data_dict['data'], maxlen=84, dtype='float32', padding='post')

    shapes = [np.array(item).shape for item in data_dict['data']]
    unique_shapes = set(shapes)

    print(f"Unique shapes in data: {unique_shapes}")
    
    data = data_padded
    labels = np.asarray(data_dict['labels'])

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

    model = RandomForestClassifier()

    model.fit(x_train, y_train)

    y_predict = model.predict(x_test)

    score = accuracy_score(y_predict, y_test)

    print('{}% of samples were classified correctly !'.format(score * 100))

    f = open(f'data/{folder_name}/model.p', 'wb')
    pickle.dump({'model': model}, f)
    f.close()


def inference_classifer(folder_name, keybinds_dict):
    print('Directory: ', folder_name)
    model_dict = pickle.load(open(f'data/{folder_name}/model.p', 'rb'))
    model = model_dict['model']
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Error: Failed to capture frame.")
            
            break  # Exit the loop if no frame is captured
        data_aux = []
        x_ = []
        y_ = []


        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            # Only consider the first hand
            hand_landmarks = results.multi_hand_landmarks[0]

            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            try: 
                data_aux_padded = pad_sequences([data_aux], maxlen=84, dtype='float32', padding='post', truncating='post')[0]  # Pads/truncates to 84 features
                
              
                probs = model.predict_proba([data_aux_padded])[0]  # Get class probabilities
                max_prob = np.max(probs)  # Find maximum probability
                predicted_class_index = np.argmax(probs)  # Find class index with max probability

                confidence_threshold = 0.85

                if max_prob > confidence_threshold:
                    predicted_class_label = model.classes_[predicted_class_index]  # This gets the class label (ensure alignment with keybinds_dict)
                    if predicted_class_label in keybinds_dict:
                        gesture_name = keybinds_dict[predicted_class_label]
                        print(f"Predicted gesture: {gesture_name} with confidence: {max_prob * 100:.2f}%")
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                        cv2.putText(frame, gesture_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
                        try:
                            pyautogui.press(gesture_name)
                        except Exception as e:
                            print(f"Action error: {str(e)}")
                    else:
                        print(f"No keybind found for predicted class: {predicted_class_label}")
                else:
                    pass

                
            except Exception as e:
                print(f'Error: {str(e)}')

           
        cv2.imshow('frame', frame)
        if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:  
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Also allows exiting with 'q'
            break
        
        cv2.waitKey(1)
        

    cap.release()
    cv2.destroyAllWindows()