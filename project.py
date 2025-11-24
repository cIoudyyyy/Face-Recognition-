import face_recognition
import cv2
import pickle
import os

def capture_and_save_face(name):
   
    video_capture = cv2.VideoCapture(0)
    
    
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print("Press 's' to save the face encoding or 'q' to quit.")
    
    while True:
        
        ret, frame = video_capture.read()
        
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        
        cv2.imshow('Video', frame)
        
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s') and len(face_encodings) > 0:
            
            encoding = face_encodings[0]
            with open(f'{name}_face_encoding.pkl', 'wb') as f:
                pickle.dump(encoding, f)
            print(f"Face encoding for {name} saved successfully.")
            break
        elif key == ord('q'):
            break
    
    
    video_capture.release()
    cv2.destroyAllWindows()


def load_face_encoding(name):
    filename = f'{name}_face_encoding.pkl'
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            encoding = pickle.load(f)
        return encoding
    else:
        print(f"No saved encoding found for {name}.")
        return None


if __name__ == "__main__":
    
    person_name = input("Enter the name for the face: ")
    capture_and_save_face(person_name)
    
    
    loaded_encoding = load_face_encoding(person_name)
    if loaded_encoding is not None:
        print(f"Loaded encoding for {person_name}: {loaded_encoding[:5]}...")
