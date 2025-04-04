import cv2
import pickle
import mediapipe as mp
import numpy as np

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
labels_dict = {'Letter_A' : 'A', 'Letter_B' : 'B', 'Letter_C' : 'C', 'Letter_L': 'L' }
while True:
    data_aux = []
    x_ = []
    y_ = []
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        continue  # Skip this iteration if the frame is empty
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
                x_.append(x)
                y_.append(y)
        x1= int(min(x_) * W) -10
        y1 = int(min(y_) * H) -10

        x2 = int(max(x_) * W) -10
        y2 = int(max(y_) * H) -10
        prediction = model.predict([np.asarray(data_aux)])
        predicted_value = labels_dict[(prediction[0])]
        #print(predicted_value)


        cv2.rectangle(frame,(x1,y1), (x2,y2),(0,0,0), 4)
        cv2.putText(frame, predicted_value, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1.3,(0,0,0),3,cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
