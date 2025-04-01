import cv2
import os
import time
from datetime import datetime

# ----------------------------
# Set Base Directory for Images
# ----------------------------
base_dir = r"P:\Sign Language Detector Application\Dataset"

# Create a new folder with timestamp to save images
folder_name = f"captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
save_dir = os.path.join(base_dir, folder_name)
os.makedirs(save_dir, exist_ok=True)

# ----------------------------
# Set Video Capture (Webcam)
# ----------------------------
cap = cv2.VideoCapture(0)  # Use 0 for default camera

# Set resolution (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ----------------------------
# Check if Camera is Opened
# ----------------------------
if not cap.isOpened():
    print("Error: Could not open camera. Exiting...")
    exit()

print("Press 'A' to start capturing 100 images...")

# ----------------------------
# Wait for 'A' to Start Capturing
# ----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame. Check the camera connection.")
        break

    cv2.imshow('Press A to start', frame)

    # Press 'A' to start capturing images
    if cv2.waitKey(1) & 0xFF == ord('a'):
        print("Starting to capture images...")
        break

# ----------------------------
# Capture 100 Images in 5 Seconds
# ----------------------------
num_images = 100
delay_between_frames = 5.0 / num_images  # ~0.05 seconds per frame

for i in range(num_images):
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print(f"Error: Failed to capture image {i}. Skipping...")
        continue

    # Save the image to the created folder
    image_path = os.path.join(save_dir, f"{i}.jpg")
    cv2.imwrite(image_path, frame)
    print(f"✅ Image {i} saved at {image_path}")

    # Delay to maintain 5 seconds for 100 images
    time.sleep(delay_between_frames)

# ----------------------------
# Release Resources
# ----------------------------
cap.release()
cv2.destroyAllWindows()

print(f"✅ 100 images captured and saved in '{save_dir}' folder successfully!")
