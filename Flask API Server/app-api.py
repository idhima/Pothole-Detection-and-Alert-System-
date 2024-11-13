from flask import Flask, request, jsonify
from detection import detect_potholes
from s3_upload import upload_to_s3
from alert_service import send_alert
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_and_alert():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Read image
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Detect potholes
    processed_image, potholes = detect_potholes(image)

    # Upload to S3 if potholes are detected
    if potholes:
        image_url = upload_to_s3(processed_image, 'detected_pothole.jpg')
        send_alert(len(potholes), image_url)
        return jsonify({'message': 'Potholes detected and alert sent', 'image_url': image_url}), 200
    else:
        return jsonify({'message': 'No potholes detected'}), 200

if __name__ == '__main__':
    app.run(debug=True)
