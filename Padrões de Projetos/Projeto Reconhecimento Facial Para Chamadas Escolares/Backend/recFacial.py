import face_recognition
import cv2
import numpy as np


# "0"is the webcam, if you want to play the video put the example file path Imagens\Isaac.mp4
video_capture = cv2.VideoCapture(0)

obama_image = face_recognition.load_image_file("backend\\Imagens\\obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]


biden_image = face_recognition.load_image_file("backend\Imagens\Biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

isaac_image = face_recognition.load_image_file("backend\Imagens\imagemUm.jpg")
isaac_face_encoding = face_recognition.face_encodings(isaac_image)[0]

joao_image = face_recognition.load_image_file("backend\Imagens\joao.jpg")
joao_face_encoding = face_recognition.face_encodings(joao_image)[0]


karen_image = face_recognition.load_image_file("backend\Imagens\karen.jpg")
karen_face_encoding = face_recognition.face_encodings(karen_image)[0]

jack_image = face_recognition.load_image_file("backend\Imagens\Jack1.jpeg")
jack_face_encoding = face_recognition.face_encodings(jack_image)[0]

eduarda_image = face_recognition.load_image_file("backend\Imagens\Eduarda.jpg")
eduarda_face_encoding = face_recognition.face_encodings(eduarda_image)[0]

gabriel_image = face_recognition.load_image_file(
    "backend\Imagens\Gabriel.jpeg")
gabriel_face_encoding = face_recognition.face_encodings(gabriel_image)[0]


known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    joao_face_encoding,
    isaac_face_encoding,
    karen_face_encoding,
    jack_face_encoding,
    eduarda_face_encoding,
    gabriel_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Joao",
    "Isaac",
    "Karen",
    "Jackson",
    "Eduarda",
    "Gabriel"
]


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:

    ret, frame = video_capture.read()

    if process_this_frame:

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
