# Multiple faces

from deepface import DeepFace
import cv2

cap = cv2.VideoCapture(0)  # Use 0 for webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # If only one face is detected, wrap it in a list for uniform handling
        if not isinstance(results, list):
            results = [results]

        for face_data in results:
            x = face_data['region']['x']
            y = face_data['region']['y']
            w = face_data['region']['w']
            h = face_data['region']['h']
            emotion = face_data['dominant_emotion']

            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Put text above the face
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

    except Exception as e:
        print("Error:", e)

    cv2.imshow('Emotion Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

