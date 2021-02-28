import cv2 as cv2


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    face_classifier = cv2.CascadeClassifier('./harcascade/haarcascade_frontalface_default.xml')

    eye_classifier = cv2.CascadeClassifier('./harcascade/haarcascade_eye.xml')

    while True:
        ret, frame = cap.read()
        print(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        print(len(faces))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0))
            eye_gray = gray[y:y + h, x:x + w]
            eye_color = frame[y:y + h, x:x + w]
            eyes = eye_classifier.detectMultiScale(eye_gray)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(eye_color, (ex, ey), (ey + ew, ey + eh), (0, 255, 0), 2)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyWindow()
