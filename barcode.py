import cv2
from pyzbar import pyzbar
import numpy as np

# Set to keep track of detected barcodes/QR codes
detected_data = set()

def decode(frame):
    global detected_data
    # Decode barcodes and QR codes in the frame
    decoded_objects = pyzbar.decode(frame)

    for obj in decoded_objects:
        # Decode the data
        data = obj.data.decode("utf-8")
        obj_type = obj.type

        # Check if the data has already been detected
        if data in detected_data:
            continue

        # Add the data to the set of detected codes
        detected_data.add(data)

        # Draw the bounding box around the detected barcode or QR code
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        for j in range(n):
            pt1 = (int(hull[j][0]), int(hull[j][1]))
            pt2 = (int(hull[(j + 1) % n][0]), int(hull[(j + 1) % n][1]))
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

        # Print the data
        print(f"Detected {obj_type}: {data}")

        # Display the data on the frame
        x = obj.rect.left
        y = obj.rect.top
        text = f"{data} ({obj_type})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

def main():
    global detected_data
    # Open the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Decode barcodes and QR codes
        frame = decode(frame)

        # Display the resulting frame
        cv2.imshow('Barcode and QR Code Scanner', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
