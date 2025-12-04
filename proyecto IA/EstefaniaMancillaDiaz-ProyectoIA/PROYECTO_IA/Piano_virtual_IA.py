import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

KEY_NAMES = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI"]
N_KEYS = len(KEY_NAMES)


def main():
    cap = cv2.VideoCapture(0)

    last_key_index = None

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            index_finger_pos = None
            current_key_index = None
            note_name = "Ninguna"

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                index_tip = hand_landmarks.landmark[8]
                x_tip = int(index_tip.x * w)
                y_tip = int(index_tip.y * h)
                index_finger_pos = (x_tip, y_tip)

                key_width = w / N_KEYS
                key_height = int(h * 0.3)
                y_top = h - key_height

                if y_tip >= y_top:
                    key_index = int(x_tip / key_width)

                    if 0 <= key_index < N_KEYS:
                        current_key_index = key_index
                        note_name = KEY_NAMES[current_key_index]

                        if current_key_index != last_key_index:
                            print(f"Tocaste la nota: {note_name}")
                            last_key_index = current_key_index
                else:
                    last_key_index = None

            key_width = int(w / N_KEYS)
            key_height = int(h * 0.3)
            y_top = h - key_height

            for i in range(N_KEYS):
                x_start = i * key_width
                x_end = x_start + key_width

                color = (255, 255, 255)
                thickness = 2

                if current_key_index == i:
                    color = (0, 255, 255)
                    thickness = -1

                cv2.rectangle(frame, (x_start, y_top), (x_end, h), color, thickness)

                text_x = x_start + 10
                text_y = h - int(key_height * 0.4)
                cv2.putText(frame, KEY_NAMES[i],
                            (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 0), 2)

            if index_finger_pos is not None:
                cv2.circle(frame, index_finger_pos, 10, (0, 0, 255), -1)
                cv2.putText(frame, "Dedo indice",
                            (index_finger_pos[0] + 10, index_finger_pos[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)

            cv2.putText(frame, f"Nota actual: {note_name}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 0) if note_name != 'Ninguna' else (0, 0, 255),
                        2)

            cv2.putText(frame,
                        "Coloca tu dedo indice sobre las teclas (parte baja de la pantalla)",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (255, 255, 255), 2)

            cv2.putText(frame, "Presiona ESC para salir",
                        (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (255, 255, 255), 2)

            cv2.imshow("Piano Aereo - MediaPipe", frame)

            key = cv2.waitKey(10) & 0xFF
            if key == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()