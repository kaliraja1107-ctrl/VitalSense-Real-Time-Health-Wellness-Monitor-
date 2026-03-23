import cv2
import numpy as np
import os

def get_temperature_from_face():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Camera not working")
        return 36.5

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    temperature = 36.5
    frame_count = 0

    # Ensure static folder exists
    if not os.path.exists("static"):
        os.makedirs("static")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Always create thermal image
        thermal = cv2.applyColorMap(frame, cv2.COLORMAP_JET)

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                intensity = np.mean(face)

                # Simulated temperature
                temperature = 36 + (intensity / 255) * 2

                cv2.rectangle(thermal, (x, y), (x+w, y+h), (255,255,255), 2)

                cv2.putText(
                    thermal,
                    f"Temp: {round(temperature,2)} C",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,255,255),
                    2
                )
        else:
            # No face detected
            cv2.putText(
                thermal,
                "No Face Detected",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                2
            )

        # Save thermal image
        cv2.imwrite("static/thermal.jpg", thermal)

        # Show window
        cv2.imshow("🔥 VitalSense Thermal Camera", thermal)

        # Auto close after some frames
        if frame_count > 50:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return round(temperature, 2)