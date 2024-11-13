import cv2
import numpy as np
import tensorflow as tf

# Load the YOLOv5 model (replace with your model directory)
model = tf.saved_model.load('app/model/yolov5_model_directory')

def detect_potholes(image):
    input_tensor = tf.convert_to_tensor(image)
    input_tensor = input_tensor[tf.newaxis, ...]

    detections = model(input_tensor)

    potholes = []
    h, w, _ = image.shape

    # Process detections
    for i in range(int(detections['num_detections'][0])):
        class_id = int(detections['detection_classes'][0][i])
        score = float(detections['detection_scores'][0][i])

        # Class ID and threshold for 'pothole' detection
        if class_id == 1 and score > 0.5:
            box = detections['detection_boxes'][0][i]
            ymin, xmin, ymax, xmax = box
            (left, top, right, bottom) = (xmin * w, ymin * h, xmax * w, ymax * h)

            potholes.append((int(left), int(top), int(right), int(bottom), score))
            cv2.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 2)
            cv2.putText(image, f"Pothole {int(score * 100)}%", (int(left), int(top) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image, potholes
